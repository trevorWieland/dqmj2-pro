import gzip,hashlib,json,os,struct,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
CLANG_SHA='6b7a698ccd1d5ef7375b7733f0675a166c560112961d3e5df0f275565a9201bc'
LINKER_SHA='b64100b407a472f831caf2789f6c09d501e2e4c876ebc772997c294be7f9f8f3'
DLLTOOL_SHA='d2f0d02b4ae109d2801f83506c329c1ca0e36d52919b273eaffb915c8cd095d1'
REPORT='evidence/application/save-core-packed-pointer-abi-source-20261031.json'
RUNNER='ports/windows-native/packed_pointer_abi_runner_20261031.c'
PROFILE='evidence/lanes/save-core/packed-pointer-abi-profile-20261031.json'
LEAF='src/runtime/thumb-runtime02/native_main_02096ce8.c'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    from match_mechanics_save_20261029_record33 import verify_inputs
    verify_inputs();r=json.loads((ROOT/REPORT).read_text());profiles=json.loads((ROOT/PROFILE).read_text())['rows'];vectors=json.loads(gzip.decompress((ROOT/r['vectorSidecar']['path']).read_bytes()));assert len(vectors)==768 and r['counts']['sourceCredit']==0
    entries=[int(p['address'],0) for p in profiles];golden=[[None]*6 for _ in range(32)]
    for v in vectors:
        helper=entries.index(int(v['helper'],0));flags=(v['native']['profile']['word']>>11)&31;result=v['native']['returnWord']>>8
        assert golden[flags][helper] in (None,result);golden[flags][helper]=result
    assert all(all(value is not None for value in row) for row in golden);payload=struct.pack('<II',0x4A325047,32)+b''.join(struct.pack('<6I',*row) for row in golden);digest=2166136261
    for index in range(64):
        for flags in range(32):
            for result in golden[flags]:
                for byte in struct.pack('<I',result):digest=((digest^byte)*16777619)&0xFFFFFFFF
    toolroot=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin';clang=toolroot/'clang.exe';linker=toolroot/'ld.lld.exe';dlltool=toolroot/'llvm-dlltool.exe';assert [sha(p) for p in (clang,linker,dlltool)]==[CLANG_SHA,LINKER_SHA,DLLTOOL_SHA]
    tools=json.loads((ROOT/'evidence/verification/packed-pointer-abi-host-tools-20261031.json').read_text());assert all(sha(ROOT/p['path'])==p['sha256'] for p in tools['files']);assert sha(ROOT/LEAF)=='545c4e66f269a75a0b3a74652ed8b74e9965c44c9846571dc5cf09b8de301516'
    for p in profiles:assert sha(ROOT/p['source'])==p['sourceSha256'] and sha(ROOT/p['expectedPrimarySource'])==p['expectedPrimarySourceSha256']
    work=ROOT/'work/save-core-lane/20261031-packed-pointer-abi-windows32';work.mkdir(parents=True,exist_ok=True);(work/'golden.bin').write_bytes(payload);definition=work/'kernel32.def';definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nExitProcess@4\nGetStdHandle@4\nReadFile@20\nWriteFile@20\n')
    sources=[LEAF]+[p['source'] for p in profiles];aliases=[f'-Dnative_fn_{entry:08x}=native_main_{entry:08x}' for entry in [0x02096CE8]+entries];family=work/'family.c';family.write_text('\n'.join('#include "'+(ROOT/source).as_posix()+'"' for source in sources)+'\n')
    environment={k:v for k,v in os.environ.items() if k not in {'CPATH','C_INCLUDE_PATH','CPLUS_INCLUDE_PATH','OBJC_INCLUDE_PATH','LIBRARY_PATH','INCLUDE','LIB','SDKROOT','CFLAGS','CPPFLAGS','LDFLAGS'}};steps=[]
    def run(command,data=None,success=True):
        args=list(map(str,command));result=subprocess.run(args,cwd=ROOT,env=environment,capture_output=True,input=data,timeout=120,creationflags=subprocess.CREATE_NO_WINDOW);steps.append(dict(command=args,exitCode=result.returncode,stdoutSha256=hashlib.sha256(result.stdout).hexdigest(),stderr=result.stderr.decode(errors='replace')))
        assert (result.returncode==0) if success else (result.returncode!=0),steps[-1];return result
    flags=['--target=i686-pc-windows-msvc','-std=c11','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-fno-strict-aliasing']
    run([dlltool,'-m','i386','-k','-d',definition,'-l',work/'kernel32.lib']);run([clang,*flags,*aliases,'-c',family,'-o',work/'family.obj']);run([clang,*flags,'-c',ROOT/RUNNER,'-o',work/'runner.obj']);exe=work/'packed-pointer-family.exe'
    run([linker,'-flavor','link','/machine:x86','/subsystem:console','/nodefaultlib','/entry:j2p_entry','/safeseh:no','/fixed','/dynamicbase:no','/timestamp:0','/manifest:embed',"/manifestuac:level='asInvoker' uiAccess='false'",'/out:'+str(exe),work/'family.obj',work/'runner.obj',work/'kernel32.lib'])
    raw=exe.read_bytes();pe=struct.unpack_from('<I',raw,0x3C)[0];assert raw[pe:pe+4]==b'PE\0\0' and struct.unpack_from('<H',raw,pe+4)[0]==0x14C and struct.unpack_from('<H',raw,pe+24)[0]==0x10B and b'asInvoker' in raw
    result=run([exe],payload);receipt=struct.unpack('<8I',result.stdout);assert receipt==(0x4A325041,4,64,32,12288,0,digest,0),receipt
    api=work/'expected-api.h';api.write_text('typedef unsigned int u32;\n'+''.join(f'extern u32 native_main_{entry:08x}(u32 *record);\n' for entry in [0x02096CE8]+entries)+''.join(f'extern u32 native_fn_{entry:08x}(u32 *record);\n' for entry in [0x02096CE8]+entries))
    negatives=[]
    for p in profiles:
        result=run([clang,*flags,'-include',api,'-c',ROOT/p['expectedPrimarySource'],'-o',work/'legacy-contract.obj'],success=False);assert b'conflicting types' in result.stderr or b'too few arguments' in result.stderr;negatives.append(dict(source=p['expectedPrimarySource'],sourceSha256=p['expectedPrimarySourceSha256'],exitCode=result.returncode,stderrSha256=hashlib.sha256(result.stderr).hexdigest()))
    out=dict(schemaVersion=1,sourceCredit=0,newFunctions=0,newExecutableBytes=0,actualWindowsPublicReturns=12288,failures=0,pointerBytes=4,receipt=list(receipt),nativeCaseDigest=r['nativeCaseDigest'],syntheticGoldenSha256=hashlib.sha256(payload).hexdigest(),oldInterfaceCompileRejections=negatives,sources=[dict(path=source,sha256=sha(ROOT/source)) for source in sources],runner=dict(path=RUNNER,sha256=sha(ROOT/RUNNER)),generatorSha256=sha(__file__),tools=dict(clang=CLANG_SHA,linker=LINKER_SHA,dlltool=DLLTOOL_SHA),executable=dict(path=exe.relative_to(ROOT).as_posix(),sha256=sha(exe),bytes=exe.stat().st_size),steps=steps,limitations=['Actual hidden Win32 process;seven ordinary-C functions,including existingCE8,with no original executable code mapped. The six typed source alternatives remain zero-coverage migrations.','The stdin corpus is synthetic and derived from actual ARM/Thumb original results;no ROM/save/assets are loaded by the Windows program. All64 array positions and32 field states exercise6 public C APIs with unchanged neighbor words.','Six old C interfaces are rejected against measured pointer prototypes at compile time. Their old ARM bytes are retained and may still work through incidental register retention;no fabricated old-binary Unicorn failure is claimed.','This is a small C subset,not a Windows game,ordinary scene,save persistence,Android execution or64-bit host claim. Root owns source preference adoption.'])
    target=ROOT/'evidence/portability/save-core-packed-pointer-abi-windows32-20261031.json';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(out,indent=2)+'\n');verify_inputs();print(dict(actualWindowsPublicReturns=12288,oldInterfaceCompileRejections=len(negatives),reportSha256=sha(target)))


if __name__=='__main__':main()
