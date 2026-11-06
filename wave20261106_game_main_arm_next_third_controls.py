import copy
import os
import shutil
import subprocess
from project import ROOT,sha256
from elftools.elf.elffile import ELFFile
from wave20261106_game_main_arm_next_third_bindings import verify_original,negative_controls,validate,frozen_inputs
from wave20261106_game_main_arm_next_compiler import COMPILER

SOURCE=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/third'
WORK=ROOT/'work/w6gm/third-controls'


def sections(path):
    with path.open('rb') as stream:return [(s.name,s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&4]


def compile_source(source,obj,flags):
    return subprocess.run([str(COMPILER),*flags,'-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))


def execute(rows):
    if SOURCE!=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/third' or WORK!=ROOT/'work/w6gm/third-controls':raise ValueError('Exact third control paths differ')
    bindings=[]
    for row in rows:
        verify_original(row,row['nativeSymbolEntries'])
        for symbol,binding in row['nativeSymbolEntries'].items():
            if binding['kind']!='function':continue
            for label,key,value in [('wrong-mode','mode','thumb'),('wrong-CPU','processor','arm7'),('wrong-program','program','child'),('wrong-module','module','ov001' if binding['module']=='ov000' else 'ov000'),('wrong-address','address',hex(int(binding['address'],0)+4)),('function-as-data','kind','data')]:
                wrong=copy.deepcopy(row['nativeSymbolEntries']);wrong[symbol][key]=value
                try:verify_original(row,wrong)
                except ValueError as error:bindings.append(dict(caller=row['address'],symbol=symbol,case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Wrong original grouped provider identity admitted')
    declarations=[];providers={'0207211c':'native_fn_02065818','02071b28':'native_fn_02065d28','02073090':'native_fn_ov000_022162c0','0207313c':'native_fn_02065d88'}
    for row in rows:
        name=format(int(row['address'],0),'08x');folder=WORK/'prototypes'/name;folder.mkdir(parents=True,exist_ok=True);obj=folder/'explicit.o';flags=[*row['compilerFlags'],'-requireprotos','-w','error'];positive=compile_source(ROOT/row['source'],obj,flags)
        if positive.returncode or sections(obj)!=sections(ROOT/row['object']):raise ValueError(('Actual required grouped prototype failed or changed executable sections',positive.stdout,positive.stderr))
        text=(SOURCE/'context.h').read_text();symbol=providers[name]
        if text.count(symbol+'(')!=1:raise ValueError('Actual missing grouped provider mutation ambiguous')
        (folder/'context.h').write_text(text.replace(symbol+'(','missing_callable_declaration(',1));wrong=folder/'missing.c';shutil.copyfile(ROOT/row['source'],wrong);badobj=folder/'missing.o';bad=compile_source(wrong,badobj,flags)
        if bad.returncode==0 or badobj.exists() or 'no prototype' not in bad.stdout:raise ValueError(('Actual missing grouped declaration admitted',bad.stdout,bad.stderr))
        declarations.append(dict(caller=row['address'],positiveExitCode=0,executableSectionsUnchanged=True,missingActualProvider=symbol,negativeExitCode=bad.returncode,negativeStdout=bad.stdout,diagnosticFlags=flags))
    folder=WORK/'layout';folder.mkdir(exist_ok=True);source=folder/'layout.c';header=(SOURCE/'context.h').read_text();checks=['sizeof(void*)==4','sizeof(LayoutRecord)==12','(u32)&((ContextPrefix*)0)->rows==16','(u32)&((DetailPrefix*)0)->flags==0x1d','(u32)&((GlobalPrefix*)0)->detail==0x20','(u32)&((CounterPrefix*)0)->flags==0xd1','(u32)&((CounterPrefix*)0)->slot==0xd5','(u32)&((CounterPrefix*)0)->counter==0xe0','(u32)&((IndexPrefix*)0)->index==0xd8','(u32)&((PagePrefix*)0)->status==0x7d7','(u32)&((PagePrefix*)0)->flags==0x7da','sizeof(Nibbles)==1','sizeof(ControlFlags)==1']
    source.write_text('#include "context.h"\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks))+'\nconst Nibbles geometryNibble={.low=5,.high=10};\nconst ControlFlags geometrySigned={.bits={-1,0,-1,0,-3}};\n');obj=folder/'layout.o';layouts=[]
    for label,text,positive in [('positive',header,True),('wrong-record-stride',header.replace('words[3]','words[4]'),False),('wrong-counter-origin',header.replace('prefix[0xd1]','prefix[0xd0]'),False),('wrong-nibble-order',header.replace('u8 low:4;u8 high:4','u8 high:4;u8 low:4'),False)]:
        (folder/'context.h').write_text(text);process=compile_source(source,obj,rows[0]['compilerFlags']);valid=process.returncode==0;objects={}
        if valid:
            with obj.open('rb') as stream:
                elf=ELFFile(stream)
                for symbol in elf.get_section_by_name('.symtab').iter_symbols():
                    if symbol.name in ['geometryNibble','geometrySigned']:objects[symbol.name]=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']].hex()
            valid=objects==dict(geometryNibble='a5',geometrySigned='d5')
        if valid!=positive:raise ValueError(('Actual geometry/nibble layout acceptance differs',label,process.stdout,objects))
        layouts.append(dict(case=label,exitCode=process.returncode,accepted=positive,actualInitializerBytes=objects,stdout=process.stdout))
    value=frozen_inputs();case=next(c for c in value['cases'] if c['symbol']=='native_data_020daf42');row=next(r for r in rows if r['address']==case['caller']);rel=next(r for r in row['relocations'] if r['symbol']==case['symbol']);binding=row['nativeSymbolEntries'][case['symbol']];image=(ROOT/value['image']['path']).read_bytes();inventory=(ROOT/value['inventory']['path']).read_text();loads=(ROOT/value['relocations']['path']).read_text();initialized=[]
    for key,wrong in [('minimumInitializedPrefix',16),('indexMinimum',1),('indexMaximum',9),('indexStride',1),('elementWidth',2),('signedElement',False),('initializedPrefixSha256','0'*64)]:
        changed=copy.deepcopy(case);changed[key]=wrong
        try:validate(changed,row,rel,binding,image,inventory,loads)
        except ValueError as error:initialized.append(dict(case='wrong-'+key,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong initialized lookup shape admitted')
    changed=bytearray(image);changed[0xdaf42]^=128
    try:validate(case,row,rel,binding,bytes(changed),inventory,loads)
    except ValueError as error:initialized.append(dict(case='changed-original-prefix',rejected=True,reason=str(error)))
    else:raise ValueError('Changed initialized lookup bytes admitted')
    return dict(status='passed',sourceCredit=0,originalBindingRejections=bindings,originalDataRejections=negative_controls(rows),initializedLookupRejections=initialized,requiredPrototypeDiagnostics=declarations,actualGeometryChecks=checks,actualCompilerLayouts=layouts,completeOriginalAllocationExtent=None,externalStorageCredit=0)
