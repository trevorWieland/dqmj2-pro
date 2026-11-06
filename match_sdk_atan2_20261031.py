from project import ROOT,write_json,sha256,configuration,verify_inputs
import match_runtime as compiler
from link_runtime_unit import validate,measured_module
from match_main_overlap_copy_20261030 import main_references
from derive_sdk_atan_20261031 import derive
from sdk_atan2_native_20261031 import execute,cases,ENTRY
from seal_recovery_evidence_20261031 import code_closure
import struct

CALLERS=['src/runtime/ov000-drafts01/native_ov000_021e8b20.c','src/runtime/runtime03/native_main_020424f4.c','src/runtime/runtime03/native_main_020420c4.c','src/runtime/runtime05/native_main_0205d25c.c','src/runtime/runtime06/native_main_0202818c.c']
SOURCES=['src/math/20261031_atan2/native_main_020028d8.c','src/math/20261031_atan2/division.c']
BINDINGS={'native_fn_0200235c':{'module':'main','processor':'arm9','kind':'function','mode':'arm','address':'0x0200235c'},'native_fn_02002458':{'module':'main','processor':'arm9','kind':'function','mode':'arm','address':'0x02002458'},'native_fn_020023c4':{'module':'main','processor':'arm9','kind':'function','mode':'arm','address':'0x020023c4'},'native_data_020d7fe0':{'module':'main','processor':'arm9','kind':'data','mode':'data','address':'0x020d7fe0'}}


def build():
    metadata,original,config=measured_module('main');compiler.WORK=ROOT/'work/atan2-source-proof-20261031/compile'
    rebuilt=bytearray(original);rows=[]
    for name in SOURCES:
        found,_=compiler.compare(ROOT/name,'main',2,'off',True)
        for row in found:
            assert row['exactAfterDeclaredRelocation']
            directory=ROOT/'work/atan2-source-proof-20261031'/row['name'];proof=validate(row,BINDINGS,directory=directory);assert proof['exactCallerBytes']
            offset=int(row['address'],0)-0x02000000;rebuilt[offset:offset+row['bytes']]=(directory/'caller.bin').read_bytes()
            row.update(sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,realMainLink=proof,exactAfterRealMwLink=True,isolatedCallerBinary=(directory/'caller.bin').relative_to(ROOT).as_posix(),isolatedCallerBinarySha256=sha256(directory/'caller.bin'),sourceDependencies=[])
            row['relocations']=[{**r,'target':r['symbol'],'targetAddress':BINDINGS[r['symbol']]['address'],'targetMode':BINDINGS[r['symbol']]['mode'],'targetModule':'main','addend':r['explicitAddend']} for r in proof['originalRelocations']]
            pool={0x020028D8:32,0x0200235C:0,0x020023C4:8}[int(row['address'],0)]
            row['boundaries']=dict(main_references(row,original,config),instructionBytes=row['bytes']-pool,literalPoolBytes=pool,generatedLiteralOrPaddingBytes=pool)
            rows.append(row)
    assert len(rows)==3 and sum(r['bytes'] for r in rows)==512
    return original,bytes(rebuilt),rows


def main():
    from audit_selected_call_arity_20261030 import arguments,closing
    import re
    caller_evidence=[]
    for path in CALLERS:
        text=(ROOT/path).read_text(encoding='utf-8-sig')
        assert re.search(r'extern u32 native_fn_020028d8\(\);',text)
        actual=[]
        for m in re.finditer(r'native_fn_020028d8\(',text):
            start=m.end()-1;end=closing(text,start,'(',')');args=arguments(text[start+1:end])
            if args:assert len(args)==2;actual.append(args)
        assert actual;caller_evidence.append({'path':path,'sha256':sha256(ROOT/path),'rawReturnDeclaration':'u32','actualArgumentCounts':[len(a) for a in actual]})
    inputs=verify_inputs(configuration());original,rebuilt,rows=build();table,derivation=derive()
    assert struct.pack('<129h',*table)==original[0xD7FE0:0xD80E2]
    results=[];observed=set();indices=set();helpers=0;devices=0;maximum=0
    for tag,(y,x) in enumerate(cases()):
        a=execute(original,table,y,x,tag);b=execute(rebuilt,table,y,x,tag);assert a==b
        observed.update(a['pcs']);indices.update((address-0x020D7FE0)//2 for address,size in a['lookup']);helpers+=2*a['state']['helperReturns'];devices+=2*a['state']['deviceCompletions'];maximum=max(maximum,a['state']['instructions'])
        results.append(a)
        if len(results)%500==0:print({'returningPairs':len(results)},flush=True)
    from validate_sdk_atan2_20261031 import controls
    negative=controls(original,rebuilt,table)
    assert verify_inputs(configuration())==inputs
    report={'schemaVersion':1,'romSha256':configuration()['romSha256'],'processor':'arm9','module':'main','matches':rows,'matchedFunctions':3,'matchedBytes':512,'newFunctionCandidates':2,'newCodeCandidateBytes':496,'existingWrapperMigrationBytes':16,'nativeSymbolEntries':BINDINGS,'sourceDataByteCredit':0,'independentTableDerivation':derivation,
        'generatorSources':[{'path':p,'sha256':sha256(ROOT/p)} for p in sorted(set(code_closure(['match_sdk_atan2_20261031.py'])+CALLERS))],'incomingCallerEvidence':caller_evidence,
        'oracle':{'pairs':len(results),'actualTopLevelReturns':2*len(results),'actualNestedHelperReturns':helpers,'modeledDeviceCompletions':devices,'functionResultProviders':0,'instructionLimit':10000,'maximumInstructions':maximum,'instructionPcs':len(observed),'ownAtan2InstructionPcs':sum(ENTRY<=p<ENTRY+408 for p in observed),'distinctTableIndices':len(indices),'rows':results},'negativeControls':negative,'inputsUnchanged':True,'wholeModuleLinked':False,'registrationPerformed':False,
        'limitations':['Two new C functions and a zero-byte-credit typed forwarding migration await module integration','The independently derived 129-element atan table has no accepted or compiled source-data credit here','Positive signed64/signed32 division completion and zero-to-three BUSY reads are modeled device effects, not function-result providers or real timing','Actual original divider helpers execute; their returns are counted separately','Quotient is stable after BUSY clears in this isolated device contract; C uses a target-aligned ordinary u64 ready-value load and a volatile polling control','INT_MIN coordinates, division by zero, negative divider inputs, interrupts, hardware contention and real device execution are unsupported','Existing historical wrapper source remains unchanged; typed forwarding is a separate migration candidate','The angle function exposes a raw u32 return boundary consistent with five retained callers; calculated values remain explicitly narrowed and sign-extended from16 bits']}
    write_json(ROOT/'evidence/matches/sdk-atan2-20261031.json',report)
    print({'functions':3,'candidateNewBytes':496,'migrationBytes':16,'actualTopReturns':2*len(results),'nestedHelperReturns':helpers,'distinctTableIndices':len(indices),'maximumInstructions':maximum})


if __name__=='__main__':
    main()
