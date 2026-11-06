import gzip
import hashlib
import json
import struct
import subprocess
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
import check_main_joint_scalar752_windows32_20261102 as windows
import main_material_track1120_fixture_20261102 as fixture
from match_main_material_track1120_20261102 import SOURCES

REPORT=ROOT/'evidence/ports/main-material-track1120-windows32-20261102.json'
NATIVE=ROOT/'evidence/matches/main-material-track1120-20261102.json'


def main():
    report=read_json(NATIVE);pin=next(p for p in report['replayDependencies']if p['path'].endswith('.json.gz'))
    assert sha256(ROOT/pin['path'])==pin['sha256']
    cases=json.loads(gzip.decompress((ROOT/pin['path']).read_bytes()))['cases'];assert len(cases)==4096
    chunks=[struct.pack('<I',len(cases))];expected=[]
    for index,row in enumerate(cases):
        page,entry,args,context=fixture.inputs(index)
        assert context==row['context']and hashlib.sha256(page).hexdigest()==row['dataSha256']
        chunks.append(struct.pack('<5I',entry,*args,*([0]*(4-len(args))))+page)
        expected.append((context['expectedReturn'],bytes(page)))
    payload=b''.join(chunks);results=[]
    windows.WORK=ROOT/'work/main-material-track1120-windows32-20261102'
    windows.DRIVER=ROOT/'src/ports/20261102_material_track1120/driver.c'
    for kind in[-1,0,1,2,3]:
        label='preferred'if kind<0 else f'step-{kind}';windows.SOURCES=list(SOURCES)
        if kind>=0:windows.SOURCES[kind]=ROOT/f'nonmatching/integration/20261102-material-track1120/step-{kind}/source.c'
        exe,built=windows.compile_sources(label)
        run=subprocess.run([str(exe)],input=payload,cwd=ROOT.parent,capture_output=True,timeout=60,
         creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,(label,run.returncode,run.stderr)
        stride=16392;assert len(run.stdout)==len(cases)*stride
        rejected=affected_rejected=0;digests=[]
        for index,(value,page)in enumerate(expected):
            offset=index*stride;ordinal,result=struct.unpack_from('<II',run.stdout,offset);assert ordinal==index
            output=run.stdout[offset+8:offset+stride];passed=result==value and output==page;rejected+=not passed
            if kind>=0 and index%4==kind:affected_rejected+=not passed
            digests.append(hashlib.sha256(struct.pack('<I',result)+output).hexdigest())
        assert (rejected==0)==(kind<0),(label,rejected)
        if kind>=0:
            control=next(c for c in report['negativeControls']if c['label']==label)
            assert affected_rejected==control['rejected'],(label,affected_rejected,control)
        results.append(dict(label=label,build=built,actualPublicCalls=len(cases),rejected=rejected,
         affectedNativeControlRejects=affected_rejected,outputDigest=hashlib.sha256(''.join(digests).encode()).hexdigest()))
    write_json(REPORT,dict(passed=True,sourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),
     preferred=results[0],controls=results[1:],actualPreferredPublicCalls=4096,actualWrongPublicCalls=16384,
     unmodifiedTargetSourceBodies=True,separateTranslationUnits=True,functionProviders=0,
     entire16384ByteInputAndReturnCompared=True,nativeReportSha256=sha256(NATIVE),
     fullGame=False,androidDeviceExecutions=0,androidLP64SourcePortabilityProven=False,
     reproductionCommand='python check_main_material_track1120_windows32_20261102.py'))
    print(dict(preferred=4096,wrong=16384,wrongRejected=sum(r['rejected']for r in results[1:])))


if __name__=='__main__':
    main()
