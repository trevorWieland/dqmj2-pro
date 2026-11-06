import gzip
import hashlib
import json
import struct
import subprocess
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from check_windows_i386_layout_20261101 import PINS
from main_joint_scale336_fixture_20261102 import inputs
from match_main_joint_scale336_20261102 import SOURCE,REPORT as NATIVE_REPORT

WORK=ROOT/'work/main-joint-scale336-windows32-20261102'
REPORT=ROOT/'evidence/ports/main-joint-scale336-windows32-20261102.json'
DRIVER=ROOT/'src/ports/20261102_joint_scale336/driver.inc'


def compile_source(source,label):
    tools=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    for name,digest in PINS.items():assert sha256(tools/name)==digest,name
    folder=WORK/label;folder.mkdir(parents=True,exist_ok=True)
    glue=folder/'glue.c';glue.write_text('#include "'+source.as_posix()+'"\n#include "'+DRIVER.as_posix()+'"\n',encoding='utf-8')
    definition=folder/'kernel32.def';definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nGetStdHandle@4\nReadFile@20\nWriteFile@20\nVirtualAlloc@16\nVirtualFree@12\nExitProcess@4\n',encoding='ascii')
    library,obj,exe=folder/'kernel32.lib',folder/'glue.obj',folder/'joint_scale336.exe'
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


def main():
    native=read_json(NATIVE_REPORT);pin=native['replayDependencies'][0];trace=ROOT/pin['path'];assert sha256(trace)==pin['sha256']
    cases=json.loads(gzip.decompress(trace.read_bytes()))['cases'];assert len(cases)==2048
    chunks=[struct.pack('<I',2048)];expected=[]
    for case in cases:
        page,cache,out_page,out_cache,args,rs=inputs(case['index']);assert args==case['args']
        chunks.append(struct.pack('<4I',*args)+page+cache);expected.append((bytes(out_page),bytes(out_cache)))
    payload=b''.join(chunks);text=SOURCE.read_text(encoding='utf-8');results=[]
    mutations=[('final-flag','pResult->flag |= NNS_G3D_JNTANM_RESULTFLAG_SCALEEX1_ONE;','pResult->flag |= NNS_G3D_JNTANM_RESULTFLAG_SCALEEX0_ONE;'),
     ('toggle-cache-bit','vec[idx >> 5] |= 1U','vec[idx >> 5] ^= 1U'),
     ('inverse-component','scaleCache[nodeID].inv.y = *(p + 4);','scaleCache[nodeID].inv.z = *(p + 4);')]
    for label,old,new in [('preferred',None,None),*mutations]:
        source=SOURCE
        if old is not None:
            source=WORK/(label+'.c');source.parent.mkdir(parents=True,exist_ok=True);changed=text.replace(old,new);assert changed!=text;source.write_text(changed,encoding='utf-8')
        exe,built=compile_source(source,label)
        run=subprocess.run([str(exe)],input=payload,cwd=ROOT.parent,capture_output=True,timeout=60,creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,(run.returncode,run.stderr)
        stride=4+65536+11520;assert len(run.stdout)==stride*2048
        rejected=0;digest=hashlib.sha256()
        for i,(page,cache)in enumerate(expected):
            offset=i*stride;ordinal=struct.unpack_from('<I',run.stdout,offset)[0];assert ordinal==i
            actual_page=run.stdout[offset+4:offset+4+65536];actual_cache=run.stdout[offset+4+65536:offset+stride]
            digest.update(run.stdout[offset:offset+stride]);rejected+=actual_page!=page or actual_cache!=cache
            if label=='preferred':assert hashlib.sha256(actual_page).hexdigest()==cases[i]['dataSha256']
        assert (rejected==0)==(old is None),(label,rejected)
        if old is not None:assert rejected==next(c['rejected']for c in native['negativeControls']if c['label']==label)
        results.append(dict(label=label,build=built,actualPublicReturns=2048,rejected=rejected,positiveControls=2048-rejected,caseSha256=digest.hexdigest()))
    write_json(REPORT,dict(passed=True,sourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),
     sourceBuild=results[0]['build'],actualPublicReturns=2048,actualWrongPublicReturns=6144,controls=results[1:],
     windowsCaseSha256=results[0]['caseSha256'],sourceBodyIncludedUnmodified=True,typedGlobalStorageExplicit=True,
     comparedInputBytes=65536,comparedCacheBytes=11520,nativeReportSha256=sha256(NATIVE_REPORT),coffMachine='I386',
     fullGame=False,androidDeviceExecutions=0,reproductionCommand='python check_main_joint_scale336_windows32_20261102.py'))
    print(dict(actualWindowsReturns=2048,wrongPublicReturns=6144,wrongRejected=sum(r['rejected']for r in results[1:])))


if __name__=='__main__':
    main()
