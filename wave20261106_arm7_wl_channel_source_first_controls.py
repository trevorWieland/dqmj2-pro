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
from wave20261106_arm7_wl_channel_source_first_build import SOURCE,LANE,WORK,FLAGS,COMPILER,build_all
from wave20261106_arm7_wl_channel_source_first_bindings import controls as binding_controls
from wave20261106_arm7_wl_channel_source_first_boundary import certificate


def execute(rows):
    from wave20261106_arm7_wl_channel_source_first_layout import all_layouts,evaluate
    from wave20261106_arm7_wl_channel_source_first_boundary import controls as boundary
    baseline=read_json(LANE/'layout-baseline.json');fresh=all_layouts(WORK/'layout-fresh');fields=fresh['027e990c']['fields']
    if fields!=baseline['027e990c']['fields']:raise ValueError('Fresh consumed-field geometry differs')
    required={'WL_MAN.Config.EnableChannel.offset':812,'WL_MAN.Config.EnableChannel.width':2,'WL_MAN.Work.CurrChannel.offset':958,'WL_MAN.Work.CurrChannel.width':2,'WL_MAN.Rf.Id.offset':1528,'WL_MAN.Rf.BkReg.offset':1540,'WL_MAN.Rf.BkReg.width':4,'WL_MAN.Rf.InitNum.offset':1532,'WL_MAN.Rf.BbpCnt.offset':1536,'WL_MAN.Rf.BbpCnt.width':2,'WL_MAN.Rf.ChanNum.offset':1534,'FLASH_TABLE.rfInit_channelDependData.RF2958Tbl.ch_Reg.offset':200,'FLASH_TABLE.rfInit_channelDependData.RF2958Tbl.ch_PwrRF.offset':298,'FLASH_TABLE.rfInit_channelDependData.RF2958Tbl.ch_PwrBB.offset':284,'FLASH_TABLE.rfInit_channelDependData.MM3156Tbl.init.offset':164}
    if any(fields[k]!=v for k,v in required.items()):raise ValueError('Native addressing and measured field offsets differ')
    negatives=[]
    for label,old,new in [('bbp-count-width','u16 BbpCnt;','u32 BbpCnt;'),('flash-register-row-stride','u8 ch_Reg[14][6];','u8 ch_Reg[14][5];')]:
        headers={p.name:p.read_text(encoding='utf-8')for p in(SOURCE/'027e990c').glob('*.h')};count=sum(text.count(old)for text in headers.values())
        if count!=1:raise ValueError('Unique consumed type mutation absent')
        changed={name:text.replace(old,new)for name,text in headers.items()};bad=evaluate('027e990c',WORK/'layout-negative'/label,changed)
        if bad['fields']==fields:raise ValueError('Wrong consumed geometry accepted')
        negatives.append(dict(case=label,rejected=True,changedFields=[k for k,v in fields.items()if bad['fields'][k]!=v]))
    return dict(status='passed',sourceCredit=0,geometry=fresh,independentNativeOffsetChecks=required,fieldGeometryNegativeControls=negatives,requiredPrototypes=prototypes(rows),boundaryControls=boundary(),bindingControls=[binding_controls(row)for row in rows],actualC99=actual_c99(rows))


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
