import gzip,hashlib,json,os,struct,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from check_save_core_packed_pointer_windows32_20261031 import CLANG_SHA,LINKER_SHA,DLLTOOL_SHA
REPORT='evidence/application/save-core-pop-index-abi-source-20261031.json'
RUNNER='ports/windows-native/pop_index_abi_runner_20261031.c'
PROFILE='evidence/lanes/save-core/pop-index-abi-profile-20261031.json'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    from match_mechanics_save_20261029_record33 import verify_inputs
    verify_inputs();r=json.loads((ROOT/REPORT).read_text());profiles=json.loads((ROOT/PROFILE).read_text())['rows'];vectors=json.loads(gzip.decompress((ROOT/r['vectorSidecar']['path']).read_bytes()));assert len(vectors)==2480 and r['counts']['netNewBytes']==0;golden={}
    def memory(v,address,size,before=False):
        for key,raw in v['blocksBefore' if before else 'blocksAfter'].items():
            start=int(key,0);data=bytes.fromhex(raw)
            if start<=address and address+size<=start+len(data):return int.from_bytes(data[address-start:address-start+size],'little')
        raise AssertionError(('Golden field absent',hex(address)))
    for v in vectors:
        p=v['profile'];entry=v['entry'];which=0 if entry==0x020CD5BC else 1;state=0x021D6840 if which==0 else 0x021D64CC;desc=0x02102A18+12*p['index'];handle=memory(v,desc,4,True);asset=memory(v,handle+4,4,True);key=(which,p['index'],p['category'],p['lowerResult']);row=[which,p['index']&0xFFFFFFFF,p['category'],p['lowerResult'],v['returnWord'],memory(v,state+4,4),memory(v,state+8,4),memory(v,desc+6,1),memory(v,asset+0x1E,1,True),memory(v,asset+0x1F,1,True),memory(v,asset+0x5C,1,True),sum(e['entry']==0x02045DC4 for e in v['providers'])];assert key not in golden or golden[key]==row;golden[key]=row
    rows=[golden[key] for key in sorted(golden)];assert len(rows)==1140;payload=struct.pack('<II',0x4A32504F,len(rows))+b''.join(struct.pack('<12I',*row) for row in rows);digest=2166136261
    for row in rows:
        for value in [row[4],row[5],row[6],row[7],row[11],1]:
            for byte in struct.pack('<I',value):digest=((digest^byte)*16777619)&0xFFFFFFFF
    toolroot=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin';clang=toolroot/'clang.exe';linker=toolroot/'ld.lld.exe';dlltool=toolroot/'llvm-dlltool.exe';assert [sha(p) for p in (clang,linker,dlltool)]==[CLANG_SHA,LINKER_SHA,DLLTOOL_SHA];tools=json.loads((ROOT/'evidence/verification/packed-pointer-abi-host-tools-20261031.json').read_text());assert all(sha(ROOT/p['path'])==p['sha256'] for p in tools['files'])
    for p in profiles:assert sha(ROOT/p['source'])==p['sourceSha256'] and sha(ROOT/p['replacesPrimary']['source'])==p['replacesPrimary']['sourceSha256']
    work=ROOT/'work/save-core-lane/20261031-pop-index-abi-windows32';work.mkdir(parents=True,exist_ok=True);(work/'golden.bin').write_bytes(payload);definition=work/'kernel32.def';definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nExitProcess@4\nGetStdHandle@4\nReadFile@20\nWriteFile@20\n');sources=[p['source'] for p in profiles];family=work/'family.c';family.write_text('\n'.join('#include "'+(ROOT/source).as_posix()+'"' for source in sources)+'\n')
    environment={k:v for k,v in os.environ.items() if k not in {'CPATH','C_INCLUDE_PATH','CPLUS_INCLUDE_PATH','OBJC_INCLUDE_PATH','LIBRARY_PATH','INCLUDE','LIB','SDKROOT','CFLAGS','CPPFLAGS','LDFLAGS'}};steps=[]
    def run(command,data=None,success=True):
        args=list(map(str,command));result=subprocess.run(args,cwd=ROOT,env=environment,capture_output=True,input=data,timeout=120,creationflags=subprocess.CREATE_NO_WINDOW);steps.append(dict(command=args,exitCode=result.returncode,stdoutSha256=hashlib.sha256(result.stdout).hexdigest(),stderr=result.stderr.decode(errors='replace')));assert (result.returncode==0) if success else (result.returncode!=0),steps[-1];return result
    flags=['--target=i686-pc-windows-msvc','-std=c11','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-fno-strict-aliasing'];run([dlltool,'-m','i386','-k','-d',definition,'-l',work/'kernel32.lib']);run([clang,*flags,'-c',family,'-o',work/'family.obj']);run([clang,*flags,'-c',ROOT/RUNNER,'-o',work/'runner.obj']);exe=work/'pop-index-family.exe';run([linker,'-flavor','link','/machine:x86','/subsystem:console','/nodefaultlib','/entry:j2p_entry','/safeseh:no','/fixed','/dynamicbase:no','/timestamp:0','/manifest:embed',"/manifestuac:level='asInvoker' uiAccess='false'",'/out:'+str(exe),work/'family.obj',work/'runner.obj',work/'kernel32.lib']);raw=exe.read_bytes();pe=struct.unpack_from('<I',raw,0x3C)[0];assert raw[pe:pe+4]==b'PE\0\0' and struct.unpack_from('<H',raw,pe+4)[0]==0x14C and struct.unpack_from('<H',raw,pe+24)[0]==0x10B and b'asInvoker' in raw
    result=run([exe],payload);receipt=struct.unpack('<8I',result.stdout);assert receipt==(0x4A325049,1,1140,1140,0,digest,4,0),receipt;api=work/'expected-api.h';api.write_text('typedef unsigned int u32;\ntypedef signed int s32;\nextern u32 native_fn_02049ad0(s32);\n'+''.join(f'extern u32 native_main_{int(p["address"],0):08x}(s32);\n' for p in profiles));negatives=[]
    for p in profiles:
        old=p['replacesPrimary'];result=run([clang,*flags,'-include',api,'-c',ROOT/old['source'],'-o',work/'legacy-contract.obj'],success=False);assert b'conflicting types' in result.stderr or b'too few arguments' in result.stderr;negatives.append(dict(source=old['source'],sourceSha256=old['sourceSha256'],exitCode=result.returncode,stderrSha256=hashlib.sha256(result.stderr).hexdigest()))
    out=dict(schemaVersion=1,sourceCredit=0,newFunctions=0,newExecutableBytes=0,actualWindowsPublicReturns=1140,failures=0,pointerBytes=4,receipt=list(receipt),nativeCaseDigest=r['nativeCaseDigest'],syntheticGoldenSha256=hashlib.sha256(payload).hexdigest(),oldInterfaceCompileRejections=negatives,sources=[dict(path=p,sha256=sha(ROOT/p)) for p in sources],runner=dict(path=RUNNER,sha256=sha(ROOT/RUNNER)),generatorSha256=sha(__file__),tools=dict(clang=CLANG_SHA,linker=LINKER_SHA,dlltool=DLLTOOL_SHA),executable=dict(path=exe.relative_to(ROOT).as_posix(),sha256=sha(exe),bytes=exe.stat().st_size),steps=steps,limitations=['Actual hidden Windows PE32 process executes the two ordinary-C typed alternatives with modeled lower lookup,category/UI/free boundaries. Native ARM results supply normalized expected capacity/count/tag and return effects for1140 unique contexts. No original executable or game inputs enter the Windows process.','All256 signed-byte indices and extra128/255 inputs are exercised,with independent category/lower-return axes. The three supplied lower contracts can deliberately explore unreachable native combinations and do not establish original scene feasibility. Modeled descriptor storage includes all384 indices;unselected pointers,tags and neighboring bytes are checked.','Two historical void/inputless interfaces fail against the explicit signed-index API at compile time. Their original ARM bytes remain unchanged and can work via register retention;no old native binary failure is fabricated.','This is a32-bit C subset,not a Windows game,Android execution,64-bit portability,actual UI/deallocation or native bank/save interpretation. Root owns adoption.']);target=ROOT/'evidence/portability/save-core-pop-index-abi-windows32-20261031.json';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(out,indent=2)+'\n');verify_inputs();print(dict(actualWindowsPublicReturns=1140,oldInterfaceCompileRejections=2,reportSha256=sha(target)))


if __name__=='__main__':main()
