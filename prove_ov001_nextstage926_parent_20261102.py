import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import match_runtime
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
import ov001_nextstage924_fixture_20261102 as F
import ov001_selector917_model_20261102 as G


def compact(result):
    return {k:v for k,v in result.items()if k!='memory'}|dict(completeRamSha256=hashlib.sha256(result['memory']).hexdigest())


def execute():
    mainInfo,main,unused=measured_module('main')
    moduleInfo,overlay,unused=measured_module('ov001')
    inverse=pow(0x41C64E6D,-1,1<<32)
    totals=dict(actualTopReturns=0,firstDispatcherReturns=0,secondDispatcherReturns=0,actualNestedPhysicalReturns=0,suppliedCalls=0,constructorCalls=0)
    rows=[]
    for base in F.profiles():
        if base['timer']not in[0,1,39,40,89,90,95,110,111,255]:continue
        p=dict(base,selector=12,subphase=110,threshold=1000,seed=(-0x3039*inverse)&0xFFFFFFFF)
        vm=F.Machine(main,overlay,None,p)
        first=vm.run(F.B.ENTRY)
        expected=bytearray(vm.beforeState)
        expected[0xA]=13
        expected[0xF]=0
        if first['stateHex']!=expected.hex()or first['rngState']!=0 or first['registers'][0]!=0:
            raise ValueError('926 original selector writer model differs')
        if [r['entry']for r in first['nativeEntries']]!=[hex(F.B.SELECTOR),'0x205fd60','0x203d294','0x2026350']:
            raise ValueError('926 actual selector initializer call order differs')
        if G.logical_providers(first)!=[dict(target=hex(F.B.NOTICE),consumedWords=[0,1],returnWord=0xC0DEC0DE)]:
            raise ValueError('926 original notification contract differs')
        vm.beforeState=bytes(expected)
        second=vm.run(F.B.ENTRY)
        ownResult=dict(second,nativeEntries=[],nativePhysicalReturns=[])
        shadow=type('View',(),dict(p=dict(p,seed=0),beforeState=bytes(expected)))()
        failures=F.model(shadow,ownResult)
        if failures:raise ValueError(('926 independent handler model differs',p['ordinal'],failures))
        if [r['entry']for r in second['nativeEntries']]!=[hex(F.ENTRY)]or[r['entry']for r in second['nativePhysicalReturns']]!=[hex(F.ENTRY)]:
            raise ValueError('926 actual handler call/return differs')
        totals['actualTopReturns']+=2
        totals['firstDispatcherReturns']+=1
        totals['secondDispatcherReturns']+=1
        totals['actualNestedPhysicalReturns']+=len(first['nativePhysicalReturns'])+len(second['nativePhysicalReturns'])
        totals['suppliedCalls']+=len(first['provided'])+len(second['provided'])
        totals['constructorCalls']+=sum(r['target']=='0x21fb214'for r in second['provided'])
        rows.append(dict(profile=p,first=compact(first),second=compact(second),allPassed=True))
    raw=json.dumps(rows,sort_keys=True,separators=(',',':')).encode()
    artifact=ROOT/'evidence/generated/ov001-nextstage926-parent-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,allPassed=True,sourceCredit=0,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',mode='arm',moduleSha256=moduleInfo['sha256'],mainSha256=mainInfo['sha256'],totals=totals,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=hashlib.sha256(raw).hexdigest()),limits=['Original dispatcher021FBD6C first executes original021FAFEC from supplied selector12/subphase0x6E, threshold1000 and inverse-LCG seed yielding RNG(1000)=0. Actual write at021FB1A4 establishes selector13.','The second test-driver invocation of the SAME original dispatcher occurs on unchanged resulting RAM; selector13 then enters actual296-byte021FB7AC. Timer raw byte+1 was supplied before first call; it is not proved to be ordinary initialized scene timing.','Ten timer values and three supplied wait statuses are tested. At timer95 and supplied wait0, actual caller passes fullu32 state+40 to suppliedFB214, ignores its return and stores timer110. At timer110 it clears timer and writes selector15. Full lower constructor behavior remains unproved; prefix922 is separate.','No code/branch patches or artificial PC routing. Native parent/selector/RNG/division/wait getter and handler execute. Notification and handler services are explicitly supplied with legal caller-saved/NZCV clobbers and no memory effects. Raw input words are retained.','Top returns60 and nested physical returns150 are separate actual counts; no duplicate source credit. Initialized actor/timer/threshold/seed/wait fields, unknown service effects, ordinary scene reachability and future state remain explicit limitations. No application/host/device or module/ROM completion claim.'])
    write_json(ROOT/'evidence/application/ov001-nextstage926-parent-20261102.json',report)
    print(totals,flush=True)

if __name__=='__main__':execute()
