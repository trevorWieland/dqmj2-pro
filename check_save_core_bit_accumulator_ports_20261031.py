import gzip,hashlib,json,os,struct,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]
from check_save_core_packed_pointer_windows32_20261031 import CLANG_SHA,LINKER_SHA,DLLTOOL_SHA
from elftools.elf.elffile import ELFFile
from match_mechanics_save_20261029_record33 import verify_inputs
RUNNER='ports/windows-native/bit_accumulator_runner_20261031.c'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    verify_inputs();report=json.loads((ROOT/'evidence/application/save-core-bit-accumulator-source-20261031.json').read_text());profile=json.loads((ROOT/'evidence/lanes/save-core/bit-accumulator-profile-20261031.json').read_text())['rows'][0];vectors=json.loads(gzip.decompress((ROOT/report['vectorSidecar']['path']).read_bytes()));assert len(vectors)==1536;payload=struct.pack('<II',0x4A324241,1536);digest=2166136261
    for v in vectors:
        assert v['actualReturn'] and v['dataMemoryAccesses']==0;payload+=struct.pack('<II',v['word'],v['returnWord'])
        for value in (v['word'],v['returnWord']):
            for byte in struct.pack('<I',value):digest=((digest^byte)*16777619)&0xFFFFFFFF
    toolroot=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin';clang=toolroot/'clang.exe';linker=toolroot/'ld.lld.exe';dlltool=toolroot/'llvm-dlltool.exe';assert [sha(p) for p in (clang,linker,dlltool)]==[CLANG_SHA,LINKER_SHA,DLLTOOL_SHA];tools=json.loads((ROOT/'evidence/verification/packed-pointer-abi-host-tools-20261031.json').read_text());assert all(sha(ROOT/p['path'])==p['sha256'] for p in tools['files']);assert sha(ROOT/profile['source'])==profile['sourceSha256']
    work=ROOT/'work/scba96/ports';work.mkdir(parents=True,exist_ok=True);definition=work/'kernel32.def';definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nExitProcess@4\nGetStdHandle@4\nReadFile@20\nWriteFile@20\n');environment={k:v for k,v in os.environ.items() if k not in {'CPATH','C_INCLUDE_PATH','CPLUS_INCLUDE_PATH','OBJC_INCLUDE_PATH','LIBRARY_PATH','INCLUDE','LIB','SDKROOT','CFLAGS','CPPFLAGS','LDFLAGS'}};steps=[]
    def run(command,data=None):
        args=list(map(str,command));result=subprocess.run(args,cwd=ROOT,env=environment,capture_output=True,input=data,timeout=120,creationflags=subprocess.CREATE_NO_WINDOW);steps.append(dict(command=args,exitCode=result.returncode,stdoutSha256=hashlib.sha256(result.stdout).hexdigest(),stderr=result.stderr.decode(errors='replace')));assert result.returncode==0,steps[-1];return result
    flags=['--target=i686-pc-windows-msvc','-std=c11','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-fno-strict-aliasing'];run([dlltool,'-m','i386','-k','-d',definition,'-l',work/'kernel32.lib']);run([clang,*flags,'-c',ROOT/profile['source'],'-o',work/'accumulator.obj']);run([clang,*flags,'-c',ROOT/RUNNER,'-o',work/'runner.obj']);exe=work/'bit-accumulator.exe';run([linker,'-flavor','link','/machine:x86','/subsystem:console','/nodefaultlib','/entry:j2p_entry','/safeseh:no','/fixed','/dynamicbase:no','/timestamp:0','/manifest:embed',"/manifestuac:level='asInvoker' uiAccess='false'",'/out:'+str(exe),work/'accumulator.obj',work/'runner.obj',work/'kernel32.lib']);raw=exe.read_bytes();pe=struct.unpack_from('<I',raw,0x3C)[0];assert raw[pe:pe+4]==b'PE\0\0' and struct.unpack_from('<H',raw,pe+4)[0]==0x14C and struct.unpack_from('<H',raw,pe+24)[0]==0x10B and b'asInvoker' in raw
    receipt=struct.unpack('<8I',run([exe],payload).stdout);assert receipt==(0x4A324257,1,1536,1536,0,digest,4,0),receipt
    obj=work/'accumulator-arm64.o';library=work/'libj2p_bit_accumulator.so';run([clang,'--target=aarch64-linux-android23','-std=c11','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-fno-strict-aliasing','-fPIC','-c',ROOT/profile['source'],'-o',obj]);run([linker,'-shared','--build-id=none','-soname','libj2p_bit_accumulator.so','-o',library,obj])
    with library.open('rb') as stream:
        elf=ELFFile(stream);assert elf.elfclass==64 and elf['e_machine']=='EM_AARCH64';symbol=elf.get_section_by_name('.dynsym').get_symbol_by_name(profile['name']);assert len(symbol)==1 and symbol[0]['st_info']['type']=='STT_FUNC';assert not [s.name for s in elf.get_section_by_name('.dynsym').iter_symbols() if s.name and s['st_shndx']=='SHN_UNDEF']
    out=dict(schemaVersion=1,sourceCredit=0,actualWindowsPublicReturns=1536,androidExecutions=0,failures=0,pointerBytes=4,receipt=list(receipt),nativeCaseDigest=report['nativeCaseDigest'],syntheticGoldenSha256=hashlib.sha256(payload).hexdigest(),source=dict(path=profile['source'],sha256=sha(ROOT/profile['source'])),runner=dict(path=RUNNER,sha256=sha(ROOT/RUNNER)),generatorSha256=sha(__file__),tools=dict(clang=CLANG_SHA,linker=LINKER_SHA,dlltool=DLLTOOL_SHA),executable=dict(path=exe.relative_to(ROOT).as_posix(),sha256=sha(exe),bytes=exe.stat().st_size),androidBuild=dict(path=library.relative_to(ROOT).as_posix(),sha256=sha(library),bytes=library.stat().st_size,machine='EM_AARCH64',exportedFunction=profile['name'],undefinedSymbols=0,actualExecutions=0),steps=steps,limitations=['Actual hidden Windows PE32 executes this recovered ordinary-C pure function1536 times against original native return words. No function/game providers or executable blobs enter the Windows process. This supports only the finite word corpus,not whole-game portability.','The same source builds a freestanding ARM64 Android23 shared object with one exported function and no undefined symbols. Android execution count is0;ABI/device/runtime behavior and whole-game operation are not inferred. No original format/scene/meaning label follows.']);path=ROOT/'evidence/portability/save-core-bit-accumulator-ports-20261031.json';path.write_text(json.dumps(out,indent=2)+'\n');verify_inputs();print(dict(actualWindowsPublicReturns=1536,androidExecutions=0,reportSha256=sha(path)))


if __name__=='__main__':main()
