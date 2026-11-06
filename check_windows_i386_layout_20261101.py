import platform
import struct
import subprocess
from pathlib import Path
from project import ROOT,write_json,sha256

PINS={'clang.exe':'6b7a698ccd1d5ef7375b7733f0675a166c560112961d3e5df0f275565a9201bc',
 'ld.lld.exe':'b64100b407a472f831caf2789f6c09d501e2e4c876ebc772997c294be7f9f8f3',
 'llvm-dlltool.exe':'d2f0d02b4ae109d2801f83506c329c1ca0e36d52919b273eaffb915c8cd095d1'}


def main():
    folder=ROOT/'work/windows-i386-layout-probe-20261101';folder.mkdir(parents=True,exist_ok=True)
    tools=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    for name,digest in PINS.items():assert sha256(tools/name)==digest,name
    definition=folder/'kernel32.def'
    definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nGetStdHandle@4\nWriteFile@20\nExitProcess@4\n',encoding='ascii')
    lib=folder/'kernel32.lib';obj=folder/'probe.obj';exe=folder/'layout_probe.exe'
    source=ROOT/'src/ports/20261101_win32_layout/probe.c'
    commands=[[str(tools/'llvm-dlltool.exe'),'-m','i386','-k','-d',str(definition),'-l',str(lib)],
     [str(tools/'clang.exe'),'--driver-mode=cl','--target=i686-pc-windows-msvc','/TC','/std:c11','/O2','/GS-','/Zl','/Brepro',
      '/clang:-ffreestanding','/clang:-fno-builtin','/c',str(source),'/Fo'+str(obj)],
     [str(tools/'ld.lld.exe'),'-flavor','link','/entry:entry','/subsystem:console','/machine:x86','/nodefaultlib',
      '/timestamp:0','/fixed','/base:0x00400000','/out:'+str(exe),str(obj),str(lib)]]
    for command in commands:
        run=subprocess.run(command,cwd=ROOT,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,(command,run.stdout,run.stderr)
    run=subprocess.run([str(exe)],cwd=ROOT.parent,capture_output=True,timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
    assert run.returncode==0,(run.returncode,run.stderr)
    values=list(struct.unpack('<6I',run.stdout));assert values==[4,4,28,24,25,26],values
    raw=exe.read_bytes();pe=struct.unpack_from('<I',raw,0x3c)[0]
    assert struct.unpack_from('<H',raw,pe+4)[0]==0x14c
    assert struct.unpack_from('<I',raw,pe+8)[0]==0 and struct.unpack_from('<I',obj.read_bytes(),4)[0]==0
    write_json(ROOT/'evidence/ports/windows-i386-layout-probe-20261101.json',dict(passed=True,sourceCredit=0,
     generator=Path(__file__).name,generatorSha256=sha256(__file__),source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),
     commands=commands,tools=[dict(path=(tools/n).relative_to(ROOT).as_posix(),sha256=sha256(tools/n))for n in PINS],
     binary=exe.relative_to(ROOT).as_posix(),binarySha256=sha256(exe),actualWindowsExitCode=run.returncode,
     windowsVersion=platform.version(),coffMachine='I386',layoutWords=values,privateChildNoWindow=True,
     fullGame=False,sourceOnlyRom=False,androidDeviceExecutions=0,reproductionCommand='python check_windows_i386_layout_20261101.py'))
    print(dict(actualWindowsExitCode=0,coffMachine='I386',layoutWords=values,binarySha256=sha256(exe)))


if __name__=='__main__':
    main()
