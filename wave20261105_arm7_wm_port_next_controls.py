import copy
from project import ROOT,read_json,write_json,sha256
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from elftools.elf.elffile import ELFFile
from link_runtime_unit import relocation_rows
from wave20261105_arm7_wm_port_next_build import SOURCE,LANE,WORK,COMPILER,FLAGS,build
from wave20261105_arm7_wm_port_next_layout import evaluate,compile_unit
from wave20261105_arm7_wm_port_next_bindings import controls as binding_controls
from wave20261105_arm7_wm_port_next_boundary import certificate


def actual_c99(rows):
    if FLAGS.count('-lang')!=1 or FLAGS[FLAGS.index('-lang')+1]!='c99':raise ValueError('Production frontend is not actual explicit C99')
    fresh,outputs=build(SOURCE/'wm_port.c',WORK/'c99-independent');results=[]
    for a,b in zip(rows,fresh):
        if a['name']!=b['name'] or a['targetSha256']!=b['outputSha256'] or relocation_rows(ROOT/a['object'],a['name'])!=relocation_rows(ROOT/b['object'],b['name']) or not b['realLink']['exactCallerBytes']:raise ValueError('Fresh full C99 body/relocation/genuine link differs')
        results.append(dict(name=b['name'],bytes=b['bytes'],relocations=len(b['relocations']),objectSha256=b['objectSha256'],genuineLinkedCallerSha256=b['outputSha256']))
    import subprocess,os
    directory=WORK/'frontend';directory.mkdir(parents=True,exist_ok=True);source=directory/'frontend.c';source.write_text('int witness(void *p){int *value=p;return *value;}\n');witness=[]
    for language in ['c99','c++']:
        flags=list(FLAGS);flags[flags.index('-lang')+1]=language;output=directory/(language.replace('+','p')+'.o');argv=[str(COMPILER),*flags,'-c',str(source),'-o',str(output)];p=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
        if (language=='c99')!=(p.returncode==0):raise ValueError('Actual C99/C++ frontend witness failed')
        witness.append(dict(language=language,command=argv,exitCode=p.returncode,stdout=p.stdout,stderr=p.stderr))
    return dict(status='passed',freshFunctions=results,actualExplicitFrontend='c99',originalRelocations=sum(len(r['relocations']) for r in rows),frontendWitness=witness)


def abi():
    directory=WORK/'abi';directory.mkdir(parents=True,exist_ok=True)
    for p in SOURCE.glob('*.h'):(directory/p.name).write_bytes(p.read_bytes())
    text='\n'.join('#include "'+p.name+'"' for p in sorted(SOURCE.glob('*.h')))+'\nu32 abi_aid(WMStatus *p){return p->aid;}\nu32 abi_rest(WMPortSendQueueData *p){return p->restBitmap;}\nu32 abi_data(WMPortSendQueueData *p){return(u32)p->data;}\nu32 abi_recv(WMPortRecvCallback*p){return p->myAid;}\nu32 abi_callback(WMPortSendCallback*p){return(u32)p->callback;}\n'
    def evaluate_unit(payload,label):
        source=directory/(label+'.c');obj=directory/(label+'.o');source.write_text(payload);compile_unit(source,obj);cases=[]
        with obj.open('rb') as stream:
            elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
            for name,offset,width in [('abi_aid',392,2),('abi_rest',6,2),('abi_data',20,4),('abi_recv',32,2),('abi_callback',28,4)]:
                s=next(s for s in symbols if s.name==name);body=elf.get_section(s['st_shndx']).data()[s['st_value']:s['st_value']+s['st_size']]
                for value in ([0,1,32767,32768,65535] if width==2 else [0,1,0x027e0898,0x80000001,0xffffffff]):
                    vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_TI925T);vm.mem_map(0x02000000,0x10000);vm.mem_write(0x02000000,body);vm.mem_write(0x02002000+offset,value.to_bytes(width,'little'));vm.reg_write(R.UC_ARM_REG_CPSR,0x10);vm.reg_write(R.UC_ARM_REG_R0,0x02002000);vm.reg_write(R.UC_ARM_REG_SP,0x0200f000);vm.reg_write(R.UC_ARM_REG_LR,0x02001000);vm.emu_start(0x02000000,0x02001000,count=64)
                    if vm.reg_read(R.UC_ARM_REG_R0)!=value or vm.reg_read(R.UC_ARM_REG_PC)!=0x02001000:raise ValueError('Fresh actual word-width/unsigned-field/callback-word ABI differs')
                    cases.append(dict(function=name,offset=offset,width=width,returned=value))
        return dict(sourceSha256=sha256(source),objectSha256=sha256(obj),actualReturns=len(cases),cases=cases)
    positive=evaluate_unit(text,'positive');bad=[]
    for label,old,new in [('signed-aid','return p->aid','return(s16)p->aid'),('narrow-rest','return p->restBitmap','return(u8)p->restBitmap'),('narrow-data-pointer','return(u32)p->data','return(u16)(u32)p->data'),('wrong-callback-word','return(u32)p->callback','return(u32)p->callback+1')]:
        try:evaluate_unit(text.replace(old,new),label)
        except ValueError as error:bad.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong ABI witness admitted')
    return dict(status='passed',positive=positive,negatives=bad,callbackWordTransferredOnly=True,callbackInvocationOrSourceCredit=0)


