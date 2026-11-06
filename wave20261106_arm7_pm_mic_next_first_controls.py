import copy
import os
import re
import struct
import subprocess
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from elftools.elf.elffile import ELFFile
from project import ROOT,read_json,write_json,sha256
from link_runtime_unit import relocation_rows
from wave20261106_arm7_pm_mic_next_first_build import SOURCE,LANE,WORK,FLAGS,COMPILER,build_all
from wave20261106_arm7_pm_mic_next_first_bindings import controls as binding_controls
from wave20261106_arm7_pm_mic_next_first_boundary import certificate


def compile_unit(source,obj,strict=False):
    obj.parent.mkdir(parents=True,exist_ok=True);argv=[str(COMPILER),*FLAGS,*(['-requireprotos','-w','error']if strict else []),'-c',str(source),'-o',str(obj)]
    process=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    return dict(command=argv,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr)


def function_body(obj,name):
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==name)
        return elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]


FIELDS=[('u8',1),('u16',2),('u32',4),('MICWork',60),('MICStatus',4),('SPIEntry',24),('OSSystemWork',1024)]
OFFSETS=[('MICWork','command',0),('MICWork','status',32),('MICWork','type',36),('MICWork','admode',38),('MICWork','buf',40),('MICWork','index',44),('MICWork','size',48),('MICWork','timerValue',52),('MICWork','timerPrescaler',54),('MICWork','temp16',56),('MICWork','temporary',58),('SPIEntry','process',4),('SPIEntry','arg',8),('OSSystemWork','mic_last_address',912),('OSSystemWork','mic_sampling_data',916)]


