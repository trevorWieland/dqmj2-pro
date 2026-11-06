from project import ROOT,configuration,read_json,write_json,sha256
from arm7_lane_sdk_division_scope_20261031 import validate_scope,MODULE_SHA,SCOPE_SHA,BASE,ENTRY,FIRST,LAST
import hashlib


def main():
    binary=ROOT/'extract/arm7/runtime/arm7-wram.bin';raw=binary.read_bytes();scope=validate_scope(raw)
    evidence=ROOT/'evidence/arm7/sdk-division-scope-20261031.json';report=read_json(evidence)
    assert report['actualOriginalReturns']==152 and report['scope']==scope
    modules=read_json(ROOT/'ledger/modules.json')['modules'];module=next(m for m in modules if m['name']=='arm7-wram' and m['processor']=='arm7' and not m.get('program'))
    assert int(module['base'],0)==BASE and module['sha256']==MODULE_SHA and LAST-BASE<=module['bytes']
    code=FIRST+4;key=f"{configuration()['romSha256']}/arm7/host/arm7-wram/arm/{code:08x}"
    amendment={'identity':key,'buildSha256':configuration()['romSha256'],'processor':'arm7','program':'','module':'arm7-wram','mode':'arm','input':binary.relative_to(ROOT).as_posix(),'inputModuleSha256':MODULE_SHA,
        'nativeEntry':hex(ENTRY),'originalQualifiedWholeSpan':{'start':hex(ENTRY),'endExclusive':hex(LAST),'bytes':LAST-ENTRY,'sha256':SCOPE_SHA},
        'additionalExecutedRange':{'start':hex(code),'endExclusive':hex(LAST),'bytes':LAST-code,'sha256':hashlib.sha256(raw[code-BASE:LAST-BASE]).hexdigest()},
        'excludedAlignment':{'start':hex(FIRST),'endExclusive':hex(code),'bytes':4,'word':'0xe1a00000','notObservedAsInstruction':True},
        'evidence':evidence.relative_to(ROOT).as_posix(),'evidenceSha256':sha256(evidence),'reproduction':['arm7_lane_sdk_division_scope_20261031.py','amend_arm7_division_inventory_20261031.py'],
        'computedDispatch':scope['computedTargetFormula'],'nativeReturns':152,'allEightComputedTargetsCovered':True,'instructionGuards':7,'newFunctionCount':0,'newMatchedBytes':0,'sourceCredit':0,
        'classification':'Verified executable tail reached by the original helper; no reconstructed source or shared candidate boundary replacement',
        'limitations':['This initialized range already contributes to module byte footprint; initialized denominator does not change','No executable-only global denominator is established','Positive-denominator u32 quotient/remainder tests do not prove every helper input or historical assembly provenance']}
    output=ROOT/'ledger/executable-scope-amendments.json';document=read_json(output) if output.exists() else {'schemaVersion':1,'sourceCredit':0,'amendments':[]}
    previous=[a for a in document['amendments'] if a['identity']==key]
    if previous:assert previous==[amendment]
    document['amendments']=[a for a in document['amendments'] if a['identity']!=key]+[amendment];write_json(output,document)
    write_json(ROOT/'evidence/verification/arm7-division-inventory-amendment-20261031.json',{'sourceCredit':0,'passed':True,'ledger':output.relative_to(ROOT).as_posix(),'ledgerSha256':sha256(output),'additionalExecutedBytes':392,'excludedNopBytes':4,'initializedDenominatorChanged':False,'sharedHeuristicBoundaryFilesChanged':False})
    print({'verifiedExecutableTailBytes':392,'excludedNopBytes':4,'newSourceCredit':0,'sharedBoundaryChange':False})


if __name__=='__main__':
    main()
