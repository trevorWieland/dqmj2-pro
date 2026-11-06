import hashlib,json,os,struct,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CLANG_SHA='6b7a698ccd1d5ef7375b7733f0675a166c560112961d3e5df0f275565a9201bc'
LINKER_SHA='b64100b407a472f831caf2789f6c09d501e2e4c876ebc772997c294be7f9f8f3'
DLLTOOL_SHA='d2f0d02b4ae109d2801f83506c329c1ca0e36d52919b273eaffb915c8cd095d1'
PROFILE='evidence/lanes/save-core/explicit-clear120-profile-20261101.json'
RUNNER='ports/windows-native/explicit_clear120_runner.c'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    candidates=[ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin',ROOT.parents[1]/'dqmj2pro-decomp/tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'];tools=Path(os.environ['J2P_NDK_BIN']) if 'J2P_NDK_BIN' in os.environ else next(p for p in candidates if (p/'clang.exe').exists());clang,linker,dlltool=[tools/n for n in ['clang.exe','ld.lld.exe','llvm-dlltool.exe']];assert [sha(p) for p in (clang,linker,dlltool)]==[CLANG_SHA,LINKER_SHA,DLLTOOL_SHA];work=ROOT/'work/scc120/windows32';work.mkdir(parents=True,exist_ok=True);profile=json.loads((ROOT/PROFILE).read_text());rows=[r for r in profile['rows'] if r['netNewBytes']==0];assert len(rows)==2;steps=[];env={k:v for k,v in os.environ.items() if k not in {'CL','_CL_','CFLAGS','CPPFLAGS','LDFLAGS','LIB','LIBPATH','INCLUDE'}}
    def run(command):
        process=subprocess.run(list(map(str,command)),cwd=ROOT,env=env,capture_output=True,timeout=60,creationflags=subprocess.CREATE_NO_WINDOW);steps.append(dict(command=list(map(str,command)),exitCode=process.returncode,stdoutSha256=hashlib.sha256(process.stdout).hexdigest(),stderr=process.stderr.decode(errors='replace')));assert process.returncode==0,steps[-1];return process
    definition=work/'kernel32.def';definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nExitProcess@4\nGetStdHandle@4\nWriteFile@20\n');run([dlltool,'-m','i386','-k','-d',definition,'-l',work/'kernel32.lib']);objects=[];inputs=[]
    def compile(source,label,defines=()):
        obj=work/(label+'.obj');command=[clang,'--target=i686-pc-windows-msvc','-std=c11','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-fno-strict-aliasing',*defines,'-c',ROOT/source,'-o',obj];run(command);objects.append(obj);inputs.append(dict(path=source,sha256=sha(ROOT/source)));return obj
    compile(RUNNER,'runner')
    for i,r in enumerate(rows):
        assert sha(ROOT/r['source'])==r['sourceSha256'] and sha(ROOT/r['oldSource'])==r['oldSourceSha256'];compile(r['source'],f'typed{i}');compile(r['oldSource'],f'retained{i}',[f'-D{r["name"]}=retained_main_{int(r["address"],0):08x}'])
    exe=work/'clear-contracts.exe';run([linker,'-flavor','link','/machine:x86','/subsystem:console','/nodefaultlib','/entry:j2p_entry','/safeseh:no','/fixed','/dynamicbase:no','/timestamp:0','/manifest:embed',"/manifestuac:level='asInvoker' uiAccess='false'",'/out:'+str(exe),*objects,work/'kernel32.lib']);binary=exe.read_bytes();offset=struct.unpack_from('<I',binary,0x3C)[0];assert binary[offset:offset+4]==b'PE\0\0' and struct.unpack_from('<H',binary,offset+4)[0]==0x14C and struct.unpack_from('<H',binary,offset+24)[0]==0x10B and b'asInvoker' in binary;first=run([exe]);second=run([exe]);assert first.stdout==second.stdout and len(first.stdout)==48;receipt=struct.unpack('<12I',first.stdout);assert receipt[:10]==(0x4A324346,1,2048,2048,2048,1792,256,1792,1792,0) and receipt[11]==0;out=dict(schemaVersion=1,pointerBytes=4,actualWindowsTypedReturns=2048,actualWindowsRetainedReturns=2048,typedPass=2048,retainedCallerWordRejects=1792,retainedNullGatePositives=256,suppliedTypedCallbacks=1792,suppliedRetainedCallbacks=1792,repeatedProcessRuns=2,receipt=list(receipt),inputSources=inputs,generator=dict(path=Path(__file__).name,sha256=sha(__file__)),profile=dict(path=PROFILE,sha256=sha(ROOT/PROFILE)),tools=dict(clangSha256=CLANG_SHA,linkerSha256=LINKER_SHA,dlltoolSha256=DLLTOOL_SHA,explicitBin=str(tools)),executable=dict(path=exe.relative_to(ROOT).as_posix(),sha256=sha(exe)),steps=steps,sourceCredit=0,limitations=['Actual hidden Win32 PE32process executes Clang-compiled typed C andretained historical C withsynthetic selectors/pointer words/byte arrays. No originalROM/save ornative executable blobs enter theprocess.','The2A498 C callback is supplied andnever dereferences synthetic pointerwords;this proves explicit caller words under C ABI,notoriginal formal declarations,heapvalidity,real frees orwhole-game portability.','Historical no-prototype zero-argument calls arearchival compiled negative controls,not a source-language guarantee;only measured rejection counts/null-gate positives are retained. Repeat runsare separate executions,not extra unique test contexts. NoAndroid deviceexecution.']);target=ROOT/'evidence/portability/save-core-explicit-clear120-windows32-20261101.json';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(out,indent=2)+'\n');print(dict(typedReturns=2048,retainedReturns=2048,rejects=1792,positives=256,exeSha256=sha(exe)))


if __name__=='__main__':main()
