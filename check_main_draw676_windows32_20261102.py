import gzip
import hashlib
import json
import struct
import subprocess
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from check_windows_i386_layout_20261101 import PINS
from main_draw676_fixture_20261102 import inputs,CALLBACKS
from match_main_draw676_20261102 import SOURCE,REPORT as NATIVE_REPORT

WORK=ROOT/'work/main-draw676-windows32-20261102'
REPORT=ROOT/'evidence/ports/main-draw676-windows32-20261102.json'
DRIVER=ROOT/'src/ports/20261102_draw676/driver.inc'


def compile_source(source,label):
    tools=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    for name,digest in PINS.items():assert sha256(tools/name)==digest,name
    folder=WORK/label;folder.mkdir(parents=True,exist_ok=True)
    glue=folder/'glue.c';glue.write_text('#include "'+source.as_posix()+'"\n#include "'+DRIVER.as_posix()+'"\n',encoding='utf-8')
    definition=folder/'kernel32.def';definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nGetStdHandle@4\nReadFile@20\nWriteFile@20\nVirtualAlloc@16\nVirtualFree@12\nExitProcess@4\n',encoding='ascii')
    library,obj,exe=folder/'kernel32.lib',folder/'glue.obj',folder/'draw676.exe'
    commands=[[str(tools/'llvm-dlltool.exe'),'-m','i386','-k','-d',str(definition),'-l',str(library)],
     [str(tools/'clang.exe'),'--driver-mode=cl','--target=i686-pc-windows-msvc','/TC','/std:c11','/O2','/GS-','/Zl','/Brepro',
      '/clang:-ffreestanding','/clang:-fno-builtin','/clang:-fno-strict-aliasing','/w','/c',str(glue),'/Fo'+str(obj)],
     [str(tools/'ld.lld.exe'),'-flavor','link','/entry:entry','/subsystem:console','/machine:x86','/nodefaultlib','/timestamp:0',
      '/fixed','/base:0x00400000','/out:'+str(exe),str(obj),str(library)]]
    for command in commands:
        run=subprocess.run(command,cwd=ROOT,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,(command,run.stdout,run.stderr)
    raw=exe.read_bytes();offset=struct.unpack_from('<I',raw,0x3C)[0]
    assert struct.unpack_from('<H',raw,offset+4)[0]==0x14C and struct.unpack_from('<I',raw,offset+8)[0]==0
    assert struct.unpack_from('<I',obj.read_bytes(),4)[0]==0
    return exe,dict(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),driverSha256=sha256(DRIVER),
     glueSha256=sha256(glue),objectSha256=sha256(obj),binary=exe.relative_to(ROOT).as_posix(),binarySha256=sha256(exe),commands=commands)


def texture_words(case):
    if not case['textureFields']:return None
    record=case['textureFields'][0];fields={int(k):v for k,v in record['fields'].items()};words=[0]*11
    words[0]=CALLBACKS.index(record['entry']);words[1]=fields[0]
    if 24 in fields:words[2:4]=[fields[24],fields[28]]
    if 32 in fields:words[4]=fields[32]|fields[34]<<16
    if 36 in fields:words[5:7]=[fields[36],fields[40]]
    words[7]=fields[44]|fields[46]<<16;words[8]=fields[48];words[9]=fields[52]
    return words


def main():
    native=read_json(NATIVE_REPORT);pin=native['replayDependencies'][0];trace=ROOT/pin['path'];assert sha256(trace)==pin['sha256']
    cases=json.loads(gzip.decompress(trace.read_bytes()))['cases'];assert len(cases)==2048
    chunks=[struct.pack('<I',2048)];pages=[]
    for case in cases:
        page,args,commands,texture,context=inputs(case['index']);assert context==case['context']
        chunks.append(struct.pack('<4I',*args)+page);pages.append(bytes(page))
    payload=b''.join(chunks);text=SOURCE.read_text(encoding='utf-8');results=[]
    mutations=[('wireframe','cmd[3] &= ~0x001f0000','cmd[3] |= 0x001f0000'),
     ('scale-command','native_fn_0202e434(0x1b','native_fn_0202e434(0x1c'),
     ('texture-width','dummy.origWidth = mat->origWidth;','dummy.origWidth = mat->origHeight;')]
    for label,old,new in [('preferred',None,None),*mutations]:
        source=SOURCE
        if old is not None:
            source=WORK/(label+'.c');source.parent.mkdir(parents=True,exist_ok=True);changed=text.replace(old,new);assert changed!=text;source.write_text(changed,encoding='utf-8')
        exe,built=compile_source(source,label)
        run=subprocess.run([str(exe)],input=payload,cwd=ROOT.parent,capture_output=True,timeout=60,creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,(run.returncode,run.stderr)
        cursor=rejected=0;rows=[]
        for index,case in enumerate(cases):
            ordinal,count,texture_count=struct.unpack_from('<3I',run.stdout,cursor);cursor+=12
            assert ordinal==index and count<=4 and texture_count<=1
            commands=[]
            for i in range(count):
                op,n=struct.unpack_from('<2I',run.stdout,cursor);cursor+=8;assert n<=64
                values=list(struct.unpack_from('<'+str(n)+'I',run.stdout,cursor))if n else[];cursor+=n*4;commands.append([op,values])
            texture=list(struct.unpack_from('<11I',run.stdout,cursor))if texture_count else None;cursor+=44*texture_count
            page=run.stdout[cursor:cursor+65536];cursor+=65536
            expected_commands=[[c['op'],c['payload']]for c in case['commands']if not c['texture']]
            passed=commands==expected_commands and texture==texture_words(case)and page==pages[index]
            rejected+=not passed;rows.append(dict(index=index,commands=commands,texture=texture,inputUnchanged=page==pages[index]))
        assert cursor==len(run.stdout)and (rejected==0)==(old is None),(label,rejected)
        if old is not None:assert rejected==next(c['rejected']for c in native['negativeControls']if c['label']==label)
        results.append(dict(label=label,build=built,actualPublicReturns=2048,rejected=rejected,positiveControls=2048-rejected,
         caseSha256=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()))
    write_json(REPORT,dict(passed=True,sourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),
     sourceBuild=results[0]['build'],actualPublicReturns=2048,actualWrongPublicReturns=6144,controls=results[1:],
     windowsCaseSha256=results[0]['caseSha256'],sourceBodyIncludedUnmodified=True,explicitGeometryAndTextureRecorders=True,
     nativeReportSha256=sha256(NATIVE_REPORT),coffMachine='I386',fullGame=False,renderedScene=False,
     androidDeviceExecutions=0,reproductionCommand='python check_main_draw676_windows32_20261102.py'))
    print(dict(actualWindowsReturns=2048,wrongPublicReturns=6144,wrongRejected=sum(r['rejected']for r in results[1:])))


if __name__=='__main__':
    main()
