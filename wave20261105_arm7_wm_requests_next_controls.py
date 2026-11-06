import copy
from project import ROOT,read_json,write_json,sha256
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from elftools.elf.elffile import ELFFile
from link_runtime_unit import relocation_rows
from wave20261105_arm7_wm_requests_next_build import SOURCE,LANE,WORK,COMPILER,FLAGS,build_all
from wave20261105_arm7_wm_requests_next_layout import evaluate,compile_unit,all_layouts
from wave20261105_arm7_wm_requests_next_bindings import controls as binding_controls
from wave20261105_arm7_wm_requests_next_boundary import certificate


def actual_c99(rows):
    if FLAGS.count('-lang')!=1 or FLAGS[FLAGS.index('-lang')+1]!='c99':raise ValueError('Production frontend is not actual explicit C99')
    fresh,outputs=build_all(WORK/'c99-independent');results=[]
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
    probes=[('027e614c','count','s32 abi(WMStatus*p){return p->mp_count;}',98,2,True),('027e614c','freq','u32 abi(WMStatus*p){return p->mp_current_freq;}',1986,2,False),('027e609c','queued','u32 abi(WMStatus*p){return p->valarm_queuedFlag;}',206,2,False),('027e609c','pointer','u32 abi(WMSPWork*p){return(u32)p->status;}',5456,4,False),('027e7d58','callback','u32 abi(WMCallback*p){return p->wlResult;}',6,2,False)];positive=[];bad=[]
    def run_probe(probe,payload,label):
        entry,name,_,offset,width,signed=probe;directory=WORK/'abi'/label;directory.mkdir(parents=True,exist_ok=True)
        for h in (SOURCE/entry).glob('*.h'):(directory/h.name).write_bytes(h.read_bytes())
        source=directory/'abi.c';obj=directory/'abi.o';source.write_text('\n'.join('#include "'+h.name+'"' for h in sorted((SOURCE/entry).glob('*.h')))+'\n'+payload+'\n');compile_unit(source,obj)
        with obj.open('rb') as stream:
            elf=ELFFile(stream);s=next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name=='abi');body=elf.get_section(s['st_shndx']).data()[s['st_value']:s['st_value']+s['st_size']]
        cases=[]
        for value in ([0,1,32767,32768,65535] if width==2 else [0,1,0x027e0898,0x80000001,0xffffffff]):
            vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_TI925T);vm.mem_map(0x02000000,0x10000);vm.mem_write(0x02000000,body);vm.mem_write(0x02002000+offset,value.to_bytes(width,'little'));vm.reg_write(R.UC_ARM_REG_CPSR,0x10);vm.reg_write(R.UC_ARM_REG_R0,0x02002000);vm.reg_write(R.UC_ARM_REG_SP,0x0200f000);vm.reg_write(R.UC_ARM_REG_LR,0x02001000);vm.emu_start(0x02000000,0x02001000,count=64);expected=(value-65536)&0xffffffff if signed and value&32768 else value
            if vm.reg_read(R.UC_ARM_REG_R0)!=expected or vm.reg_read(R.UC_ARM_REG_PC)!=0x02001000:raise ValueError('Fresh actual signed/unsigned/word/pointer ARMv4T ABI differs')
            cases.append(dict(input=value,returned=expected))
        return dict(name=name,cases=cases,actualReturns=len(cases),sourceSha256=sha256(source),objectSha256=sha256(obj))
    for probe in probes:
        positive.append(run_probe(probe,probe[2],probe[1]+'-positive'));payload=probe[2].replace('return p->mp_count','return(u16)p->mp_count') if probe[1]=='count' else probe[2].replace('return p->','return(u8)p->') if probe[4]==2 else probe[2].replace('return(u32)p->','return(u16)(u32)p->')
        try:run_probe(probe,payload,probe[1]+'-bad')
        except ValueError as error:bad.append(dict(case=probe[1],rejected=True,reason=str(error)))
        else:raise ValueError('Wrong ARM7 request ABI admitted')
    return dict(status='passed',positive=positive,negativeControls=bad,actualFreshReturns=sum(p['actualReturns'] for p in positive),sourceCredit=0)


def boundary_controls():
    records=read_json(LANE/'boundary-certificate.json')['functions'];image=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();results=[]
    for record in records:
        for label in ['mode','span-hash','invented-envelope','missing-literal','origin','instruction','width']:
            if not record['flow']['literalReads'] and label in ['missing-literal','origin','width']:continue
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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261105/arm7-wm-requests-next' or LANE!=ROOT/'evidence/lanes/parallel-wave20261105/arm7-wm-requests-next' or WORK!=ROOT/'work/w5wr':raise ValueError('New WM port controls materializer scope differs')
    baseline=read_json(LANE/'layout-baseline.json');fresh=all_layouts(WORK/'layout-fresh')
    if {k:v['fields'] for k,v in fresh.items()}!={k:v['fields'] for k,v in baseline.items()}:raise ValueError('Actual closed request C/compiler geometry changed')
    bad=[]
    for entry,label,old,new in [('027e609c','queued-width','u16 valarm_queuedFlag;','u32 valarm_queuedFlag;'),('027e7d58','result-width','u16 wlResult;','u32 wlResult;'),('027e83cc','mask-width','u32 mask;','u16 mask;')]:
        headers={p.name:p.read_text() for p in (SOURCE/entry).glob('*.h')};found=[name for name,text in headers.items() if old in text]
        if not found:raise ValueError('Meaningful geometry mutation absent: '+label)
        headers[found[0]]=headers[found[0]].replace(old,new,1)
        try:
            result=evaluate(entry,WORK/('layout-'+label),headers)
            if result['fields']==baseline[entry]['fields']:raise RuntimeError('Wrong geometry did not change checked fields')
            bad.append(dict(case=label,rejected=True,changedGeometry=True))
        except ValueError as error:bad.append(dict(case=label,rejected=True,compileRejected=True,reason=str(error)))
    return dict(status='passed',sourceCredit=0,layout=fresh,geometryNegatives=bad,actualABI=abi(),actualC99=actual_c99(rows),boundaryControls=boundary_controls(),bindingControls=[binding_controls(r) for r in rows])
