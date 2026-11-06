import gzip
import hashlib
import json
import struct
import subprocess
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from check_windows_i386_layout_20261101 import PINS
from main_anim_init160_fixture_20261102 import inputs
from match_main_anim_graph1004_20261102 import SPECS,source_path,REPORT as NATIVE_REPORT
from link_runtime_unit import measured_module

WORK=ROOT/'work/main-anim-graph1004-windows32-20261102'
REPORT=ROOT/'evidence/ports/main-anim-graph1004-windows32-20261102.json'
DRIVER='src/ports/20261102_anim_graph1004/driver.c'
DICTIONARY='src/runtime/20261101_resource_dictionary/native_main_0202bd74.c'


def compile_sources(sources,label):
    tools=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    for name,digest in PINS.items():assert sha256(tools/name)==digest,name
    folder=WORK/label;folder.mkdir(parents=True,exist_ok=True);definition=folder/'kernel32.def';library=folder/'kernel32.lib'
    definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nGetStdHandle@4\nReadFile@20\nWriteFile@20\nVirtualAlloc@16\nVirtualFree@12\nExitProcess@4\n',encoding='ascii')
    commands=[[str(tools/'llvm-dlltool.exe'),'-m','i386','-k','-d',str(definition),'-l',str(library)]]
    objects=[];records=[]
    for index,name in enumerate([*sources,DICTIONARY,DRIVER]):
        path=ROOT/name;obj=folder/f'source-{index}.obj';objects.append(obj)
        command=[str(tools/'clang.exe'),'--driver-mode=cl','--target=i686-pc-windows-msvc','/TC','/std:c11','/O2','/GS-','/Zl','/Brepro',
         '/clang:-ffreestanding','/clang:-fno-builtin','/clang:-fno-strict-aliasing','/w','/c',str(path),'/Fo'+str(obj)]
        if name==DICTIONARY:command.append('/Dnative_main_0202bd74=selected_dictionary_index')
        commands.append(command)
    exe=folder/'anim_graph1004.exe'
    commands.append([str(tools/'ld.lld.exe'),'-flavor','link','/entry:entry','/subsystem:console','/machine:x86','/nodefaultlib',
     '/timestamp:0','/fixed','/base:0x00400000','/out:'+str(exe),*[str(p)for p in objects],str(library)])
    for command in commands:
        run=subprocess.run(command,cwd=ROOT,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,(command,run.stdout,run.stderr)
    for name,obj in zip([*sources,DICTIONARY,DRIVER],objects):
        assert struct.unpack_from('<I',obj.read_bytes(),4)[0]==0
        records.append(dict(source=name,sourceSha256=sha256(ROOT/name),objectSha256=sha256(obj)))
    raw=exe.read_bytes();offset=struct.unpack_from('<I',raw,0x3C)[0]
    assert struct.unpack_from('<H',raw,offset+4)[0]==0x14C and struct.unpack_from('<I',raw,offset+8)[0]==0
    return exe,dict(sources=records,commands=commands,binary=exe.relative_to(ROOT).as_posix(),binarySha256=sha256(exe))


def run_cases(exe,payload,cases,expected_pages):
    run=subprocess.run([str(exe)],input=payload,cwd=ROOT.parent,capture_output=True,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
    assert run.returncode==0,(run.returncode,run.stderr)
    stride=12+65536;assert len(run.stdout)==len(cases)*stride
    rejected=0;rows=[]
    for index,(case,expected)in enumerate(zip(cases,expected_pages)):
        offset=index*stride;ordinal,fills,dictionaries=struct.unpack_from('<3I',run.stdout,offset)
        page=run.stdout[offset+12:offset+stride];assert ordinal==index
        expected_fills=sum(c['entry']==0x02008BE0 for c in case['calls'])
        expected_dictionaries=sum(c['entry']==0x0202BD74 for c in case['calls'])
        passed=page==expected and hashlib.sha256(page).hexdigest()==case['dataSha256']and fills==expected_fills and dictionaries==expected_dictionaries
        rejected+=not passed;rows.append(dict(index=index,modelPassed=passed,fillCalls=fills,dictionaryCalls=dictionaries,dataSha256=hashlib.sha256(page).hexdigest()))
    return dict(actualPublicReturns=len(cases),rejected=rejected,positiveControls=len(cases)-rejected,
     caseSha256=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
     fillBackendCalls=sum(r['fillCalls']for r in rows),reconstructedDictionaryCalls=sum(r['dictionaryCalls']for r in rows))


def main():
    native=read_json(NATIVE_REPORT);trace=ROOT/native['replayDependencies'][0]['path'];assert sha256(trace)==native['replayDependencies'][0]['sha256']
    cases=json.loads(gzip.decompress(trace.read_bytes()))['cases'];assert len(cases)==640
    metadata,image,unused=measured_module('main');chunks=[struct.pack('<I',640)];pages=[]
    for case in cases:
        index=case['index'];page,expected,args,table,count,selected,context=inputs(image,index)
        assert context==case['context']and selected==case['selectedCallback']
        chunks.append(struct.pack('<6I',index,count,*args)+table+page);pages.append(bytes(expected))
    payload=b''.join(chunks);sources=[source_path(a).relative_to(ROOT).as_posix()for a in SPECS];results=[]
    for label,entry in [('preferred',None),*[(f'wrong-{a:08x}',a)for a in SPECS]]:
        chosen=list(sources)
        if entry is not None:
            path=WORK/f'wrong-{entry:08x}.c';text=source_path(entry).read_text(encoding='utf-8')
            old,new=('priority = 127','priority = 126')if entry==0x0202E8B8 else('>> 24','>> 23')if entry==0x02032324 else('0x100','0x200')
            changed=text.replace(old,new);assert changed!=text;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(changed,encoding='utf-8')
            chosen[list(SPECS).index(entry)]=path.relative_to(ROOT).as_posix()
        exe,built=compile_sources(chosen,label);execution=run_cases(exe,payload,cases,pages)
        assert (execution['rejected']==0)==(entry is None),(label,execution)
        if entry is not None:
            expected_control=next(c for c in native['negativeControls']if int(c['address'],0)==entry)
            assert execution['rejected']==expected_control['rejected'],(label,execution,expected_control)
        results.append(dict(label=label,build=built,execution=execution))
    write_json(REPORT,dict(passed=True,sourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),
     sourceBuild=results[0]['build'],actualWindowsGameFunctionReturns=640,actualWrongPublicReturns=3840,controls=results[1:],
     windowsCaseSha256=results[0]['execution']['caseSha256'],positiveExecution=results[0]['execution'],
     originalSourceBodiesCompiled=6,selectedDictionarySourceCompiled=True,explicitCpuFillBackend=True,
     functionPointerTableRelocatedByIdentity=True,defaultCalculationPointerWordsStoredOnly=True,
     nativeReportSha256=sha256(NATIVE_REPORT),tools=[dict(path='tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin/'+n,sha256=d)for n,d in PINS.items()],
     coffMachine='I386',fullGame=False,androidDeviceExecutions=0,reproductionCommand='python check_main_anim_graph1004_windows32_20261102.py'))
    print(dict(windowsGameFunctionReturns=640,wrongPublicReturns=3840,wrongRejected=sum(r['execution']['rejected']for r in results[1:])))


if __name__=='__main__':
    main()
