from project import ROOT,configuration,verify_inputs,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import validate,measured_module
from match_main_overlap_copy_20261030 import main_references
from main_mmio_view_native_20261031 import cases,execute,ENTRY
from seal_recovery_evidence_20261031 import code_closure

SOURCE='src/runtime/20261031_mmio_views/native_main_0200427c.c'


def negative_controls(original,rebuilt):
    source=(ROOT/SOURCE).read_text(encoding='utf-8-sig');result=[];returns=0
    compiler.WORK=ROOT/'work/main-mmio-view-controls-20261031/compile'
    for name,text in [('wrong-field-mask',source.replace('0x3C','0x1C')),('wrong-mode-boundary',source.replace('mode < 3','mode < 2'))]:
        path=ROOT/f'nonmatching/main-runtime/20261031/mmio-0200427c-{name}.c';path.write_text(text,encoding='utf-8');rows,_=compiler.compare(path,'main',2,'off',False);assert len(rows)==1
        directory=ROOT/'work/main-mmio-view-controls-20261031'/name
        try:validate(rows[0],{},directory=directory)
        except ValueError as error:refusal=str(error)
        else:raise AssertionError('Wrong C matched')
        payload=(directory/'caller.bin').read_bytes();assert len(payload)==72
        arm=bytearray(rebuilt);arm[ENTRY-0x02000000:ENTRY-0x02000000+72]=payload;vectors=[]
        for tag,(mode,half) in enumerate([(0,0x20),(2,0x80),(2,0xA0),(3,0),(3,0x80),(5,0x3C),(6,0),(7,0xFFFF)]):
            native=execute(original,mode,half,tag);wrong=execute(bytes(arm),mode,half,tag,check=False);returns+=2
            vectors.append({'mode':mode,'configuration':half,'nativeResult':native['result'],'wrongResult':wrong['result'],'rejected':not wrong['modelPassed'],'positiveControl':wrong['modelPassed'],'actualReturns':2})
        rejects=sum(v['rejected'] for v in vectors);positives=sum(v['positiveControl'] for v in vectors);assert rejects and positives
        result.append({'name':name,'source':path.relative_to(ROOT).as_posix(),'sourceSha256':sha256(path),'objectSha256':rows[0]['objectSha256'],'wholeCompiledCRealLinked':True,'exactByteRefusal':refusal,'rejections':rejects,'positiveControls':positives,'cases':vectors})
    return {'passed':True,'sourceCredit':0,'actualTopReturns':returns,'functionResultProviders':0,'controls':result}


def main():
    inputs=verify_inputs(configuration());metadata,original,config=measured_module('main');compiler.WORK=ROOT/'work/main-mmio-view-source-20261031/compile'
    rows,_=compiler.compare(ROOT/SOURCE,'main',2,'off',False);assert len(rows)==1;row=rows[0];assert row['exactAfterDeclaredRelocation']
    directory=ROOT/'work/main-mmio-view-source-20261031/linked';proof=validate(row,{},directory=directory);assert proof['exactCallerBytes']
    rebuilt=bytearray(original);rebuilt[ENTRY-0x02000000:ENTRY-0x02000000+72]=(directory/'caller.bin').read_bytes()
    row.update(sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,realMainLink=proof,exactAfterRealMwLink=True,sourceDependencies=[])
    row['boundaries']=dict(main_references(row,original,config),instructionBytes=68,literalPoolBytes=4,generatedLiteralOrPaddingBytes=4)
    results=[];pcs=set();maximum=0
    for tag,(mode,half) in enumerate(cases()):
        a=execute(original,mode,half,tag);b=execute(bytes(rebuilt),mode,half,tag);assert a==b;results.append(a);pcs.update(a['pcs']);maximum=max(maximum,a['state']['instructions'])
    controls=negative_controls(original,bytes(rebuilt));assert verify_inputs(configuration())==inputs
    report={'schemaVersion':1,'romSha256':configuration()['romSha256'],'processor':'arm9','module':'main','matches':rows,'matchedFunctions':1,'matchedBytes':72,'nativeSymbolEntries':{},'generatorSources':[{'path':p,'sha256':sha256(ROOT/p)} for p in code_closure(['match_main_mmio_view_20261031.py'])],
        'oracle':{'pairs':len(results),'actualTopLevelReturns':2*len(results),'functionResultProviders':0,'instructionLimit':200,'maximumInstructions':maximum,'ownInstructionPcs':len(pcs),'orderedMmioReads':[[0x04001000,4],[0x0400100E,2]],'rows':results},'negativeControls':controls,'inputsUnchanged':True,'wholeModuleLinked':False,'sourceCreditAcceptedByThisScript':0,
        'limitations':['Synthetic stable register snapshots validate numerical mode and address behavior; real device timing is not tested','No ownership, current screen, scene, register naming or actual VRAM backing is inferred','No whole-game or Android execution is established','Source adoption awaits registry/module/regression gates']}
    write_json(ROOT/'evidence/matches/main-mmio-view-20261031.json',report);print({'matchedFunctions':1,'bytes':72,'actualTopReturns':2*len(results),'ownInstructionPcs':len(pcs),'negativeReturns':controls['actualTopReturns']})


if __name__=='__main__':
    main()
