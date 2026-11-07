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
from wave20261106_arm7_rtc_loop_source_first_build import SOURCE,LANE,WORK,FLAGS,COMPILER,build_all
from wave20261106_arm7_rtc_loop_source_first_bindings import controls as binding_controls
from wave20261106_arm7_rtc_loop_source_first_boundary import certificate


def execute(rows):
    from wave20261106_arm7_rtc_loop_source_first_layout import all_layouts,evaluate
    from wave20261106_arm7_rtc_loop_source_first_boundary import controls as boundary
    baseline=read_json(LANE/'layout-baseline.json');fresh=all_layouts(WORK/'layout-fresh');fields=fresh['027f60b4']['fields']
    if fields!=baseline['027f60b4']['fields']:raise ValueError('Fresh consumed-field geometry differs')
    required={'RTCImportedView.opaquePrefix.width':4,'RTCImportedView.work.offset':4,'RTCImportedView.work.msgQueue.offset':4,'RTCImportedView.work.busy.offset':472,'RTCImportedView.work.busy.width':4,'RTCImportedView.work.command.offset':476,'RTCImportedView.work.command.width':2,'RTCWork.msgQueue.width':32,'RTCWork.busy.offset':468,'RTCWork.command.offset':472,'RTCRawData.sizeof':8,'RTCRawData.t.date.offset':0,'RTCRawData.t.time.offset':4,'RTCRawData.a.status1.offset':0,'RTCRawData.a.status1.width':2,'RTCRawData.a.status2.offset':2,'RTCRawData.a.pulse.offset':4,'OSSystemWork.real_time_clock.offset':488}
    if any(fields[k]!=v for k,v in required.items()):raise ValueError('Native addressing and measured field offsets differ')
    negatives=[]
    for label,old,new in [('busy-word-width','BOOL busy;','u16 busy;'),('opaque-prefix-offset','u8 opaquePrefix[4]','u8 opaquePrefix[8]')]:
        headers={p.name:p.read_text(encoding='utf-8')for p in(SOURCE/'027f60b4').glob('*.h')};count=sum(text.count(old)for text in headers.values())
        if count!=1:raise ValueError('Unique consumed type mutation absent')
        changed={name:text.replace(old,new)for name,text in headers.items()};bad=evaluate('027f60b4',WORK/'layout-negative'/label,changed)
        if bad['fields']==fields:raise ValueError('Wrong consumed geometry accepted')
        negatives.append(dict(case=label,rejected=True,changedFields=[k for k,v in fields.items()if bad['fields'][k]!=v]))
    from wave20261106_arm7_rtc_loop_source_first_storage import controls as storage_controls
    return dict(status='passed',sourceCredit=0,sourceStorage=storage_controls(rows[0],compile_unit),geometry=fresh,independentNativeOffsetChecks=required,fieldGeometryNegativeControls=negatives,requiredPrototypes=prototypes(rows),boundaryControls=boundary(),bindingControls=[binding_controls(row)for row in rows],actualC99=actual_c99(rows))


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
