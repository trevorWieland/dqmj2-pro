import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
import save_core_controller123_prefix_20261101 as P
from match_mechanics_save_20261029_record33 import file_identity,native_entry,ROM_SHA,SAVE_SHA,MAIN_SHA
from match_mechanics_save_20261031_lane_menu_setup import runtime_files
from match_mechanics_save_20261031_lane_pointer_sequence import unpack


def main():
    P.main();path='evidence/functional/save-core-controller123-prefix-20261101.json';report=json.loads((ROOT/path).read_text());vectors=unpack(report['vectorSidecar'],report['nativeCaseDigest']);assert len(vectors)==796 and report['actualTopReturns']==1592 and report['providers']==0;row=report['match'];source=(ROOT/row['source']).read_text();wrongsource=source.replace('s8 *, 0x26C) != 0x2A','s8 *, 0x26C) != 0x2B');assert wrongsource!=source;wrongpath=ROOT/'nonmatching/save-core/20261101-controller123/wrong_guard.c';wrongpath.write_text(wrongsource);arm=P.B.measured_module('main')[1];P.B.SOURCE=wrongpath.relative_to(ROOT).as_posix();P.B.WORK='work/scc123/wrong_guard';wrong,body=P.B.build(arm[0x70298:0x70564]);controls=[]
    for guard in (0,42,43,255):
        p=P.profile(guard=guard);a=P.Machine(arm,p).run();b=P.Machine(arm,p,body).run();P.validate(a)
        try:P.validate(b);rejected=False
        except AssertionError:rejected=True
        controls.append(dict(guard=guard,actualOriginalReturn=True,actualWrongReturn=True,rejected=rejected,expected=a['returnWord'],wrong=b['returnWord']))
    assert sum(r['rejected'] for r in controls)==2;deps=runtime_files()|{path,report['vectorSidecar']['path'],'evidence/attempts/save-core-controller123-declarations-20261101.json','evidence/attempts/save-core-controller123-role-orders-20261101.json',row['source'],wrong['source'],'prove_save_core_controller123_prefix_20261101.py'};entries={};cache={}
    for a in [P.ENTRY,*P.HELPERS]:entries[hex(a)]=native_entry('main',a,cache)
    for r in [row,wrong]:deps.update(p['path'] for p in r.get('sourceDependencies',[]))
    deps.update(v[0]['symbolsFile'] for v in cache.values());out=dict(schemaVersion=1,romSha256=ROM_SHA,saveSha256=SAVE_SHA,arm9Sha256=MAIN_SHA,sourceCredit=0,matchedBytes=0,exactFunctionMatch=False,report=path,reportSha256=P.B.sha((ROOT/path).read_bytes()),caseDigest=report['nativeCaseDigest'],cases=796,actualTopReturns=1592,additionalControlReturns=8,controlRejects=2,controlPositives=2,completeWrongC=wrong,controls=controls,nativeSymbols=entries,replayDependencies=[file_identity(p) for p in sorted(deps)],replayRequires=[],limits=report['limits']);target=ROOT/'evidence/functional/save-core-controller123-prefix-receipt-20261101.json';target.write_text(json.dumps(out,indent=2)+'\n');print(dict(actualTopReturns=1592,sourceCredit=0,receiptSha256=P.B.sha(target.read_bytes())))


if __name__=='__main__':main()
