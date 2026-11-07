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
from wave20261106_arm7_wl_rxman_source_first_build import SOURCE,LANE,WORK,FLAGS,COMPILER,build_all
from wave20261106_arm7_wl_rxman_source_first_bindings import controls as binding_controls
from wave20261106_arm7_wl_rxman_source_first_boundary import certificate


def execute(rows):
    from wave20261106_arm7_wl_rxman_source_first_layout import all_layouts,evaluate
    baseline=read_json(LANE/'layout-baseline.json');fresh=all_layouts(WORK/'layout-fresh')
    if fresh['027f3f40']['fields']!=baseline['027f3f40']['fields']:raise ValueError('Fresh measured consumed-field geometry differs')
    fields=fresh['027f3f40']['fields'];required={'WL_MAN.HeapMan.RxManCtrl.Head.offset':476,'WL_MAN.HeapMan.RxManCtrl.Count.offset':484,'WL_MAN.Work.Mode.offset':848,'WL_MAN.Counter.rx.fragment.offset':1376,'WL_MAN.Counter.rx.unicast.offset':1380,'WL_MAN.Counter.rx.multicast.offset':1384,'WL_MAN.Counter.rx.duplicateErr.offset':1400,'RXPACKET.frame.offset':16,'RXFRM.FirmHeader.CamAdrs.offset':2,'RXFRM.MacHeader.Rx.Status.offset':8,'RXFRM.Dot11Header.FrameCtrl.offset':20,'RXFRM.Dot11Header.Adrs1.offset':24,'RXFRM.Dot11Header.Adrs2.offset':30,'RXFRM.Dot11Header.SeqCtrl.offset':42}
    if any(fields[k]!=v for k,v in required.items()):raise ValueError('Native entry/CFG measured consumed offsets disagree')
    negative=[]
    for label,old,new in [('multicast-width',r'(u32\s+rts;\s*u32\s+fragment;\s*u32\s+unicast;\s*)u32(\s+multicast;)',r'\1u16\2'),('queue-count-width',r'(LPHEAPBUF_HEADER Head;\s*LPHEAPBUF_HEADER Tail;\s*)u16(\s+Count;)',r'\1u32\2')]:
        headers={p.name:p.read_text(encoding='utf-8-sig')for p in(SOURCE/'027f3f40').glob('*.h')};changed={};count=0
        for name,text in headers.items():changed[name],n=re.subn(old,new,text);count+=n
        if count!=1:raise ValueError(('One actual measured type field expected',label,count))
        bad=evaluate('027f3f40',WORK/'layout-negative'/label,changed)
        if bad['fields']==fields:raise ValueError('Altered measured geometry unexpectedly admitted')
        negative.append(dict(case=label,rejected=True,changedFields=[k for k,v in fields.items()if bad['fields'][k]!=v]))
    return dict(status='passed',sourceCredit=0,geometry=fresh,independentNativeOffsetChecks=required,fieldGeometryNegativeControls=negative,requiredPrototypes=prototypes(rows),boundaryControls=boundary_controls(),bindingControls=[binding_controls(row)for row in rows],actualC99=actual_c99(rows))


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
