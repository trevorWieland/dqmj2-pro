import ctypes
import gzip
import hashlib
import json
import struct
import subprocess
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from main_rng_scene_fixture_20261101 import inputs

CLANG_SHA="6b7a698ccd1d5ef7375b7733f0675a166c560112961d3e5df0f275565a9201bc"
LINKER_SHA="b64100b407a472f831caf2789f6c09d501e2e4c876ebc772997c294be7f9f8f3"
SOURCES=[("src/runtime/main-scalars01/native_main_0203d2ec_db8ce10bfe68.c","0203d2ec"),
 ("src/runtime/runtime08/native_main_020443ec.c","020443ec"),
 ("src/runtime/runtime08/native_main_02044508.c","02044508"),
 ("src/runtime/runtime08/native_main_0204457c.c","0204457c"),
 ("src/ports/20261101_rng_scene/harness.c",None)]


def compile_source(source,label):
    tools=ROOT/"tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin"
    clang,linker=tools/"clang.exe",tools/"ld.lld.exe"
    assert sha256(clang)==CLANG_SHA and sha256(linker)==LINKER_SHA
    folder=ROOT/"work/main-rng-scene-windows-20261101"/label;folder.mkdir(parents=True,exist_ok=True)
    objects=[];records=[];commands=[]
    for index,(name,alias)in enumerate([(source,None),*SOURCES]):
        path=ROOT/name;obj=folder/f"source-{index}.obj"
        command=[str(clang),"--driver-mode=cl","--target=x86_64-pc-windows-msvc","/TC","/std:c11","/O2","/Brepro",
         "/clang:-ffreestanding","/clang:-fno-builtin","/clang:-fno-stack-protector","/clang:-fno-strict-aliasing","/w",
         "/c",str(path),"/Fo"+str(obj)]
        if alias:command.append("/Dnative_main_"+alias+"=native_fn_"+alias)
        run=subprocess.run(command,cwd=ROOT,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,run.stdout+run.stderr
        assert struct.unpack_from("<I",obj.read_bytes(),4)[0]==0
        objects.append(obj);commands.append(command);records.append(dict(source=name,sourceSha256=sha256(path),objectSha256=sha256(obj),objectTimeDateStamp=0))
    dll=folder/"rng_scene.dll"
    command=[str(linker),"-flavor","link","/dll","/noentry","/machine:x64","/nodefaultlib","/timestamp:0",
     "/out:"+str(dll),*[str(obj)for obj in objects]]
    run=subprocess.run(command,cwd=ROOT,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    assert run.returncode==0,run.stdout+run.stderr;commands.append(command)
    module=ctypes.CDLL(str(dll));word=ctypes.c_uint32;byte=ctypes.c_ubyte
    module.j2p_prepare.argtypes=[ctypes.POINTER(byte),word,word];module.j2p_prepare.restype=None
    module.j2p_run.argtypes=[];module.j2p_run.restype=word
    module.j2p_state.argtypes=[ctypes.POINTER(byte),ctypes.POINTER(byte),ctypes.POINTER(word),ctypes.POINTER(word),ctypes.POINTER(word)]
    module.j2p_state.restype=None
    return module,dict(sources=records,commands=commands,binary=dll.relative_to(ROOT).as_posix(),binarySha256=sha256(dll))


def execute(module,index):
    frame,seed,mirror,mode,expected=inputs(index)
    raw=(ctypes.c_ubyte*64).from_buffer_copy(frame);module.j2p_prepare(raw,seed,index)
    returned=module.j2p_run();after=(ctypes.c_ubyte*64)();after_seed=(ctypes.c_ubyte*4)()
    ids=(ctypes.c_uint32*8)();args=(ctypes.c_uint32*8)();count=ctypes.c_uint32()
    module.j2p_state(after,after_seed,ids,args,ctypes.byref(count));assert count.value<=8
    calls=[[ids[i],args[i]if ids[i]in[0x022139E8,0x0220268C,0x0220345C]else None]for i in range(count.value)]
    return dict(index=index,rawR0=returned,resultingSeed=int.from_bytes(bytes(after_seed),"little"),resultingFrame=bytes(after).hex(),providedCalls=calls)


def main():
    assert sys.platform=="win32"and ctypes.sizeof(ctypes.c_void_p)==8
    native=read_json(ROOT/"evidence/matches/main-rng-scene-explicit-20261101.json")
    trace=ROOT/native["replayDependencies"][0]["path"];assert sha256(trace)==native["replayDependencies"][0]["sha256"]
    cases=json.loads(gzip.decompress(trace.read_bytes()))["cases"]
    source=native["matches"][0]["source"];assert sha256(ROOT/source)==native["matches"][0]["sourceSha256"]
    module,built=compile_source(source,"preferred");rows=[]
    for case in cases:
        result=execute(module,case["index"])
        expected=dict(index=case["index"],rawR0=case["rawR0"],resultingSeed=case["resultingSeed"],resultingFrame=case["resultingFrame"],
         providedCalls=[[item["target"],item["r0"]]for item in case["providedCalls"]])
        assert result==expected,case["index"];rows.append(result)
    controls=[];text=(ROOT/source).read_text(encoding="utf-8");needle="native_fn_0203d2ec(native_fn_0204457c());"
    for label,replacement in[("wrong-seed","native_fn_0203d2ec(native_fn_0204457c() + 1U);"),("omit-setter","native_fn_0204457c();")]:
        path=ROOT/"work/main-rng-scene-windows-20261101"/(label+".c");path.write_text(text.replace(needle,replacement),encoding="utf-8")
        wrong,proof=compile_source(path.relative_to(ROOT).as_posix(),label);rejected=0
        for index in range(1152):rejected+=execute(wrong,index)!=rows[index]
        assert rejected==132
        controls.append(dict(label=label,actualPublicReturns=1152,rejected=rejected,positiveControls=1152-rejected,build=proof))
    digest=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    output=dict(passed=True,sourceCredit=0,host="Windows",architecture="x86_64",compilerSha256=CLANG_SHA,linkerSha256=LINKER_SHA,
     sourceBuild=built,actualPublicReturns=1152,actualWrongPublicReturns=2304,totalActualPublicReturns=3456,
     windowsCaseSha256=digest,nativeTraceSha256=sha256(trace),controls=controls,
     nativeSelectedHelperSourcesCompiled=True,onlyFunctionNamesAliased=True,explicitOverlayServiceProviders=True,
     fullGameExecuted=False,androidDeviceExecutions=0,reproductionCommand="python check_main_rng_scene_windows_20261101.py")
    write_json(ROOT/"evidence/ports/main-rng-scene-windows-20261101.json",output)
    print(dict(publicReturns=1152,actualControlReturns=2304,wrongRejected=264,windowsCaseSha256=digest))


if __name__=="__main__":
    main()
