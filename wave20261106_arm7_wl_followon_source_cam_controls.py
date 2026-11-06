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
from wave20261106_arm7_wl_followon_source_cam_build import SOURCE,LANE,WORK,FLAGS,COMPILER,build_all
from wave20261106_arm7_wl_followon_source_cam_bindings import controls as binding_controls
from wave20261106_arm7_wl_followon_source_cam_boundary import certificate


def primitive_abi():
    probes=[('upper-byte','u32 abi(u16 value){return(value>>8)&255;}','u32 abi(u16 value){return value&255;}',[0,1,255,256,0x12ab,65535],lambda n:n>>8),('query-truncate','u32 abi(u32 value){return(u16)value;}','u32 abi(u32 value){return(u8)value;}',[0,1,0x1234abcd,0x8000ffff,0xffffffff],lambda n:n&65535),('full-return','u32 abi(u32 value){return value;}','u32 abi(u32 value){return(u16)value;}',[0,1,0x1234abcd,0x8000ffff,0xffffffff],lambda n:n)]
    positive=[];negative=[]
    def actual(probe,body,label):
        name,_,_,values,expected=probe;directory=WORK/'abi'/label;directory.mkdir(parents=True,exist_ok=True);
        for path in (SOURCE/'027ebc50').glob('*'):
            if path.suffix in ['.c','.h']:(directory/path.name).write_bytes(path.read_bytes())
        source=directory/'abi.c';obj=directory/'abi.o';source.write_text('#include "main.c"\n'+body+'\n');attempt=compile_unit(source,obj)
        if attempt['exitCode']:raise ValueError(('Actual primitive ABI compilation failed',attempt))
        code=function_body(obj,'abi');cases=[]
        for value in values:
            vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_TI925T);vm.mem_map(0x02000000,0x10000);vm.mem_write(0x02000000,code);vm.reg_write(R.UC_ARM_REG_CPSR,0x10);vm.reg_write(R.UC_ARM_REG_R0,value);vm.reg_write(R.UC_ARM_REG_SP,0x0200f000);vm.reg_write(R.UC_ARM_REG_LR,0x02001000);vm.emu_start(0x02000000,0x02001000,count=64)
            if vm.reg_read(R.UC_ARM_REG_R0)!=expected(value)or vm.reg_read(R.UC_ARM_REG_PC)!=0x02001000:raise ValueError('Actual promoted16-bit/32-bit return ABI differs')
            cases.append(dict(input=value,returned=expected(value)))
        return dict(name=name,sourceSha256=sha256(source),objectSha256=sha256(obj),actualReturns=len(cases),cases=cases)
    for probe in probes:
        positive.append(actual(probe,probe[1],probe[0]+'-positive'))
        try:actual(probe,probe[2],probe[0]+'-bad')
        except ValueError as error:negative.append(dict(case=probe[0],rejected=True,reason=str(error)))
        else:raise ValueError('Wrong promoted-word/return ABI admitted')
    return dict(status='passed',sourceCredit=0,positive=positive,negativeControls=negative,actualFreshReturns=sum(r['actualReturns']for r in positive))


def geometry():
    directory=WORK/'geometry';directory.mkdir(parents=True,exist_ok=True);(directory/'context.h').write_bytes((SOURCE/'027f4b88/context000.h').read_bytes());source=directory/'geometry.c';obj=directory/'geometry.o';source.write_text('#include "context.h"\nu32 dimensions[]={sizeof(u8),sizeof(u16),sizeof(u32)};\n');attempt=compile_unit(source,obj)
    if attempt['exitCode']or struct.unpack('<3I',function_body(obj,'dimensions'))!=(1,2,4):raise ValueError('Actual owned primitive C geometry differs')
    return dict(status='passed',sourceCredit=0,unsignedCharBytes=1,unsignedShortBytes=2,unsignedLongBytes=4,objectSha256=sha256(obj))


def execute(rows):
    from wave20261106_arm7_wl_followon_source_cam_layout import all_layouts,evaluate
    baseline=read_json(LANE/'layout-baseline.json');fresh=all_layouts(WORK/'layout-fresh')
    if any(fresh[tag]['fields']!=baseline[tag]['fields']for tag in baseline):raise ValueError('Fresh complete owned C geometry differs')
    negative=[]
    for tag,typ,label,old,new in [('027ebc50','WlStaElement','state-width',r'u16\s+state;','u32 state;'),('027ebb50','WlStaElement','frame-count-width',r'u16\s+frameCount;','u32 frameCount;')]:
        headers={p.name:p.read_text()for p in (SOURCE/tag).glob('*.h')};changed={};count=0
        for name,text in headers.items():
            matches=list(re.finditer(r'typedef\s+struct\s*{[^{}]*}\s*'+typ+';',text));changed[name]=text
            for match in matches:
                replacement,n=re.subn(old,new,match.group());count+=n;changed[name]=text[:match.start()]+replacement+text[match.end():]
        if count!=1:raise ValueError(('Actual CAM field mutation not unique',label,count))
        try:
            bad=evaluate(tag,WORK/'layout-negative'/label,changed)
            if bad['fields']==baseline[tag]['fields']:raise RuntimeError('Incorrect CAM field geometry admitted')
        except ValueError:pass
        negative.append(dict(case=label,rejected=True))
    return dict(status='passed',sourceCredit=0,geometry=fresh,fieldGeometryNegativeControls=negative,actualABI=primitive_abi(),requiredPrototypes=prototypes(rows),boundaryControls=boundary_controls(),bindingControls=[binding_controls(row)for row in rows],actualC99=actual_c99(rows))


def compile_unit(source,obj,strict=False):
    obj.parent.mkdir(parents=True,exist_ok=True);argv=[str(COMPILER),*FLAGS,*(['-requireprotos','-w','error']if strict else []),'-c',str(source),'-o',str(obj)]
    process=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    return dict(command=argv,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr)

def function_body(obj,name):
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==name)
        return elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]

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
                pattern=r'^[ \t]*(?:extern[ \t]+)?[A-Za-z_][\w \t*]*[ \t*]+\b'+re.escape(name)+r'\s*\([^;{}]*\);[ \t]*$';text,count=re.subn(pattern,'',text,flags=re.M);omitted+=count;(target/header).write_text(text)
            if omitted<1:raise ValueError(('Exact actual prototype omission not unique',name,omitted))
            failure=compile_unit(target/'main.c',target/'bad.o',True);diagnostics=(failure['stdout']+failure['stderr']).lower()
            if failure['exitCode']==0 or name.lower()not in diagnostics or not any(term in diagnostics for term in ['no prototype','undefined identifier']):raise ValueError(('Missing actual prototype not rejected',name,failure))
            negative.append(dict(name=name,rejected=True,attempt=failure));used.add(name)
    return dict(status='passed',positive=positive,negativeControls=negative)

def boundary_controls():
    records=read_json(LANE/'boundary-certificate.json')['functions'];image=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();results=[]
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
            try:certificate(flow,image,0x027e0000,digest)
            except ValueError as error:results.append(dict(address=record['address'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError(('Wrong actual original PM boundary admitted',record['address'],label))
    return dict(status='passed',sourceCredit=0,negativeControls=results)

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
