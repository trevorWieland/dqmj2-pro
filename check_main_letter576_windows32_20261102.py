import gzip
import hashlib
import json
import struct
import subprocess
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
import check_main_joint_scalar752_windows32_20261102 as windows
import main_letter576_fixture_20261102 as fixture
from match_main_letter576_20261102 import SOURCE,HELPER

NATIVE=ROOT/'evidence/matches/main-letter576-20261102.json'
REPORT=ROOT/'evidence/ports/main-letter576-windows32-20261102.json'


def main():
    report=read_json(NATIVE);pin=next(p for p in report['replayDependencies']if p['path'].endswith('.json.gz'))
    assert sha256(ROOT/pin['path'])==pin['sha256']
    cases=json.loads(gzip.decompress((ROOT/pin['path']).read_bytes()))['cases'];assert len(cases)==2048
    windows.WORK=ROOT/'work/main-letter576-windows32-20261102';windows.DRIVER=ROOT/'src/ports/20261102_letter576/driver.c'
    results=[]
    for label in['preferred','transparency','palette']:
        source=SOURCE if label=='preferred'else ROOT/f'nonmatching/integration/20261102-letter576/{label}/source.c'
        folder=windows.WORK/label;folder.mkdir(parents=True,exist_ok=True);wrapper=folder/'letter.c'
        wrapper.write_text('#define native_fn_02034ab8 native_main_02034ab8\n#include "'+source.as_posix()+'"\n',encoding='utf-8')
        windows.SOURCES=[wrapper,HELPER];exe,built=windows.compile_sources(label)
        built['unmodifiedSourceInputs']=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in[source,HELPER]]
        count=2048 if label=='preferred'else 512;chunks=[struct.pack('<I',count)];expected=[]
        for index in range(count):
            page,output,args,context=fixture.inputs(index);assert hashlib.sha256(output).hexdigest()==cases[index]['dataSha256']
            chunks.append(struct.pack('<II',fixture.ENTRY,args[0])+page);expected.append(output)
        run=subprocess.run([str(exe)],input=b''.join(chunks),cwd=ROOT.parent,capture_output=True,timeout=60,creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,(label,run.returncode,run.stderr)
        stride=16388;assert len(run.stdout)==count*stride
        rejected=0;digests=[]
        for index,wanted in enumerate(expected):
            offset=index*stride;assert struct.unpack_from('<I',run.stdout,offset)[0]==index
            output=run.stdout[offset+4:offset+stride];rejected+=output!=wanted;digests.append(hashlib.sha256(output).hexdigest())
        assert(rejected==0)==(label=='preferred')
        if label!='preferred':assert rejected==next(c['rejected']for c in report['negativeControls']if c['label']==label)
        results.append(dict(label=label,build=built,actualPublicCalls=count,rejected=rejected,positiveControls=count-rejected,
         outputDigest=hashlib.sha256(''.join(digests).encode()).hexdigest()))
    write_json(REPORT,dict(passed=True,sourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),
     preferred=results[0],controls=results[1:],actualPreferredPublicCalls=2048,actualWrongPublicCalls=1024,
     unmodifiedTargetAndSelectedBitReaderBodies=True,separateTranslationUnits=True,functionProviders=0,
     entire16384ByteInputOutputCompared=True,nativeReportSha256=sha256(NATIVE),fullGame=False,renderedUi=False,androidDeviceExecutions=0,
     reproductionCommand='python check_main_letter576_windows32_20261102.py'))
    print(dict(preferred=2048,wrong=1024,wrongRejected=sum(r['rejected']for r in results[1:])))


if __name__=='__main__':
    main()