def geometry(directory,mutation=None):
    directory.mkdir(parents=True,exist_ok=True)
    for path in (SOURCE/'03805784').glob('*'):
        if path.is_file():(directory/path.name).write_bytes(path.read_bytes())
    if mutation:
        path=directory/'context000.h';text=path.read_text();old,new=mutation
        if text.count(old)!=1:raise ValueError('Geometry mutation not unique')
        path.write_text(text.replace(old,new))
    expressions=['sizeof('+name+')'for name,_ in FIELDS]+['(u32)&(('+typ+'*)0)->'+field for typ,field,_ in OFFSETS]
    source=directory/'geometry.c';source.write_text('#include "main.c"\nu32 geometry[]={'+','.join(expressions)+'};\n');obj=directory/'geometry.o';attempt=compile_unit(source,obj)
    if attempt['exitCode']:raise ValueError(('Actual C99 geometry compilation failed',attempt))
    raw=function_body(obj,'geometry');values=list(struct.unpack('<'+'I'*(len(raw)//4),raw));expected=[n for _,n in FIELDS]+[n for _,_,n in OFFSETS]
    if values!=expected:raise ValueError(('Actual closed C geometry differs',values,expected))
    return dict(status='passed',fields=[dict(name=name,bytes=value)for(name,_),value in zip(FIELDS,values)],offsets=[dict(type=typ,field=field,offset=value)for typ,field,value in OFFSETS],sourceSha256=sha256(source),objectSha256=sha256(obj))


def prototypes(rows):
    positive=[];negative=[];used=set()
    for row in rows:
        directory=WORK/'prototypes'/format(int(row['address'],0),'08x');directory.mkdir(parents=True,exist_ok=True)
        for path in (ROOT/row['source']).parent.glob('*'):
            if path.is_file():(directory/path.name).write_bytes(path.read_bytes())
        obj=directory/'positive.o';attempt=compile_unit(directory/'main.c',obj,True)
        if attempt['exitCode'] or function_body(obj,row['name'])!=function_body(ROOT/row['object'],row['name']) or relocation_rows(obj,row['name'])!=relocation_rows(ROOT/row['object'],row['name']):raise ValueError(('Actual required-prototype C99 changed or failed',attempt))
        positive.append(dict(name=row['name'],objectSha256=sha256(obj),relocationsIdentical=True))
        names=[row['name']]+[name for name,binding in row['nativeSymbolEntries'].items()if binding['kind']=='function'and name!='_u32_div_f'and name not in used]
        for name in names:
            target=directory/('missing-'+name);target.mkdir(parents=True,exist_ok=True)
            for path in directory.glob('*.c'):(target/path.name).write_bytes(path.read_bytes())
            headers={p.name:p.read_text()for p in directory.glob('*.h')};omitted=0
            for header,text in headers.items():
                pattern=r'^.*\b'+re.escape(name)+r'\s*\([^;{}]*\);\s*$';text,count=re.subn(pattern,'',text,flags=re.M);omitted+=count;(target/header).write_text(text)
            if omitted<1:raise ValueError(('Exact actual prototype omission not unique',name,omitted))
            failure=compile_unit(target/'main.c',target/'bad.o',True);diagnostics=(failure['stdout']+failure['stderr']).lower()
            if failure['exitCode']==0 or name.lower()not in diagnostics or not any(term in diagnostics for term in ['no prototype','undefined identifier']):raise ValueError(('Missing actual prototype not rejected',name,failure))
            negative.append(dict(name=name,rejected=True,attempt=failure));used.add(name)
    return dict(status='passed',positive=positive,negativeControls=negative)


def abi():
    probes=[('command','u32 abi(MICWork*p){return p->command[0];}',0,2),('status','u32 abi(MICWork*p){return p->status;}',32,4),('buffer','u32 abi(MICWork*p){return(u32)p->buf;}',40,4),('timer','u32 abi(MICWork*p){return p->timerValue;}',52,2),('sample','u32 abi(OSSystemWork*p){return p->mic_sampling_data;}',916,2),('last-address','u32 abi(OSSystemWork*p){return p->mic_last_address;}',912,4)];positive=[];negative=[]
    def actual(probe,body,label):
        name,_,offset,width=probe;directory=WORK/'abi'/label;directory.mkdir(parents=True,exist_ok=True);(directory/'context000.h').write_bytes((SOURCE/'03805784/context000.h').read_bytes());source=directory/'abi.c';obj=directory/'abi.o';source.write_text('#include "context000.h"\n'+body+'\n');attempt=compile_unit(source,obj)
        if attempt['exitCode']:raise ValueError(('Actual ABI compilation failed',attempt))
        code=function_body(obj,'abi');cases=[]
        for value in ([0,1,32768,65535]if width==2 else[0,1,0x80000001,0xffffffff]if width==4 else[0,1,0x123456789abcdef0,0x8000000100000000,0xffffffffffffffff]):
            vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_TI925T);vm.mem_map(0x02000000,0x10000);vm.mem_write(0x02000000,code);vm.mem_write(0x02002000+offset,value.to_bytes(width,'little'));vm.reg_write(R.UC_ARM_REG_CPSR,0x10);vm.reg_write(R.UC_ARM_REG_R0,0x02002000);vm.reg_write(R.UC_ARM_REG_SP,0x0200f000);vm.reg_write(R.UC_ARM_REG_LR,0x02001000);vm.emu_start(0x02000000,0x02001000,count=64);returned=vm.reg_read(R.UC_ARM_REG_R0)|(vm.reg_read(R.UC_ARM_REG_R1)<<32 if width==8 else 0)
            if returned!=value or vm.reg_read(R.UC_ARM_REG_PC)!=0x02001000:raise ValueError('Actual word-width/longlong ARMv4T ABI differs')
            cases.append(dict(input=value,returned=returned))
        return dict(name=name,actualReturns=len(cases),cases=cases,sourceSha256=sha256(source),objectSha256=sha256(obj))
    for probe in probes:
        positive.append(actual(probe,probe[1],probe[0]+'-positive'));cast='u32'if probe[3]==8 else'u8'if probe[3]==2 else'u16';bad=probe[1].replace('return(u32)p->','return(u16)(u32)p->')if probe[0]=='buffer'else probe[1].replace('return p->','return('+cast+')p->')
        try:actual(probe,bad,probe[0]+'-bad')
        except ValueError as error:negative.append(dict(case=probe[0],rejected=True,reason=str(error)))
        else:raise ValueError('Wrong actual field ABI admitted')
    return dict(status='passed',sourceCredit=0,positive=positive,negativeControls=negative,actualFreshReturns=sum(r['actualReturns']for r in positive))


def boundary_controls():
    records=read_json(LANE/'boundary-certificate.json')['functions'];image=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();results=[]
    for record in records:
        for label in ['mode','span-hash','invented-envelope','missing-literal','one-origin-omitted','origin','instruction','width']:
            if not record['flow']['literalReads']and label in ['missing-literal','one-origin-omitted','origin','width']:continue
            flow=copy.deepcopy(record['flow']);digest=record['nativeSpanSha256']
            if label=='mode':flow['entryMode']='thumb'
            elif label=='span-hash':digest='0'*64
            elif label=='invented-envelope':flow['computedEvidenceEndExclusive']=hex(int(flow['computedEvidenceEndExclusive'],0)+4);flow['computedEvidenceEnvelopeBytes']+=4
            elif label=='missing-literal':flow['literalReads']=[r for r in flow['literalReads']if r['address']!=record['flow']['literalReads'][0]['address']]
            elif label=='one-origin-omitted':flow['literalReads'].pop()
            elif label=='origin':flow['literalReads'][0]['origin']=hex(int(flow['literalReads'][0]['origin'],0)+4)
            elif label=='instruction':flow['instructions'][0]['word']='0'
            else:flow['literalReads'][0]['bytes']=2
            try:certificate(flow,image,0x037f8000,digest)
            except ValueError as error:results.append(dict(address=record['address'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError(('Wrong actual original PM boundary admitted',record['address'],label))
    return dict(status='passed',sourceCredit=0,negativeControls=results)


def execute(rows):
    geometry_positive=geometry(WORK/'geometry-positive');baseline=read_json(LANE/'layout-baseline.json');bad=[]
    if geometry_positive['fields']!=baseline['fields']or geometry_positive['offsets']!=baseline['offsets']:raise ValueError('Frozen measured PM geometry changed')
    for label,mutation in [('command-width',('u16 command[16 ]','u32 command[16 ]')),('timer-width',('u16 timerValue;','u32 timerValue;')),('sample-width',('u16 mic_sampling_data;','u32 mic_sampling_data;'))]:
        try:geometry(WORK/('geometry-'+label),mutation)
        except ValueError as error:bad.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong actual PM geometry admitted')
    from wave20261106_arm7_pm_mic_next_first_callback import execute as callback_controls
    return dict(status='passed',sourceCredit=0,callbackABI=callback_controls(rows),geometry=geometry_positive,geometryNegatives=bad,actualABI=abi(),requiredPrototypes=prototypes(rows),boundaryControls=boundary_controls(),bindingControls=[binding_controls(r)for r in rows],actualC99=actual_c99(rows))


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
