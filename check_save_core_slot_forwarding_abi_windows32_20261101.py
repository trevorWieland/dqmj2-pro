import hashlib, json, os, struct, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CLANG_SHA = '6b7a698ccd1d5ef7375b7733f0675a166c560112961d3e5df0f275565a9201bc'
LINKER_SHA = 'b64100b407a472f831caf2789f6c09d501e2e4c876ebc772997c294be7f9f8f3'
DLLTOOL_SHA = 'd2f0d02b4ae109d2801f83506c329c1ca0e36d52919b273eaffb915c8cd095d1'
PROFILE = 'evidence/lanes/save-core/slot-forwarding-abi138-profile-20261101.json'
RUNNER = 'ports/windows-native/slot_forwarding_abi138_runner.c'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    candidates = [ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin', ROOT.parents[1] / 'dqmj2pro-decomp/tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin']
    tools = Path(os.environ['J2P_NDK_BIN']) if 'J2P_NDK_BIN' in os.environ else next((p for p in candidates if (p / 'clang.exe').exists()))
    clang, linker, dlltool = [tools / n for n in ['clang.exe', 'ld.lld.exe', 'llvm-dlltool.exe']]
    assert [sha(p) for p in (clang, linker, dlltool)] == [CLANG_SHA, LINKER_SHA, DLLTOOL_SHA]
    work = ROOT / 'work/sca138/windows32'
    work.mkdir(parents=True, exist_ok=True)
    profile = json.loads((ROOT / PROFILE).read_text())
    rows = profile['rows']
    steps = []
    env = {k: v for k, v in os.environ.items() if k not in {'CL', '_CL_', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LIB', 'LIBPATH', 'INCLUDE'}}

    def run(command):
        process = subprocess.run(list(map(str, command)), cwd=ROOT, env=env, capture_output=True, timeout=60, creationflags=subprocess.CREATE_NO_WINDOW)
        steps.append(dict(command=list(map(str, command)), exitCode=process.returncode, stdoutSha256=hashlib.sha256(process.stdout).hexdigest(), stderr=process.stderr.decode(errors='replace')))
        assert process.returncode == 0, steps[-1]
        return process
    definition = work / 'kernel32.def'
    definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nExitProcess@4\nGetStdHandle@4\nWriteFile@20\n')
    run([dlltool, '-m', 'i386', '-k', '-d', definition, '-l', work / 'kernel32.lib'])
    objects = []
    inputs = []

    def compile(source, label, defines=()):
        obj = work / (label + '.obj')
        command = [clang, '--target=i686-pc-windows-msvc', '-std=c11', '-O2', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-strict-aliasing', *defines, '-c', ROOT / source, '-o', obj]
        run(command)
        objects.append(obj)
        inputs.append(dict(path=source, sha256=sha(ROOT / source)))
        return obj
    compile(RUNNER, 'runner')
    row=rows[0]
    assert sha(ROOT/row['source'])==row['sourceSha256'] and sha(ROOT/row['legacySource'])==row['legacySourceSha256']
    common=['-Dnative_fn_0205f70c=guarded_getter138','-Dnative_fn_0205f6a0=guarded_setter138']
    compile(row['source'],'typed',[f"-D{row['name']}=typed138",*common])
    compile(row['legacySource'],'retained',[f"-D{row['name']}=retained138",*common])
    compile('nonmatching/save-core/20261101-slot-forwarding-abi138-controls/windows_wrong_index.c','wrong',[f"-D{row['name']}=wrong138",*common])
    for unit in profile['reusedSources']:
        assert sha(ROOT/unit['source'])==unit['sourceSha256']
        if int(unit['address'],0)==0x0205F70C:compile(unit['source'],'getter',['-Dnative_main_0205f70c=getter_actual138'])
        else:compile(unit['source'],'setter',['-Dnative_main_0205f6a0=setter_actual138','-Dnative_fn_02038148=sdk_callback138','-Dnative_fn_0205ed58=host_status138'])
    exe = work / 'slot-forwarding-contracts.exe'
    run([linker, '-flavor', 'link', '/machine:x86', '/subsystem:console', '/nodefaultlib', '/entry:j2p_entry', '/safeseh:no', '/fixed', '/dynamicbase:no', '/timestamp:0', '/manifest:embed', "/manifestuac:level='asInvoker' uiAccess='false'", '/out:' + str(exe), *objects, work / 'kernel32.lib'])
    binary = exe.read_bytes()
    offset = struct.unpack_from('<I', binary, 60)[0]
    assert binary[offset:offset + 4] == b'PE\x00\x00' and struct.unpack_from('<H', binary, offset + 4)[0] == 332 and (struct.unpack_from('<H', binary, offset + 24)[0] == 267) and (b'asInvoker' in binary)
    first = run([exe])
    second = run([exe])
    assert first.stdout==second.stdout and len(first.stdout)==96
    receipt=struct.unpack('<24I',first.stdout);n=receipt[2]
    assert receipt[:3]==(0x4A325346,1,4208) and receipt[3:7]==(n,n,0,0)
    assert receipt[7]==n and receipt[8]+receipt[9]==n and receipt[10]==0 and receipt[9]>0
    assert receipt[11]==n and receipt[12]+receipt[13]==n and receipt[14]==0 and receipt[12]>0 and receipt[13]>0
    assert receipt[15]==n and receipt[16]==receipt[8] and receipt[17]==receipt[12] and receipt[18]==receipt[19]==receipt[20] and receipt[22:]==(0,0)
    out=dict(schemaVersion=1,pointerBytes=4,uniqueContexts=n,actualWindowsTypedReturns=n,actualWindowsRetainedReturns=n,actualWindowsWrongReturns=n,typedPass=n,retainedMissingIndexRejects=receipt[9],retainedPositives=receipt[8],wrongIndexRejects=receipt[13],wrongIndexPositives=receipt[12],repeatedProcessRuns=2,totalTypedReturnsAcrossRepeatedRuns=2*n,totalRetainedReturnsAcrossRepeatedRuns=2*n,totalWrongReturnsAcrossRepeatedRuns=2*n,receipt=list(receipt),inputSources=inputs,generator=dict(path=Path(__file__).name,sha256=sha(__file__)),profile=dict(path=PROFILE,sha256=sha(ROOT/PROFILE)),tools=dict(clangSha256=CLANG_SHA,linkerSha256=LINKER_SHA,dlltoolSha256=DLLTOOL_SHA,explicitBin=str(tools)),executable=dict(path=exe.relative_to(ROOT).as_posix(),sha256=sha(exe)),steps=steps,sourceCredit=0,limitations=['Actual hidden PE32 executes typed48-byte C, retained historical C and a complete wrong-index C function. The frozen accepted96-byte getter and108-byte setter source also execute as C. Only their SDK callback and status primitive are modeled; no ROM/save/native executable blob enters the process.','The getter guard records the full incoming index before accessing a table. Historical omitted-argument behavior is an actual compiled binary observation, not a C-language guarantee. Full previous-byte/FFFFFFFF return, signed validity, unsigned127 setter gate, complete forwarded words, memory and SDK callback contracts are checked independently.','Two identical process runs do not double unique contexts. Original native comparisons and Windows executions remain distinct; no Android or complete-game execution is established.'])
    target = ROOT / 'evidence/portability/save-core-slot-forwarding-abi138-windows32-20261101.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, indent=2) + '\n')
    print(dict(contexts=n,typed=n,retainedRejects=receipt[9],retainedPositives=receipt[8],wrongRejects=receipt[13],wrongPositives=receipt[12],exeSha256=sha(exe)))
if __name__ == '__main__':
    main()
