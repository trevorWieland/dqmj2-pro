import hashlib, json, os, struct, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CLANG_SHA = '6b7a698ccd1d5ef7375b7733f0675a166c560112961d3e5df0f275565a9201bc'
LINKER_SHA = 'b64100b407a472f831caf2789f6c09d501e2e4c876ebc772997c294be7f9f8f3'
DLLTOOL_SHA = 'd2f0d02b4ae109d2801f83506c329c1ca0e36d52919b273eaffb915c8cd095d1'
PROFILE = 'evidence/lanes/save-core/configuration-abi130-profile-20261101.json'
RUNNER = 'ports/windows-native/configuration_abi130_runner.c'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    candidates = [ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin', ROOT.parents[1] / 'dqmj2pro-decomp/tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin']
    tools = Path(os.environ['J2P_NDK_BIN']) if 'J2P_NDK_BIN' in os.environ else next((p for p in candidates if (p / 'clang.exe').exists()))
    clang, linker, dlltool = [tools / n for n in ['clang.exe', 'ld.lld.exe', 'llvm-dlltool.exe']]
    assert [sha(p) for p in (clang, linker, dlltool)] == [CLANG_SHA, LINKER_SHA, DLLTOOL_SHA]
    work = ROOT / 'work/sca130/windows32'
    work.mkdir(parents=True, exist_ok=True)
    profile = json.loads((ROOT / PROFILE).read_text())
    row = profile['rows'][0]
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
    assert sha(ROOT / row['source']) == row['sourceSha256'] and sha(ROOT / profile['historicalSource']) == profile['historicalSourceSha256']
    compile(row['source'], 'typed', ['-Dnative_main_0204a04c=typed_configuration130'])
    compile(profile['historicalSource'], 'retained', ['-Dnative_main_0204a04c=retained_configuration130'])
    compile('nonmatching/save-core/20261101-configuration-abi130-controls/wrong_cleanup_object.c', 'wrong', ['-Dnative_main_0204a04c=wrong_configuration130'])
    exe = work / 'configuration-contracts.exe'
    run([linker, '-flavor', 'link', '/machine:x86', '/subsystem:console', '/nodefaultlib', '/entry:j2p_entry', '/safeseh:no', '/fixed', '/dynamicbase:no', '/timestamp:0', '/manifest:embed', "/manifestuac:level='asInvoker' uiAccess='false'", '/out:' + str(exe), *objects, work / 'kernel32.lib'])
    binary = exe.read_bytes()
    offset = struct.unpack_from('<I', binary, 60)[0]
    assert binary[offset:offset + 4] == b'PE\x00\x00' and struct.unpack_from('<H', binary, offset + 4)[0] == 332 and (struct.unpack_from('<H', binary, offset + 24)[0] == 267) and (b'asInvoker' in binary)
    first = run([exe])
    second = run([exe])
    assert first.stdout == second.stdout and len(first.stdout) == 64
    receipt = struct.unpack('<16I', first.stdout)
    assert receipt[:4] == (1244807491, 1, 1024, 1024) and receipt[4] == 1024 and (receipt[5] > 0) and (receipt[5] + receipt[6] == 1024) and (receipt[7:11] == (1024, 512, 512, 1024)) and (receipt[12:14] == (512, 0)) and (receipt[15] == 0)
    out = dict(schemaVersion=1, pointerBytes=4, actualWindowsTypedReturns=1024, perProcessTypedReturns=1024,totalTypedReturnsAcrossRepeatedRuns=2048,totalRetainedReturnsAcrossRepeatedRuns=2048,totalWrongReturnsAcrossRepeatedRuns=2048, actualWindowsRetainedReturns=1024, actualWindowsWrongReturns=1024, typedPass=1024, retainedCallerPointerRejects=receipt[5], retainedPositives=receipt[6], wrongCallerPointerRejects=512, wrongZeroHandlePositives=512, repeatedProcessRuns=2, receipt=list(receipt), inputSources=inputs, generator=dict(path=Path(__file__).name, sha256=sha(__file__)), profile=dict(path=PROFILE, sha256=sha(ROOT / PROFILE)), tools=dict(clangSha256=CLANG_SHA, linkerSha256=LINKER_SHA, dlltoolSha256=DLLTOOL_SHA, explicitBin=str(tools)), executable=dict(path=exe.relative_to(ROOT).as_posix(), sha256=sha(exe)), steps=steps, sourceCredit=0, limitations=['Actual hidden Win32 PE32process executes newtyped100-byte function C,retained historical C andcomplete wrongtyped C underpinned Clang/LLD withsynthetic objects. NoROM/save/nativeexecutableblob enters theprocess.', 'Host lowerC models independentlycheck theincoming cleanup pointer,handleclear,callorder,forwarded configuration words,packed fields,flags/modecopy andrawobjectreturn. These modelsdo notprove originalSDKimplementations orwholegameportability.', 'The historical no-prototype missingargument call is anactualcompiled oldbinary control,not a source-language guarantee. Itshelper checksargumentidentity beforeany dereference. Exact nativeCW bytes donotestablish portablecorrectness. Wrongtypedobjecthas512 positivezero-handlecases and512 rejects.', 'Two identical processruns arenotadditional uniquecontexts. Object/results,callerPointerrejections andprovidedmodelscope remain distinct fromnative/Android execution.'])
    target = ROOT / 'evidence/portability/save-core-configuration-abi130-windows32-20261101.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, indent=2) + '\n')
    print(dict(typedReturns=1024, retainedReturns=1024, wrongReturns=1024, retainedRejects=receipt[5], retainedPositives=receipt[6], exeSha256=sha(exe)))
if __name__ == '__main__':
    main()
