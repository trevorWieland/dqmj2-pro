import hashlib
import json
import os
import struct
import subprocess
import zipfile
from pathlib import Path
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,read_json,write_json,sha256
from check_windows_i386_layout_20261101 import PINS
import check_main_joint_scalar752_windows32_20261102 as windows
import main_material_track1120_fixture_20261102 as fixture
from match_main_material_track1120_20261102 import SOURCES

WORK=ROOT/'work/android-material-track1120-20261102'
VIEWS=ROOT/'generated/portability/20261102-material-track1120-fixed-width'
BUNDLE=ROOT/'build/ports/android-material-track1120-20261102'
REPORT=ROOT/'evidence/portability/android-material-track1120-build-20261102.json'


def main():
    target_report=ROOT/'evidence/matches/main-material-track1120-20261102.json'
    native=read_json(target_report);assert native['matchedBytes']==1120
    existing=read_json(ROOT/'evidence/ports/main-material-track1120-windows32-20261102.json')
    assert existing['passed']and existing['actualPreferredPublicCalls']==4096
    WORK.mkdir(parents=True,exist_ok=True);VIEWS.mkdir(parents=True,exist_ok=True);BUNDLE.mkdir(parents=True,exist_ok=True)
    views=[];changes=[]
    for path in SOURCES:
        text=path.read_text(encoding='utf-8');assert text.count('typedef unsigned long u32;')==1
        changed=text.replace('typedef unsigned long u32;','typedef unsigned int u32;');view=VIEWS/path.name
        if view.exists():assert view.read_text(encoding='utf-8')==changed
        else:view.write_text(changed,encoding='utf-8')
        views.append(view);changes.append(dict(source=path.relative_to(ROOT).as_posix(),sourceSha256=sha256(path),
         portableView=view.relative_to(ROOT).as_posix(),portableSha256=sha256(view),onlyChange='unsigned-long32 to unsigned-int32 typedef'))
    target_driver=ROOT/'src/ports/20261102_material_track1120/driver.c';driver=WORK/'windows-driver.c'
    driver.write_text(target_driver.read_text(encoding='utf-8').replace('typedef unsigned long u32;','typedef unsigned int u32;'),encoding='utf-8')
    windows.SOURCES=views;windows.DRIVER=driver;windows.WORK=WORK/'windows-fixed-width'
    exe,built=windows.compile_sources('preferred')
    chunks=[struct.pack('<I',4096)];expected=[];all_contexts=[]
    for index in range(4096):
        page,entry,args,context=fixture.inputs(index)
        chunks.append(struct.pack('<5I',entry,*args,*([0]*(4-len(args))))+page)
        output=struct.pack('<II',index,context['expectedReturn'])+page;expected.append(output);all_contexts.append((chunks[-1],output))
    payload=b''.join(chunks);wanted=b''.join(expected)
    result=subprocess.run([str(exe)],input=payload,cwd=ROOT.parent,capture_output=True,timeout=60,creationflags=subprocess.CREATE_NO_WINDOW)
    assert result.returncode==0 and result.stdout==wanted,(result.returncode,len(result.stdout))
    windows_evidence=dict(passed=True,sourceCredit=0,actualPublicCalls=4096,functionProviders=0,build=built,
     inputSha256=hashlib.sha256(payload).hexdigest(),outputSha256=hashlib.sha256(wanted).hexdigest(),sourceChanges=changes)
    windows_path=ROOT/'evidence/ports/main-material-track1120-fixed-width-windows32-20261102.json';write_json(windows_path,windows_evidence)
    ndk=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64';clang=ndk/'bin/clang.exe'
    for name,digest in PINS.items():assert sha256(ndk/'bin'/name)==digest,name
    environment={k:v for k,v in os.environ.items()if k not in{'CL','_CL_','CFLAGS','CPPFLAGS','LDFLAGS','LIB','LIBPATH','INCLUDE','CPATH','C_INCLUDE_PATH','SDKROOT'}}
    steps=[];objects=[];dependencies=set()
    def run(command):
        command=[str(v)for v in command];process=subprocess.run(command,cwd=ROOT.parent,env=environment,capture_output=True,timeout=120,creationflags=subprocess.CREATE_NO_WINDOW)
        step=dict(command=command,exitCode=process.returncode,stdout=process.stdout.decode(errors='replace'),stderr=process.stderr.decode(errors='replace'));steps.append(step)
        assert process.returncode==0,step
        return process
    runner=ROOT/'ports/android-native/material_track1120_runner_20261102.c'
    for index,path in enumerate([*views,runner]):
        obj=WORK/f'android-{index}.o';dep=WORK/f'android-{index}.d'
        run([clang,'--target=aarch64-linux-android26','--sysroot='+str(ndk/'sysroot'),'-std=c11','-O2','-fPIE','-fno-strict-aliasing','-MD','-MF',dep,'-c',path,'-o',obj]);objects.append(obj)
        for token in dep.read_text().split(': ',1)[1].replace('\\\n',' ').split():
            p=Path(token).resolve();assert p.is_file()and p.is_relative_to(ROOT),token;dependencies.add(p)
    executable=BUNDLE/'material-track1120'
    linked=run([clang,'--target=aarch64-linux-android26','--sysroot='+str(ndk/'sysroot'),'-fuse-ld=lld','-fPIE','-pie','-Wl,--build-id=sha1','-Wl,--trace',*objects,'-o',executable])
    for line in linked.stdout.decode(errors='replace').splitlines():
        path=Path(line.strip().split('(',1)[0])
        if path.is_file():
            path=path.resolve();assert path.is_relative_to(ROOT);dependencies.add(path)
    with executable.open('rb')as stream:
        elf=ELFFile(stream);assert elf.elfclass==64 and elf.little_endian and elf['e_machine']=='EM_AARCH64'and elf['e_type']=='ET_DYN'
        assert next(s.get_interp_name()for s in elf.iter_segments()if s['p_type']=='PT_INTERP')=='/system/bin/linker64'
        symbols={s.name for s in elf.get_section_by_name('.symtab').iter_symbols()}
        assert all('native_main_'+x in symbols for x in['02033930','02033a98','02033d48','02033e48'])
    selected=sorted({((i*269)%4096)for i in range(256)});assert len(selected)==256
    vector_payload=struct.pack('<I',len(selected))+b''.join(all_contexts[i][0]for i in selected)
    vector_expected=b''.join(struct.pack('<I',ordinal)+all_contexts[i][1][4:]for ordinal,i in enumerate(selected))
    categories={fixture.inputs(i)[3]['kind']for i in selected};assert categories=={0,1,2,3}
    (BUNDLE/'vectors.bin').write_bytes(vector_payload);(BUNDLE/'expected.bin').write_bytes(vector_expected)
    (BUNDLE/'SHA256SUMS').write_text(''.join(sha256(BUNDLE/n)+'  '+n+'\n'for n in['material-track1120','vectors.bin','expected.bin']),encoding='ascii')
    (BUNDLE/'README.md').write_text('''# Private Android ARM64 material-track component test

This API26+ ARM64 command-line bundle contains four pure reconstructed component functions and256 deterministic synthetic contexts. Source integer typedefs explicitly use32-bit unsigned int; the same views pass4,096 actual Windows i386 calls. The Android ELF is cross-compiled and inspected; no Android/Thor execution has occurred.

In a disposable executable directory on an authorized ARM64 Android device, verify SHA256SUMS, then run:

```sh
chmod 700 material-track1120
./material-track1120 < vectors.bin > actual.bin
cmp actual.bin expected.bin
```

Success requires exit0 and exact binary equality. No ROM/save, display, audio, network or persistent game-state input is used. Keep this bundle private. Dual-screen UI, parent pointer-rich layouts, rendering, complete game behavior and original target-byte equivalence of the portability typedef revision are not established.
''',encoding='utf-8')
    archive=BUNDLE.with_suffix('.zip')
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9)as bundle:
        for path in sorted(BUNDLE.iterdir()):
            entry=zipfile.ZipInfo(path.name,date_time=(2000,1,1,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;entry.external_attr=0o600<<16;bundle.writestr(entry,path.read_bytes())
    write_json(REPORT,dict(sourceCredit=0,nativeTargetReportSha256=sha256(target_report),sourceChanges=changes,
     generator=Path(__file__).name,generatorSha256=sha256(__file__),windowsFixedWidthReport=windows_path.relative_to(ROOT).as_posix(),windowsReportSha256=sha256(windows_path),
     actualWindowsPublicCalls=4096,nativeAndroidExecutableCrossCompiled=True,androidDeviceExecutions=0,selectedNativeIndices=selected,
     bundle=archive.relative_to(ROOT).as_posix(),bundleSha256=sha256(archive),executableSha256=sha256(executable),
     syntheticInputSha256=hashlib.sha256(vector_payload).hexdigest(),expectedOutputSha256=hashlib.sha256(vector_expected).hexdigest(),
     dependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in sorted(dependencies)],steps=steps,
     reproductionCommand='python build_android_material_track1120_20261102.py',fullGame=False,dualScreenInterface=False))
    print(dict(androidElfBuilt=True,syntheticContexts=256,actualWindowsCalls=4096,androidExecutions=0,dependencies=len(dependencies),bundleSha256=sha256(archive)))


if __name__=='__main__':
    main()
