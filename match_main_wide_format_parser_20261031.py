from project import ROOT,write_json,sha256,configuration,read_json
import match_runtime as compiler
from link_runtime_unit import validate,measured_module
from main_wide_format_parser_native_20261031 import execute,cases
from seal_recovery_evidence_20261031 import code_closure
from match_main_overlap_copy_20261030 import main_references


def main():
    compiler.WORK=ROOT/'work/wide-format-parser-proof-20261031/compile'
    metadata,original,module_config=measured_module('main')
    source=ROOT/'src/runtime/20261031_wide_format_parser/native_main_0201f2c0.c'
    rows,_=compiler.compare(source,'main',3,'off',speed=True)
    assert len(rows)==1 and rows[0]['exactAfterDeclaredRelocation']
    row=rows[0]
    bindings={'native_data_020d8f14':{'processor':'arm9','module':'main','kind':'data','mode':'data','address':'0x020d8f14'}}
    directory=ROOT/'work/wide-format-parser-proof-20261031/linked'
    proof=validate(row,bindings,directory=directory);assert proof['exactCallerBytes']
    row['relocations']=[{**r,'target':r['symbol'],'targetAddress':bindings[r['symbol']]['address'],'targetMode':bindings[r['symbol']]['mode'],'targetModule':'main','addend':r['explicitAddend']} for r in proof['originalRelocations']]
    compiled=bytearray(original);compiled[0x1F2C0:0x1F2C0+1400]=(directory/'caller.bin').read_bytes()
    row.update(sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,exactAfterRealMwLink=True,realMwldProof=proof,isolatedCallerBinary=(directory/'caller.bin').relative_to(ROOT).as_posix(),isolatedCallerBinarySha256=sha256(directory/'caller.bin'),sourceDependencies=[])
    results=[];coverage=set();maximum=0
    for tag,case in enumerate(cases()):
        native=execute(original,case,tag);rebuilt=execute(bytes(compiled),case,tag);assert native==rebuilt
        coverage.update(native['pcs']);maximum=max(maximum,native['instructions'])
        text=case[0] if isinstance(case[0],str) else case[0].decode('latin1')
        results.append({'formatCodeUnits':[ord(x) for x in text],'arguments':list(case[1]),'result':native})
        if len(results)%300==0:print({'returningPairs':len(results)},flush=True)
    from validate_main_wide_format_parser_20261031 import main as negative_controls
    negative_controls()
    controls=read_json(ROOT/'evidence/verification/main-wide-format-parser-controls-20261031.json')
    assert controls['passed'] and controls['actualTopLevelReturns']==24
    row['boundaries']=dict(main_references(row,original,module_config),instructionBytes=1388,literalPoolBytes=12,ordinaryCInstructionBytes=1388,generatedLiteralOrPaddingBytes=12)
    report={'schemaVersion':1,'romSha256':configuration()['romSha256'],'processor':'arm9','module':'main','matches':[row],'matchedFunctions':1,'matchedBytes':1400,'nativeSymbolEntries':bindings,
        'generatorSources':[{'path':p,'sha256':sha256(ROOT/p)} for p in code_closure(['match_main_wide_format_parser_20261031.py'])],
        'oracle':{'pairs':len(results),'actualOriginalAndSourceReturns':2*len(results),'providedCalls':0,'ownInstructionPcsObserved':len(coverage),'maximumInstructions':maximum,'instructionLimit':10000,'rows':results},
        'negativeControls':controls,'registrationPerformedByThisScript':False,'wholeModuleLinked':False,'limitations':['Bounded UTF16 formats and argument buffers are synthetic','Raw128-plus code units are exercised without locale/text-meaning claims','The sole format padding byte copies stack poison and has no semantic field meaning','Invalid pointers, arbitrary strings, decimal integer overflow and INT_MIN width negation remain unsupported','Full module adoption remains pending; wrong-long-kind and byte-classification C controls reject as measured']}
    write_json(ROOT/'evidence/matches/main-wide-format-parser-20261031.json',report)
    print({'matchedFunctions':1,'bytes':1400,'actualReturns':2*len(results),'instructionPcs':len(coverage),'maximumInstructions':maximum})


if __name__=='__main__':
    main()
