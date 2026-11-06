from project import ROOT,configuration,verify_inputs,read_json,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from seal_recovery_evidence_20261031 import code_closure
import match_sdk_trig_data_20261031 as data

SOURCE='src/math/20261031_trig/sincos_wrappers.c'
SOURCE_HASH='19321dc82cf6e9af57b57b106c3b2ff0e9902e7a451c03d6aba764aecadcfb2a'
WORK=ROOT/'work/sdk-trig-wrappers-proof-20261031'


def main():
    inputs=verify_inputs(configuration())
    assert sha256(ROOT/SOURCE)==SOURCE_HASH
    data.WORK=WORK/'table-rebuild'
    data_row,derivation,unused,data_arm=data.compile_data()
    compiler.WORK=WORK/'compile'
    attempts,_=compiler.compare(ROOT/SOURCE,'main',2,'off')
    assert len(attempts)==3 and all(row['compiledBytes']==row['bytes']==92 for row in attempts)
    bindings={};rows=[];source_wrappers=[]
    for row in attempts:
        local_bindings=qualified_bindings(row)
        for name,item in local_bindings.items():
            assert name not in bindings or bindings[name]==item
            bindings[name]=item
        directory=WORK/row['name']
        proof=validate(row,local_bindings,directory=directory)
        assert proof['exactCallerBytes']
        binary=directory/'caller.bin'
        assert sha256(binary)==proof['nativeSpanSha256']==proof['linkedCallerSha256']
        source_wrappers.append({'address':row['address'],'binary':binary.relative_to(ROOT).as_posix(),'sha256':sha256(binary)})
        row.update(sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,
            theoreticalRelocationMatchingBytes=row['matchingBytes'],theoreticalRelocationOutputSha256=row['outputSha256'],
            exactBytes=True,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,matchingBytes=92,
            outputSha256=proof['linkedCallerSha256'],realMwldProof=proof,
            isolatedCallerBinary=binary.relative_to(ROOT).as_posix(),isolatedCallerBinarySha256=sha256(binary),sourceDependencies=[])
        rows.append(row)
    from sdk_trig_native_oracle_20261031 import main as run_oracle
    run_oracle(source_wrappers=source_wrappers,source_table=(data.WORK/'sincos-linked.bin').relative_to(ROOT).as_posix())
    oracle=read_json(ROOT/'evidence/verification/sdk-trig-source-wrappers-20261031.json')
    assert oracle['actualTopLevelReturns']==8258 and oracle['compiledOrdinaryWrapperBytes']==276
    from validate_sdk_trig_wrappers_20261031 import main as negative_controls
    negative_controls()
    controls=read_json(ROOT/'evidence/verification/sdk-trig-wrapper-controls-20261031.json')
    assert controls['passed'] and controls['actualTopLevelReturns']==36
    assert verify_inputs(configuration())==inputs
    dependencies=code_closure(['match_sdk_trig_wrappers_20261031.py'])
    dependencies.append(data.SOURCE)
    report={'schemaVersion':1,'romSha256':configuration()['romSha256'],'arm9Sha256':sha256(data_arm),
        'matches':rows,'matchedFunctions':3,'matchedBytes':276,'nativeSymbolEntries':bindings,
        'nativeSymbols':{name:item['address'] for name,item in bindings.items()},'oracle':oracle,'negativeControls':controls,
        'sourceDependencies':[],'generatorSources':[{'path':path,'sha256':sha256(ROOT/path)} for path in sorted(set(dependencies))],
        'tableDataCreditInThisReport':0,'tableRequiredBySource':'evidence/data/sdk-trig-table-20261031.json',
        'sourceTableInput':{'path':data.SOURCE,'sha256':data_row['sourceSha256']},
        'cArithmetic':'Unsigned64 multiplication/addition wrap before the16-bit phase narrowing; signed32 input is explicitly extended before conversion',
        'inputsUnchanged':True,'registrationPerformedByThisScript':False,'wholeModuleLinked':False,
        'limitations':['Original Thumb matrix callees execute and receive no duplicate source credit','Synthetic raw angles and independent matrix memory models do not establish current game scene state','Whole-module adoption and source-ledger registration remain pending; wrong-bias and unsigned-angle C controls pass their expected rejection/positive checks']}
    write_json(ROOT/'evidence/matches/sdk-trig-wrappers-20261031.json',report)
    print({'functions':3,'ordinaryCBytes':276,'actualTopLevelReturns':oracle['actualTopLevelReturns'],'providedCalls':0,'acceptedSourceCredit':0})


if __name__=='__main__':
    main()
