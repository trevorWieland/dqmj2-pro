import ctypes
import gzip
import hashlib
import json
import struct
import subprocess
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from main_animation_obj352_fixture_20261101 import inputs,DATA,SPECS
from match_main_animation_obj352_20261101 import COUNTS

CLANG_SHA='6b7a698ccd1d5ef7375b7733f0675a166c560112961d3e5df0f275565a9201bc'
LINKER_SHA='b64100b407a472f831caf2789f6c09d501e2e4c876ebc772997c294be7f9f8f3'
WORK=ROOT/'work/main-animation-obj352-windows-20261101'
REPORT=ROOT/'evidence/ports/main-animation-obj352-windows-20261101.json'


def compile_sources(sources,label):
    tools=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    clang,linker=tools/'clang.exe',tools/'ld.lld.exe';assert sha256(clang)==CLANG_SHA and sha256(linker)==LINKER_SHA
    folder=WORK/label;folder.mkdir(parents=True,exist_ok=True);objects=[];records=[];commands=[]
    for index,name in enumerate([*sources,'src/ports/20261101_animation_obj352/dispatch.c']):
        path=ROOT/name;obj=folder/f'source-{index}.obj'
        command=[str(clang),'--driver-mode=cl','--target=x86_64-pc-windows-msvc','/TC','/std:c11','/O2','/Brepro','/GS-',
         '/clang:-ffreestanding','/clang:-fno-builtin','/clang:-fno-stack-protector','/clang:-fno-strict-aliasing','/w','/c',str(path),'/Fo'+str(obj)]
        if index==2:command.append('/Dnative_main_0202c054=native_fn_0202c054')
        run=subprocess.run(command,cwd=ROOT,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);assert run.returncode==0,run.stdout+run.stderr
        assert struct.unpack_from('<I',obj.read_bytes(),4)[0]==0
        objects.append(obj);commands.append(command);records.append(dict(source=name,sourceSha256=sha256(path),objectSha256=sha256(obj),objectTimeDateStamp=0))
    dll=folder/'animation_obj352.dll'
    command=[str(linker),'-flavor','link','/dll','/noentry','/machine:x64','/nodefaultlib','/timestamp:0','/out:'+str(dll),*[str(p)for p in objects]]
    run=subprocess.run(command,cwd=ROOT,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);assert run.returncode==0,run.stdout+run.stderr
    commands.append(command)
    return dict(sources=records,commands=commands,binary=dll.relative_to(ROOT).as_posix(),binarySha256=sha256(dll))


def execute_child(label):
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.VirtualAlloc.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_uint32,ctypes.c_uint32];kernel.VirtualAlloc.restype=ctypes.c_void_p
    kernel.VirtualFree.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_uint32];kernel.VirtualFree.restype=ctypes.c_int
    allocation=kernel.VirtualAlloc(DATA,65536,0x3000,4);assert allocation==DATA,ctypes.get_last_error()
    try:
        dll=ctypes.CDLL(str(WORK/label/'animation_obj352.dll'));dll.j2p_run.argtypes=[ctypes.c_uint32]*4;dll.j2p_run.restype=ctypes.c_uint32
        rows=[];rejected=0;native=read_json(ROOT/'evidence/matches/main-animation-obj352-20261101.json')
        for entry,count in COUNTS.items():
            pin=next(item for item in native['replayDependencies']if f'{entry:08x}'in item['path']);path=ROOT/pin['path'];assert sha256(path)==pin['sha256']
            cases=json.loads(gzip.decompress(path.read_bytes()))['cases'];assert len(cases)==count
            for case in cases:
                page,args,expected,context=inputs(entry,case['index']);assert context==case['context']and expected==case['rawR0']
                ctypes.memmove(DATA,bytes(page),65536);result=dll.j2p_run(entry,*(args+[0]*(3-len(args))))
                assert ctypes.string_at(DATA,65536)==page
                rejected+=result!=expected;rows.append(dict(address=f'0x{entry:08X}',index=case['index'],rawR0=result))
        output=dict(label=label,actualPublicReturns=len(rows),rejected=rejected,
         caseSha256=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest())
        write_json(WORK/label/'execution.json',output)
    finally:
        assert kernel.VirtualFree(DATA,0,0x8000)


def main():
    assert sys.platform=='win32'and ctypes.sizeof(ctypes.c_void_p)==8
    if len(sys.argv)>1:execute_child(sys.argv[1]);return
    native=read_json(ROOT/'evidence/matches/main-animation-obj352-20261101.json');sources=[]
    for row in native['matches']:
        assert sha256(ROOT/row['source'])==row['sourceSha256'];sources.append(row['source'])
    results=[]
    for label,source_index in [('preferred',None),('wrong-animation-offset',0),('wrong-frame-equality',1),('wrong-dictionary-bound',2),('wrong-sprite-width',3)]:
        selected=list(sources)
        if source_index is not None:
            address=list(SPECS)[source_index];path=WORK/f'wrong-{address:08x}.c'
            text=(ROOT/selected[source_index]).read_text(encoding='utf-8')
            mutations={0x0202BF2C:('anmSetData->offset','anmSetData->offset + 4'),0x0202BFE0:('<= frame','< frame'),
             0x0202C054:('idx < dict->numEntry','idx <= dict->numEntry'),0x020364DC:('w / 8','w / 4')}
            old,new=mutations[address];changed=text.replace(old,new);assert changed!=text
            path.write_text(changed,encoding='utf-8');selected[source_index]=path.relative_to(ROOT).as_posix()
        built=compile_sources(selected,label)
        command=[sys.executable,str(Path(__file__).resolve()),label]
        run=subprocess.run(command,cwd=ROOT.parent,capture_output=True,timeout=90,creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,run.stdout+run.stderr
        execution=read_json(WORK/label/'execution.json');assert (execution['rejected']==0)==(source_index is None)
        results.append(dict(build=built,execution=execution,command=command))
    output=dict(passed=True,sourceCredit=0,host='Windows',architecture='x86_64',compilerSha256=CLANG_SHA,linkerSha256=LINKER_SHA,
     sourceBuild=results[0]['build'],actualPublicReturns=sum(COUNTS.values()),actualWrongPublicReturns=sum(COUNTS.values())*4,
     totalActualPublicReturns=sum(COUNTS.values())*5,windowsCaseSha256=results[0]['execution']['caseSha256'],controls=results[1:],
     nativeReportSha256=sha256(ROOT/'evidence/matches/main-animation-obj352-20261101.json'),
     unmodifiedCandidateSourcesCompiled=True,functionNamesAliasedOnly=['native_main_0202c054=native_fn_0202c054'],
     fixedGuestDataMapping='0x02400000..0x0240FFFF, private disposable child process, VirtualFree verified',
     fullGameExecuted=False,androidDeviceExecutions=0,reproductionCommand='python check_main_animation_obj352_windows_20261101.py')
    write_json(REPORT,output);print(dict(publicReturns=output['actualPublicReturns'],wrongPublicReturns=output['actualWrongPublicReturns'],wrongRejected=sum(r['execution']['rejected']for r in results[1:])))


if __name__=='__main__':
    main()