def boundary_controls():
    records=read_json(LANE/'boundary-certificate.json')['functions'];image=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();results=[]
    for record in records:
        for label in ['mode','span-hash','invented-envelope','missing-literal','origin','instruction','width']:
            flow=copy.deepcopy(record['flow']);digest=record['nativeSpanSha256']
            if label=='mode':flow['entryMode']='thumb'
            elif label=='span-hash':digest='0'*64
            elif label=='invented-envelope':flow['computedEvidenceEndExclusive']=hex(int(flow['computedEvidenceEndExclusive'],0)+4);flow['computedEvidenceEnvelopeBytes']+=4
            elif label=='missing-literal':flow['literalReads']=[r for r in flow['literalReads'] if r['address']!=record['flow']['literalReads'][0]['address']]
            elif label=='origin':flow['literalReads'][0]['origin']=flow['entry']
            elif label=='instruction':flow['instructions'][0]['word']='0'
            else:flow['literalReads'][0]['bytes']=2
            try:certificate(flow,image,0x027e0000,digest)
            except ValueError as error:results.append(dict(address=record['address'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError('Wrong actual original WM port boundary admitted')
    return dict(status='passed',negativeControls=results,sourceCredit=0)


def execute(rows):
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261105/arm7-wm-port-next' or LANE!=ROOT/'evidence/lanes/parallel-wave20261105/arm7-wm-port-next' or WORK!=ROOT/'work/w5wp':raise ValueError('New WM port controls materializer scope differs')
    baseline=read_json(LANE/'layout-baseline.json');fresh=evaluate(WORK/'layout-fresh')
    if fresh['fields']!=baseline['fields']:raise ValueError('Actual closed C/compiler geometry changed')
    headers={p.name:p.read_text() for p in SOURCE.glob('*.h')};geometryBad=[]
    for label,old,new in [('queue-offset','WMPortSendQueueData sendQueueData[32 ]','u32 shiftedQueue;WMPortSendQueueData sendQueueData[32 ]'),('queue-field-width','u16 restBitmap;','u32 restBitmap;'),('queue-pointer-width','const u16 * data;','u16 data;')]:
        changed=dict(headers);found=[name for name,text in changed.items() if old in text]
        if not found:raise ValueError('Meaningful geometry mutation target absent: '+label)
        name=found[0];changed[name]=changed[name].replace(old,new,1)
        try:
            altered=evaluate(WORK/('layout-'+label),changed)
            if altered['fields']==baseline['fields']:raise RuntimeError('Wrong geometry mutation left all checked ABI values unchanged')
            geometryBad.append(dict(case=label,rejected=True,changedGeometry=True))
        except ValueError as error:geometryBad.append(dict(case=label,rejected=True,compileRejected=True,reason=str(error)))
    return dict(status='passed',sourceCredit=0,layout=fresh,geometryNegatives=geometryBad,actualABI=abi(),actualC99=actual_c99(rows),boundaryControls=boundary_controls(),bindingControls=[binding_controls(r) for r in rows])
