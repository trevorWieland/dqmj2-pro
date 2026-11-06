import gzip
import hashlib
import json
import struct
import subprocess
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
import check_main_joint_scalar752_windows32_20261102 as windows
import main_canvas_areas1224_fixture_20261102 as fixture
from match_main_canvas_areas1224_20261102 import SOURCES

NATIVE=ROOT/'evidence/matches/main-canvas_areas1224-20261102.json'
REPORT=ROOT/'evidence/ports/main-canvas_areas1224-windows32-20261102.json'


def main():
    report=read_json(NATIVE);pin=next(p for p in report['replayDependencies']if p['path'].endswith('.json.gz'))
    assert sha256(ROOT/pin['path'])==pin['sha256']
    cases=json.loads(gzip.decompress((ROOT/pin['path']).read_bytes()))['cases'];assert len(cases)==3072
    windows.WORK=ROOT/'work/main-canvas_areas1224-windows32-20261102';windows.DRIVER=ROOT/'src/ports/20261102_canvas_areas1224/driver.c'
    results=[]
    for kind in[-1,0,1,2]:
        label='preferred'if kind<0 else f'palette-{kind}';paths=list(SOURCES)
        if kind>=0:paths[kind]=ROOT/f'nonmatching/integration/20261102-canvas_areas1224/{label}/source.c'
        folder=windows.WORK/label;folder.mkdir(parents=True,exist_ok=True);wrapped=[]
        for number,path in enumerate(paths):
            wrapper=folder/f'unit-source-{number}.c'
            wrapper.write_text('#define native_fn_02035650 native_main_02035650\n#include "'+path.as_posix()+'"\n',encoding='utf-8');wrapped.append(wrapper)
        windows.SOURCES=wrapped;exe,built=windows.compile_sources(label)
        built['unmodifiedSourceInputs']=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in paths]
        indices=list(range(3072))if kind<0 else[i for i in range(3072)if fixture.inputs(i)[2]==list(fixture.OWN)[kind]]
        chunks=[struct.pack('<I',len(indices))];expected=[]
        for index in indices:
            page,output,entry,args,context=fixture.inputs(index);assert hashlib.sha256(output).hexdigest()==cases[index]['dataSha256']
            chunks.append(struct.pack('<9I',entry,*args,*([0]*(8-len(args))))+page);expected.append(output)
        run=subprocess.run([str(exe)],input=b''.join(chunks),cwd=ROOT.parent,capture_output=True,timeout=60,creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,(label,run.returncode,run.stderr)
        stride=32772;assert len(run.stdout)==len(indices)*stride;rejected=0;digests=[]
        for ordinal,wanted in enumerate(expected):
            offset=ordinal*stride;assert struct.unpack_from('<I',run.stdout,offset)[0]==ordinal
            output=run.stdout[offset+4:offset+stride];rejected+=output!=wanted;digests.append(hashlib.sha256(output).hexdigest())
        assert(rejected==0)==(kind<0)
        if kind>=0:assert rejected==next(c['rejected']for c in report['negativeControls']if c['label']==label)
        results.append(dict(label=label,build=built,actualPublicCalls=len(indices),rejected=rejected,positiveControls=len(indices)-rejected,
         outputDigest=hashlib.sha256(''.join(digests).encode()).hexdigest()))
    write_json(REPORT,dict(passed=True,sourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),
     preferred=results[0],controls=results[1:],actualPreferredPublicCalls=3072,actualWrongPublicCalls=3072,
     unmodifiedTargetBodies=True,separateTranslationUnits=True,portableBackends=dict(wordFill=True,powerOfTwoObjectBlockIndex=True,originalArmByteCredit=0),entire32768ByteInputOutputCompared=True,
     nativeReportSha256=sha256(NATIVE),fullGame=False,renderedUi=False,androidDeviceExecutions=0,
     reproductionCommand='python check_main_canvas_areas1224_windows32_20261102.py'))
    print(dict(preferred=3072,wrong=3072,wrongRejected=sum(r['rejected']for r in results[1:])))


if __name__=='__main__':
    main()
