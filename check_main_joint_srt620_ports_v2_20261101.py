import ctypes
import gzip
import hashlib
import json
import struct
import subprocess
import sys
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,read_json,write_json,sha256

CLANG_SHA="6b7a698ccd1d5ef7375b7733f0675a166c560112961d3e5df0f275565a9201bc"
LINKER_SHA="b64100b407a472f831caf2789f6c09d501e2e4c876ebc772997c294be7f9f8f3"
ENTRIES=[0x0202C6CC,0x0202C788,0x0202CF80]
WORK=ROOT/"work/main-joint-srt620-ports-v2-20261101"
COLLECTOR="src/ports/20261101_joint_srt620/collector.c"


def invoke(command):
    run=subprocess.run(command,cwd=ROOT,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    assert run.returncode==0,run.stdout+run.stderr
    return dict(command=command,exitCode=run.returncode,stderr=run.stderr.decode(errors="replace"))


def source_paths(wrong=False):
    paths=[]
    for entry in ENTRIES:
        source=ROOT/f"src/runtime/20261101_joint_srt620/native_main_{entry:08x}.c"
        if wrong:
            text=source.read_text(encoding="utf-8")
            text=text.replace(">> 12",">> 11")if entry==0x0202CF80 else text.replace("0x1b ,","0x1c ,")
            target=WORK/f"wrong-{entry:08x}.c";target.write_text(text,encoding="utf-8");source=target
        paths.append(source)
    return [*paths,ROOT/COLLECTOR]


def compile_windows(paths,label,clang,linker):
    folder=WORK/label;folder.mkdir(parents=True,exist_ok=True);objects=[];steps=[]
    for index,path in enumerate(paths):
        obj=folder/f"source-{index}.obj"
        command=[str(clang),"--driver-mode=cl","--target=x86_64-pc-windows-msvc","/TC","/std:c11","/O2","/Brepro","/GS-","/w",
         "/clang:-ffreestanding","/clang:-fno-builtin","/clang:-fno-stack-protector","/clang:-fno-strict-aliasing","/c",str(path),"/Fo"+str(obj)]
        steps.append(invoke(command));assert struct.unpack_from("<I",obj.read_bytes(),4)[0]==0;objects.append(obj)
    dll=folder/"joint_srt.dll";steps.append(invoke([str(linker),"-flavor","link","/dll","/noentry","/machine:x64","/nodefaultlib","/timestamp:0","/out:"+str(dll),*[str(o)for o in objects]]))
    module=ctypes.CDLL(str(dll));function=module.j2p_joint_run
    function.argtypes=[ctypes.c_uint32,ctypes.POINTER(ctypes.c_uint32),ctypes.POINTER(ctypes.c_uint32)];function.restype=ctypes.c_uint32
    proof=dict(sources=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in paths],
     objectHashes=[sha256(o)for o in objects],objectTimeDateStamps=[0]*len(objects),binary=dll.relative_to(ROOT).as_posix(),binarySha256=sha256(dll),steps=steps)
    return module,function,proof


def execute(function,variant,words):
    values=(ctypes.c_uint32*22)(*words);before=bytes(values);output=(ctypes.c_uint32*64)()
    length=function(variant,values,output);assert length<=64 and bytes(values)==before
    return list(output[:length])


def main():
    assert sys.platform=="win32"and ctypes.sizeof(ctypes.c_void_p)==8
    WORK.mkdir(parents=True,exist_ok=True);tools=ROOT/"tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin"
    clang,linker=tools/"clang.exe",tools/"ld.lld.exe";assert sha256(clang)==CLANG_SHA and sha256(linker)==LINKER_SHA
    report=read_json(ROOT/"evidence/matches/main-joint-srt620-20261101.json");paths=source_paths()
    module,function,proof=compile_windows(paths,"preferred",clang,linker)
    native=[];results=[]
    for variant,trace in enumerate(report["replayDependencies"]):
        path=ROOT/trace["path"];assert sha256(path)==trace["sha256"]
        cases=json.loads(gzip.decompress(path.read_bytes()))["cases"]
        for case in cases:
            expected=[word for op,payload in case["commands"]for word in[op,len(payload),*payload]]
            output=execute(function,variant,case["inputWords"]);assert output==expected,(variant,case["index"])
            native.append([variant,case["index"],case["inputWords"],expected]);results.append(output)
    wrong,wrong_function,wrong_proof=compile_windows(source_paths(True),"wrong",clang,linker)
    controls=[dict(variant=i,actualReturningWrongCExecutions=0,rejected=0,positiveControls=0)for i in range(3)]
    for item,expected in zip(native,results):
        variant,index,words,unused=item;output=execute(wrong_function,variant,words);row=controls[variant]
        row["actualReturningWrongCExecutions"]+=1;row["rejected"]+=output!=expected;row["positiveControls"]+=output==expected
    assert len(native)==2304 and all(c["rejected"]>0 for c in controls)
    android=WORK/"android-arm64";android.mkdir(parents=True,exist_ok=True);library=android/"libj2p_joint_srt.so"
    command=[str(clang),"--target=aarch64-linux-android26","-std=c11","-O2","-ffreestanding","-fno-builtin","-fno-stack-protector",
     "-fno-strict-aliasing","-fPIC","-fvisibility=hidden","-shared","-nostdlib","-Wl,--build-id=none",*[str(p)for p in paths],"-o",str(library)]
    cross=invoke(command)
    with library.open("rb")as stream:
        elf=ELFFile(stream);assert elf["e_machine"]=="EM_AARCH64"and elf["e_type"]=="ET_DYN"
        symbols=list(elf.get_section_by_name(".dynsym").iter_symbols())
        assert any(s.name=="j2p_joint_run"and s["st_shndx"]!="SHN_UNDEF"for s in symbols)
        undefined=[s.name for s in symbols if s.name and s["st_shndx"]=="SHN_UNDEF"];assert not undefined,undefined
    result=dict(passed=True,sourceCredit=0,compilerSha256=CLANG_SHA,linkerSha256=LINKER_SHA,windows=proof,wrongWindows=wrong_proof,
     windowsActualPublicReturns=2304,windowsActualWrongCReturns=2304,controls=controls,
     windowsCaseSha256=hashlib.sha256(json.dumps(results,separators=(",",":")).encode()).hexdigest(),
     nativeVectorSha256=hashlib.sha256(json.dumps(native,separators=(",",":")).encode()).hexdigest(),
     android=dict(target="aarch64-linux-android26",compiledAndLinked=True,elfMachine="EM_AARCH64",elfType="ET_DYN",undefinedSymbols=undefined,
      binary=library.relative_to(ROOT).as_posix(),binarySha256=sha256(library),step=cross,deviceExecutions=0),
     commandBufferCollectorProvided=True,physicalGpu=False,fullGame=False,reproductionCommand="python check_main_joint_srt620_ports_v2_20261101.py")
    write_json(ROOT/"evidence/ports/main-joint-srt620-windows-android-20261101.json",result)
    print(dict(windowsReturns=2304,returningWrongC=2304,wrongRejected=sum(c["rejected"]for c in controls),androidSharedLibrary=True,deviceExecutions=0))


if __name__=="__main__":
    main()
