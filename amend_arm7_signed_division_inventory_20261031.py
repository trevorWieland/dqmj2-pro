import hashlib
from project import ROOT,configuration,read_json,write_json,sha256
from arm7_lane_sdk_signed_division_scope_20261031 import validate_scope,BASE,ENTRY,FIRST,LAST,END,MODULE_SHA,SCOPE_SHA


def main():
    binary=ROOT/'extract/arm7/runtime/arm7-wram.bin';raw=binary.read_bytes();scope=validate_scope(raw)
    path=ROOT/'evidence/arm7/sdk-signed-division-scope-20261031.json';report=read_json(path)
    assert report['scope']==scope and report['actualOriginalReturns']==138 and report['negativeControls']==7 and report['allPassed']
    assert not report['zeroOrNegativeDenominatorSupported'] and all(r['actualReturn'] for r in report['records'])
    modules=read_json(ROOT/'ledger/modules.json')['modules'];module=next(m for m in modules if m['name']=='arm7-wram' and m['processor']=='arm7' and not m.get('program'))
    assert int(module['base'],0)==BASE and module['sha256']==MODULE_SHA and END-BASE<=module['bytes']
    begin=FIRST+4;key=f"{configuration()['romSha256']}/arm7/host/arm7-wram/arm/{begin:08x}"
    amendment={'identity':key,'buildSha256':configuration()['romSha256'],'processor':'arm7','program':'','module':'arm7-wram','mode':'arm','input':binary.relative_to(ROOT).as_posix(),'inputModuleSha256':MODULE_SHA,'nativeEntry':hex(ENTRY),
        'originalQualifiedWholeSpan':{'start':hex(ENTRY),'endExclusive':hex(END),'bytes':END-ENTRY,'sha256':SCOPE_SHA},
        'additionalExecutedRange':{'start':hex(begin),'endExclusive':hex(LAST),'bytes':LAST-begin,'sha256':hashlib.sha256(raw[begin-BASE:LAST-BASE]).hexdigest()},
        'excludedAlignment':{'start':hex(FIRST),'endExclusive':hex(begin),'bytes':4,'word':'0xe1a00000','notObservedAsInstruction':True},
        'alreadyInventoriedEpilogue':{'start':hex(LAST),'endExclusive':hex(END),'bytes':END-LAST},
        'evidence':path.relative_to(ROOT).as_posix(),'evidenceSha256':sha256(path),'reproduction':['arm7_lane_sdk_signed_division_scope_20261031.py','amend_arm7_signed_division_inventory_20261031.py'],
        'computedDispatch':scope['computedTargetFormula'],'nativeReturns':138,'instructionGuards':7,'allEightComputedTargetsCovered':len(report['computedTargets'])==8,'newFunctionCount':0,'newMatchedBytes':0,'sourceCredit':0,
        'classification':'Executed original signed-divide tail omitted from a heuristic entry range; zero reconstructed-source or assembly-provenance credit',
        'limitations':['Only signed numerators and positive signed denominators are qualified','Initialized byte denominator already includes this range and is unchanged','No executable-only global denominator, complete runtime ABI or original assembly provenance is established','Shared heuristic boundaries and the frozen unsigned amendment are unchanged']}
    assert amendment['additionalExecutedRange']['bytes']==388 and amendment['alreadyInventoriedEpilogue']['bytes']==20
    output=ROOT/'ledger/executable-scope-amendments-signed.json';write_json(output,{'schemaVersion':1,'sourceCredit':0,'amendments':[amendment]})
    write_json(ROOT/'evidence/verification/arm7-signed-division-inventory-amendment-20261031.json',{'sourceCredit':0,'passed':True,'ledger':output.relative_to(ROOT).as_posix(),'ledgerSha256':sha256(output),'additionalExecutedBytes':388,'excludedNopBytes':4,'existingEpilogueBytes':20,'initializedDenominatorChanged':False,'sharedHeuristicBoundaryFilesChanged':False,'unsignedAmendmentUnchanged':True})
    print({'executedTailBytes':388,'excludedNopBytes':4,'newSourceCredit':0})


if __name__=='__main__':main()
