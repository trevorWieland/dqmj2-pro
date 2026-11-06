import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
import save_core_item_caller_fixtures_20261031 as P
from match_mechanics_save_20261029_record33 import verify_inputs,sha,file_identity
from match_mechanics_save_20261031_lane_pointer_sequence import unpack
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
CASE='8b862875f8f53f60c32237ef49625df5de77fe4bb29121822d44ab0ea5b33cb1'
SOURCE='src/mechanics_save/20261031_lane_item_byte/native_main_02066a7c.c'
SOURCE_SHA='f359b97caed21cd1bab9a3399d9e2a77d98b528571407f28e6cbbb6d19f766da'
PROFILE='evidence/lanes/save-core/item-byte-profile-20261031.json'
PROFILE_SHA='f5ef30da138898c7a27830c1e41e53d6a4e8f233ca3be110216f2158f54e8921'
REPORT='evidence/application/save-core-item-caller-source-20261031.json'


def main():
    import unicorn
    assert sys.version_info[:3]==(3,13,5) and unicorn.__version__=='2.1.4';verify_inputs();assert sha((ROOT/SOURCE).read_bytes())==SOURCE_SHA and sha((ROOT/PROFILE).read_bytes())==PROFILE_SHA
    P.main();r=json.loads((ROOT/REPORT).read_text());vectors=unpack(r['vectorSidecar'],CASE);assert len(vectors)==1907
    assert r['counts']['actualOriginalAndCorrectSourceTopReturns']==3814 and r['counts']['actualWrongSelectorCallerReturns']==1907 and r['counts']['independentWrongSelectorRejections']==1254 and r['counts']['observationalPositiveControls']==653
    assert r['counts']['nativeDependencyReturnsOriginalAndSource']==29494 and r['counts']['suppliedEffectCallsOriginalAndSource']==1416 and r['counts']['sourceCredit']==0
    assert all(v['native']['actualReturn'] and v['wrongSelector']['actualReturn'] for v in vectors)
    row=r['matchedSelector'];assert row['sourceSha256']==SOURCE_SHA and row['exactByteEqual'] and row['compiledBytes']==32
    link=row['realLinkSnapshot'];proof=json.loads((ROOT/link['isolatedCallerLinkValidation']).read_text());assert proof['exactCallerBytes'] and proof['sourceSha256']==SOURCE_SHA and proof['sourceObjectSha256']==row['objectSha256']
    assert sha((ROOT/row['object']).read_bytes())==row['objectSha256'] and sha((ROOT/link['isolatedCallerBinary']).read_bytes())==link['isolatedCallerBinarySha256']
    deps=runtime_files()|{REPORT,PROFILE,SOURCE,r['compiledWrongSelector']['source'],r['vectorSidecar']['path'],'prove_save_core_item_caller_20261031.py','evidence/application/save_core_item_caller_fixtures_20261031.py','evidence/application/save_core_item_caller_machine_20261031.py','provenance/seed-manifest.json'}
    for module in ('main','ov001'):deps.add(P.Q.B.measured_module(module)[0]['symbolsFile'])
    out=dict(schemaVersion=1,sourceCredit=0,romSha256=r['romSha256'],saveSha256=r['saveSha256'],arm9Sha256=r['arm9Sha256'],counts=r['counts'],nativeCaseDigest=CASE,report=REPORT,reportSha256=sha((ROOT/REPORT).read_bytes()),sourceSha256=SOURCE_SHA,nativeEntries=r['nativeEntries'],replayRequires=[],replayDependencies=[file_identity(p) for p in sorted(deps)],limitations=r['limitations'])
    target=ROOT/'evidence/functional/mechanics-save-item-caller-20261031.json';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(out,indent=2)+'\n');verify_inputs();print(dict(receiptSha256=sha(target.read_bytes()),caseDigest=CASE,counts=r['counts']))


if __name__=='__main__':main()
