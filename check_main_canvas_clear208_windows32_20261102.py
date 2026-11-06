import gzip
import hashlib
import json
import struct
import subprocess
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
import check_main_joint_scalar752_windows32_20261102 as windows
import main_canvas_clear284_fixture_v2_20261102 as fixture
from match_main_canvas_clear284_v2_20261102 import SOURCES as TARGET_SOURCES
SOURCES=TARGET_SOURCES[1:]

NATIVE=ROOT/'evidence/matches/main-canvas-clear284-v2-20261102.json'
REPORT=ROOT/'evidence/ports/main-canvas-clear208-windows32-20261102.json'


def main():
    report=read_json(NATIVE);pin=next(p for p in report['replayDependencies']if p['path'].endswith('.json.gz'))
    assert sha256(ROOT/pin['path'])==pin['sha256']
    cases=json.loads(gzip.decompress((ROOT/pin['path']).read_bytes()))['cases'];assert len(cases)==3072
    windows.WORK=ROOT/'work/main-canvas-clear208-windows32-20261102';windows.DRIVER=ROOT/'src/ports/20261102_canvas_clear208/driver.c'
    results=[]
    for kind in[-1,1,2]:
        label='preferred'if kind<0 else f'palette-{kind}';paths=list(SOURCES)
        if kind>=0:paths[kind-1]=ROOT/f'nonmatching/integration/20261102-canvas_clear284/{label}/source.c'
        windows.SOURCES=paths;exe,built=windows.compile_sources(label)
        built['unmodifiedSourceInputs']=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in paths]
        indices=[i for i in range(3072)if i%3]if kind<0 else[i for i in range(3072)if fixture.inputs(i)[2]==list(fixture.SPANS)[kind]]
        chunks=[struct.pack('<I',len(indices))];expected=[]
        for index in indices:
            page,output,entry,args,context=fixture.inputs(index);assert hashlib.sha256(output).hexdigest()==cases[index]['dataSha256']
            chunks.append(struct.pack('<9I',entry,*args,*([0]*(8-len(args))))+page);expected.append(output)
        run=subprocess.run([str(exe)],input=b''.join(chunks),cwd=ROOT.parent,capture_output=True,timeout=60,creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,(label,run.returncode,run.stderr)
        stride=16388;assert len(run.stdout)==len(indices)*stride;rejected=0;digests=[]
        for ordinal,wanted in enumerate(expected):
            offset=ordinal*stride;assert struct.unpack_from('<I',run.stdout,offset)[0]==ordinal
            output=run.stdout[offset+4:offset+stride];rejected+=output!=wanted;digests.append(hashlib.sha256(output).hexdigest())
        assert(rejected==0)==(kind<0)
        if kind>=0:assert rejected==next(c['rejected']for c in report['negativeControls']if c['label']==label)
        results.append(dict(label=label,build=built,actualPublicCalls=len(indices),rejected=rejected,positiveControls=len(indices)-rejected,
         outputDigest=hashlib.sha256(''.join(digests).encode()).hexdigest()))
    write_json(REPORT,dict(passed=True,sourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),
     preferred=results[0],controls=results[1:],actualPreferredPublicCalls=2048,actualWrongPublicCalls=2048,
     unmodifiedTargetBodies=True,separateTranslationUnits=True,portableMemoryBackend=dict(function='native_fn_02008c58',compiledInDriver=True,originalArmAssemblyHostBuild=False,sourceByteCredit=0),entire16384ByteInputOutputCompared=True,
     nativeReportSha256=sha256(NATIVE),fullGame=False,renderedUi=False,androidDeviceExecutions=0,
     reproductionCommand='python check_main_canvas_clear208_windows32_20261102.py'))
    print(dict(preferred=2048,wrong=2048,wrongRejected=sum(r['rejected']for r in results[1:])))


if __name__=='__main__':
    main()
