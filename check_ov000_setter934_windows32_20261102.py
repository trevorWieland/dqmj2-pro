import json
import struct
import subprocess
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from project import ROOT,read_json,write_json,sha256
TOOLS=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
WORK=ROOT/'work/ol934-windows'
PORT=ROOT/'ports/windows-setter934'
SOURCES=[('preferred','src/overlays/ov000_20261102_raw_setter931/source.c',0),('wrong-sign-return','nonmatching/overlay-lane/20261102-setter933-controls/wrong-sign-return/source.c',1536),('wrong-truncated-return','nonmatching/overlay-lane/20261102-setter933-controls/wrong-truncated-return/source.c',1536),('wrong-byte-store','nonmatching/overlay-lane/20261102-setter933-controls/wrong-byte-store/source.c',1792)]


def build(name,path):
    folder=WORK/name
    folder.mkdir(parents=True,exist_ok=True)
    source=folder/'kernel.c'
    source.write_bytes(path.read_bytes())
    source.with_name('context.h').write_bytes(path.with_name('context.h').read_bytes())
    definition=folder/'kernel32.def'
    definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nExitProcess@4\n',encoding='ascii')
    library=folder/'kernel32.lib'
    commands=[[str(TOOLS/'llvm-dlltool.exe'),'-m','i386','-k','-d',str(definition),'-l',str(library)]]
    objects=[]
    for index,item in enumerate([source,PORT/'driver.c']):
        obj=folder/('unit'+str(index)+'.obj')
        objects.append(obj)
        commands.append([str(TOOLS/'clang.exe'),'--driver-mode=cl','--target=i686-pc-windows-msvc','/TC','/std:c11','/O2','/GS-','/Zl','/Brepro','/clang:-ffreestanding','/clang:-fno-builtin','/w','/c',str(item),'/Fo'+str(obj)])
    executable=folder/'setter.exe'
    commands.append([str(TOOLS/'ld.lld.exe'),'-flavor','link','/entry:entry','/subsystem:console','/machine:x86','/nodefaultlib','/timestamp:0','/fixed','/base:0x00400000','/out:'+str(executable),*map(str,objects),str(library)])
    for command in commands:
        result=subprocess.run(command,cwd=ROOT,capture_output=True,timeout=60,creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode:raise ValueError(dict(command=command,returncode=result.returncode,stderr=result.stderr.decode(errors='replace')))
    data=executable.read_bytes()
    offset=struct.unpack_from('<I',data,0x3C)[0]
    if struct.unpack_from('<H',data,offset+4)[0]!=0x14C or struct.unpack_from('<I',data,offset+8)[0]!=0:raise ValueError('934 PE32 architecture/timestamp differs')
    for obj in objects:
        if struct.unpack_from('<I',obj.read_bytes(),4)[0]!=0:raise ValueError('934 COFF timestamp differs')
    return executable,dict(source=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path)),unmodifiedSourceBytes=sha256(source)==sha256(path),contextSha256=sha256(path.with_name('context.h')),driverSha256=sha256(PORT/'driver.c'),commands=commands,objects=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in objects],executable=dict(path=executable.relative_to(ROOT).as_posix(),sha256=sha256(executable)),machine='I386',peTimestamp=0)


def main():
    if sys.version_info[:3]!=(3,13,5):raise ValueError('934 pinned Python differs')
    for row in read_json(ROOT/'evidence/verification/geometry895-windows-tools-import-20261102.json')['files']:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError(('934 local tool differs',row['path']))
    runs=[]
    for name,path,expected in SOURCES:
        executable,proof=build(name,ROOT/path)
        results=[]
        for process in range(2 if name=='preferred'else 1):
            result=subprocess.run([str(executable)],cwd=ROOT.parent,capture_output=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode!=expected or result.stdout or result.stderr:raise ValueError(('934 actual PE32 result differs',name,result.returncode,expected,result.stdout,result.stderr))
            results.append(dict(processIndex=process,actualPublicReturns=1792,independentContractRejects=result.returncode,positive=1792-result.returncode))
        runs.append(dict(name=name,build=proof,processes=results))
    report=dict(schemaVersion=1,allPassed=True,sourceCredit=0,newMatchedBytes=0,platform='Windows PE32 console I386',actualPreferredPublicReturns=3584,actualWrongPublicReturns=5376,wrongRejects=4864,preferredSourceUnchanged=True,runs=runs,limits=['Actual silent native Windows console executions, two fresh preferred processes, three independently compiled wrong-C processes. Source is byte-identical to the ARM raw-word alternative; source credit remains zero because the DS function is already accepted.','Separate translation units and no LTO retain1792 external function calls per process; public return value, low8 store and adjacent canaries are independently checked. Process exit code is the number of rejected contexts.','All256 low bytes and seven upper patterns cover zero/sign extension domains. A signed8-return facade has valid positive cases, retained rather than treated as unconditional failure.','This is the pure raw-word alternative API, not proof of the old s8 signature or an original formal declaration. No Android device, GUI, game scene, persistent state or application edits.'])
    write_json(ROOT/'evidence/ports/ov000-setter934-windows32-20261102.json',report)
    print(dict(actualPreferredPublicReturns=3584,actualWrongPublicReturns=5376,wrongRejects=4864,sourceCredit=0),flush=True)

if __name__=='__main__':main()
