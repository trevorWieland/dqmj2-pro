import gzip
import hashlib
import json
import struct
import subprocess
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
import check_main_joint_scalar752_windows32_20261102 as windows
import main_material_parents496_fixture_20261102 as fixture
from match_main_material_parents496_20261102 import SOURCES,LEAVES

REPORT=ROOT/'evidence/ports/main-material-parents496-windows32-20261102.json'
NATIVE=ROOT/'evidence/matches/main-material-parents496-20261102.json'


def main():
    report=read_json(NATIVE);pin=next(p for p in report['replayDependencies']if p['path'].endswith('.json.gz'))
    assert sha256(ROOT/pin['path'])==pin['sha256']
    cases=json.loads(gzip.decompress((ROOT/pin['path']).read_bytes()))['cases'];assert len(cases)==1024
    chunks=[struct.pack('<I',len(cases))];expected=[]
    for index,row in enumerate(cases):
        page,output,entry,args,context=fixture.inputs(index)
        assert hashlib.sha256(output).hexdigest()==row['dataSha256']and context==row['context']
        chunks.append(struct.pack('<5I',entry,*args,*([0]*(4-len(args))))+page);expected.append(output)
    payload=b''.join(chunks);results=[]
    windows.WORK=ROOT/'work/main-material-parents496-windows32-20261102'
    windows.DRIVER=ROOT/'src/ports/20261102_material_parents496/driver.c'
    for kind in[-1,0,1]:
        label='preferred'if kind<0 else f'parent-{list(fixture.PARENTS)[kind]:08x}'
        parents=list(SOURCES)
        if kind>=0:parents[kind]=ROOT/f'nonmatching/integration/20261102-material-parents496/{label}/source.c'
        folder=windows.WORK/label;folder.mkdir(parents=True,exist_ok=True);wrapped=[]
        for index,path in enumerate(parents):
            wrapper=folder/f'parent{index}.c'
            wrapper.write_text(''.join(f'#define native_fn_{a} native_main_{a}\n'for a in['02033930','02033a98','02033d48','02033e48'])+
             '#include "'+path.as_posix()+'"\n',encoding='utf-8');wrapped.append(wrapper)
        windows.SOURCES=[*wrapped,*LEAVES];exe,built=windows.compile_sources(label)
        built['unmodifiedSourceInputs']=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in[*parents,*LEAVES]]
        run=subprocess.run([str(exe)],input=payload,cwd=ROOT.parent,capture_output=True,timeout=60,
         creationflags=subprocess.CREATE_NO_WINDOW)
        assert run.returncode==0,(label,run.returncode,run.stderr)
        stride=16388;assert len(run.stdout)==len(cases)*stride
        rejected=affected_rejected=0;digests=[]
        for index,wanted in enumerate(expected):
            offset=index*stride;assert struct.unpack_from('<I',run.stdout,offset)[0]==index
            output=run.stdout[offset+4:offset+stride];passed=output==wanted;rejected+=not passed
            if kind>=0 and index%2==kind:affected_rejected+=not passed
            digests.append(hashlib.sha256(output).hexdigest())
        assert (rejected==0)==(kind<0),(label,rejected)
        if kind>=0:
            control=next(c for c in report['negativeControls']if c['label']==label)
            assert affected_rejected==control['rejected'],(label,affected_rejected,control)
        results.append(dict(label=label,build=built,actualPublicCalls=len(cases),actualCompiledLeafCalls=5*len(cases),
         rejected=rejected,affectedNativeControlRejects=affected_rejected,outputDigest=hashlib.sha256(''.join(digests).encode()).hexdigest()))
    write_json(REPORT,dict(passed=True,sourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),
     preferred=results[0],controls=results[1:],actualPreferredPublicCalls=1024,actualWrongPublicCalls=2048,
     actualPreferredCompiledLeafCalls=5120,unmodifiedTargetSourceBodies=True,separateTranslationUnits=True,functionProviders=0,
     entire16384ByteInputOutputCompared=True,nativeReportSha256=sha256(NATIVE),
     fullGame=False,androidDeviceExecutions=0,androidLP64SourcePortabilityProven=False,
     reproductionCommand='python check_main_material_parents496_windows32_20261102.py'))
    print(dict(preferred=1024,wrong=2048,compiledLeafCalls=5120,wrongRejected=sum(r['rejected']for r in results[1:])))


if __name__=='__main__':
    main()
