import gzip
import hashlib
import json
import struct
import subprocess
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from check_windows_i386_layout_20261101 import PINS
import main_joint_scalar752_fixture_20261102 as fixture

WORK=ROOT/'work/main-joint-scalar752-windows32-20261102'
REPORT=ROOT/'evidence/ports/main-joint-scalar752-windows32-20261102.json'
DRIVER=ROOT/'src/ports/20261102_joint_scalar752/driver.c'
NATIVE=ROOT/'evidence/matches/main-joint-scalar752-20261102.json'
SOURCES=[ROOT/'src/runtime/20261102_joint_animation4588/native_main_02032b90.c',
 ROOT/'src/runtime/20261102_joint_animation4588_ranked/native_main_02032ed4.c']


def compile_sources(label,mutation=None):
    tools=ROOT/'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    for name,digest in PINS.items():assert sha256(tools/name)==digest,name
    folder=WORK/label;folder.mkdir(parents=True,exist_ok=True);paths=list(SOURCES)
    if mutation:
        index,old,new=mutation;original=paths[index];text=original.read_text(encoding='utf-8')
        changed=text.replace(old,new);assert changed!=text
        wrong=folder/original.name;wrong.write_text(changed,encoding='utf-8');paths[index]=wrong
    definition=folder/'kernel32.def'
    definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nGetStdHandle@4\nReadFile@20\nWriteFile@20\nVirtualAlloc@16\nVirtualFree@12\nExitProcess@4\n',encoding='ascii')
    library=folder/'kernel32.lib';commands=[[str(tools/'llvm-dlltool.exe'),'-m','i386','-k','-d',str(definition),'-l',str(library)]]
    objects=[];inputs=[]
    for number,path in enumerate([*paths,DRIVER]):
        obj=folder/f'unit{number:02}.obj';objects.append(obj)
        commands.append([str(tools/'clang.exe'),'--driver-mode=cl','--target=i686-pc-windows-msvc','/TC','/std:c11',
         '/O2','/GS-','/Zl','/Brepro','/clang:-ffreestanding','/clang:-fno-builtin','/clang:-fno-strict-aliasing','/w',
         '/c',str(path),'/Fo'+str(obj)])
        inputs.append(dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path)))
    exe=folder/'joint_scalar.exe'
    commands.append([str(tools/'ld.lld.exe'),'-flavor','link','/entry:entry','/subsystem:console','/machine:x86',
     '/nodefaultlib','/timestamp:0','/fixed','/base:0x00400000','/out:'+str(exe),*[str(p)for p in objects],str(library)])
    for command in commands:
        run=subprocess.run(command,cwd=ROOT,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,(command,run.stdout.decode(errors='replace'),run.stderr.decode(errors='replace'))
    raw=exe.read_bytes();offset=struct.unpack_from('<I',raw,0x3C)[0]
    assert struct.unpack_from('<H',raw,offset+4)[0]==0x14C and struct.unpack_from('<I',raw,offset+8)[0]==0
    for obj in objects:assert struct.unpack_from('<I',obj.read_bytes(),4)[0]==0
    return exe,dict(inputs=inputs,objectHashes=[sha256(p)for p in objects],binarySha256=sha256(exe),commands=commands,
     compilerPins=PINS,driverSha256=sha256(DRIVER))


def main():
    native=read_json(NATIVE);pin=next(p for p in native['replayDependencies']if p['path'].endswith('.json.gz'))
    assert sha256(ROOT/pin['path'])==pin['sha256']
    cases=json.loads(gzip.decompress((ROOT/pin['path']).read_bytes()))['cases'];assert len(cases)==4096
    chunks=[struct.pack('<I',len(cases))];expected=[]
    for index,row in enumerate(cases):
        page,output,entry,args,context=fixture.inputs(index)
        assert hashlib.sha256(output).hexdigest()==row['dataSha256']
        chunks.append(struct.pack('<5I',entry,*args)+page);expected.append(output)
    payload=b''.join(chunks);results=[]
    controls=[('translation-wrap',(0,'if (pJntAnm->flag & NNS_G3D_JNTANM_OPTION_END_TO_START_INTERPOLATION)',
     'if (!(pJntAnm->flag & NNS_G3D_JNTANM_OPTION_END_TO_START_INTERPOLATION))')),
     ('scale-wrap',(1,'if (pJntAnm->flag & NNS_G3D_JNTANM_OPTION_END_TO_START_INTERPOLATION)',
     'if (!(pJntAnm->flag & NNS_G3D_JNTANM_OPTION_END_TO_START_INTERPOLATION))')),
     ('translation-width',(0,'const fx16 * p_fx16','const u16 * p_fx16')),
     ('scale-width',(1,'const fx16 * p_fx16','const u16 * p_fx16'))]
    for label,mutation in[('preferred',None),*controls]:
        exe,built=compile_sources(label,mutation)
        run=subprocess.run([str(exe)],input=payload,cwd=ROOT.parent,capture_output=True,timeout=60,
         creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,(label,run.returncode,run.stderr)
        stride=16388;assert len(run.stdout)==len(cases)*stride
        rejected=affected_rejected=0;digests=[]
        for index,wanted in enumerate(expected):
            offset=index*stride;assert struct.unpack_from('<I',run.stdout,offset)[0]==index
            output=run.stdout[offset+4:offset+stride];passed=output==wanted;rejected+=not passed
            if mutation and index%2==mutation[0]:affected_rejected+=not passed
            digests.append(hashlib.sha256(output).hexdigest())
        assert (rejected==0)==(mutation is None),(label,rejected)
        if mutation:
            control=next(c for c in native['negativeControls']if c['label']==label)
            assert affected_rejected==control['rejected'],(label,affected_rejected,control)
        results.append(dict(label=label,build=built,actualPublicCalls=len(cases),rejected=rejected,
         affectedNativeControlRejects=affected_rejected,outputDigest=hashlib.sha256(''.join(digests).encode()).hexdigest()))
    write_json(REPORT,dict(passed=True,sourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),
     preferred=results[0],controls=results[1:],actualPreferredPublicCalls=4096,actualWrongPublicCalls=16384,
     unmodifiedTargetSourceBodies=True,separateTranslationUnits=True,functionProviders=0,
     entire16384ByteInputOutputCompared=True,nativeReportSha256=sha256(NATIVE),
     fullGame=False,androidDeviceExecutions=0,androidLP64SourcePortabilityProven=False,
     reproductionCommand='python check_main_joint_scalar752_windows32_20261102.py'))
    print(dict(preferred=4096,wrong=16384,wrongRejected=sum(r['rejected']for r in results[1:])))


if __name__=='__main__':
    main()
