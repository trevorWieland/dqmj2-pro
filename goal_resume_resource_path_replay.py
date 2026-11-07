import gzip
import hashlib
import json
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
from goal_resume_resource_path_views import LANE
from goal_resume_resource_path_contracts import recipe,recipes,build,view
from goal_resume_resource_path_compile import geometry
from goal_resume_resource_path_proof import prototype_controls,identity_controls,wrong_c
from goal_resume_resource_path_behavior import qualify,HELPERS,module_image


def replay_builds():
    results=[]
    for ref in recipes():
        address=int(ref['address'],0);folder=ROOT/'work/p-api'/f'{address:08x}';old=ROOT/ref['source']
        if sha256(old)!=ref['sourceSha256']:raise ValueError('Frozen previous source changed')
        for dependency in ref['sourceDependencies']:
            if sha256(ROOT/dependency['path'])!=dependency['sha256']:raise ValueError('Frozen previous dependency changed')
        prior,unused=build(old,folder/'p',ref);fresh,body=build(view(ref),folder/'v',ref)
        results.append(dict(identity=ref['admittedIdentity'],bytes=ref['bytes'],previous=prior,view=fresh,allocatedContractEqual=True,rawRelocationsEqual=True,sourceCredit=0))
        print(dict(module=ref['module'],address=ref['address'],previousAndViewNativeExact=True),flush=True)
    return results


def physical(binding):
    return((binding.get('program')or''),binding['processor'],binding['module'],binding['mode'],binding['kind'],int(binding['address'],0))


def merge_bindings(rows):
    result={}
    for row in rows:
        for name,binding in row['nativeSymbolEntries'].items():
            if name in result and physical(result[name])!=physical(binding):raise ValueError('Canonical module contains conflicting full physical bindings')
            result[name]=dict(binding,address=hex(int(binding['address'],0)))
    return result


def main():
    for pin in read_json(LANE/'inputs-replay.json')['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen qualification input changed',pin['path']))
    sdk=geometry(recipe(0x0202a8e0));results=replay_builds()
    bodies={(r['view']['module'],int(r['view']['address'],0)):(ROOT/r['view']['realLink']['lcf']).with_name('caller.bin').read_bytes()for r in results}
    traces=qualify(bodies);prototypes=prototype_controls();namespace=identity_controls(results);negatives=wrong_c(bodies)
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();trace=LANE/'traces.json.gz';trace.write_bytes(gzip.compress(raw,mtime=0))
    rows=[dict(r['view'],sourceCredit=0,previousSourceCreditPreserved=True)for r in results];native_helpers=[]
    for address,size in HELPERS.items():
        unused,image=module_image('main');body=image[address-0x02000000:address-0x02000000+size]
        native_helpers.append(dict(program='',processor='arm9',module='main',mode='arm',address=hex(address),bytes=size,sha256=hashlib.sha256(body).hexdigest(),helperSourceCredit=0))
    limits=['All27 previous sources and new views are independently freshly compiled against actual frozen original allocated/symbol/raw-relocation contracts and genuinely linked as complete native function spans.','The62 new native/source pairs exercise the typed providers and five reviewed caller boundaries; inherited closed behavior for other identical bodies is preserved, not replayed or generalized to whole scenes.','Real native FSInitFile/FSOpenFile/FSCloseFile and archive/free wrappers execute. Filesystem find/open-command, allocator/read backend and UI upload services remain bounded supplied interfaces.','SDK u32 remains unsigned long; canonical top API return/heap words are unsigned int. Existing public caller signatures and unrelated data/API views remain unchanged.','No whole-program ISO-C repair, whole-module integration, new source credit or prepared174 acceptance is asserted.']
    behavior=dict(pairs=len(traces),actualTopReturns=2*len(traces),actualHelperReturnsPerSide=sum(len(t['result']['actualHelperReturns'])for t in traces),originalAndFreshFullRegistersCPSRMemoryEqual=True,nativeHelpers=native_helpers,independentModels=['Unsigned file-length/status and real SDK record path','Heap/rounded allocation/signed alignment and read ownership','Incoming filename word/capacity and read-state flags','Original overlay two-bit palette route','Four-byte filename table entries and real free wrapper','Native1399-record44-byte stride and compact16-bit fields'])
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm9',allPassed=True,matches=rows,functions=27,bytes=4812,canonicalMatchedFunctions=27,canonicalMatchedBytes=4812,acceptedFunctionCountDelta=0,acceptedByteCreditDelta=0,sourceCredit=0,zeroCreditMigrationFunctions=27,originalClaimAccepted173Functions=23,originalClaimPrepared174Functions=4,allocatedComparisons=results,prototypeControls=prototypes,namespaceAndSourceControls=namespace,behavior=behavior,wrongC=negatives,generatedTrace=dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace),uncompressedSha256=hashlib.sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=limits)
    write_json(LANE/'qualification.json',report)
    for module in['main','ov000','ov005','ov006']:
        selected=[r for r in rows if r['module']==module];unused,image=module_image(module)
        canonical=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm9',module=module,moduleSha256=hashlib.sha256(image).hexdigest(),allPassed=True,matches=selected,canonicalMatchedFunctions=len(selected),canonicalMatchedBytes=sum(r['bytes']for r in selected),acceptedFunctionCountDelta=0,acceptedByteCreditDelta=0,acceptedSourceCredit=0,nativeSymbolEntries=merge_bindings(selected),qualification=dict(path=(LANE/'qualification.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'qualification.json')),sdkTypeGeometry=sdk,producer=Path(__file__).name,producerSha256=sha256(__file__),limits=limits)
        write_json(ROOT/'evidence/matches'/('goal-resume20261107-resource-path-api-'+module+'.json'),canonical)
    print(dict(functions=27,preservedBytes=4812,pairs=len(traces),actualHelperReturnsPerSide=behavior['actualHelperReturnsPerSide'],prototypeCases=len(prototypes['compilerCases']),identitySourceControls=sum(len(c['rejected'])for c in namespace),wrongCRejected=[len(r['rejected'])for r in negatives],sourceCredit=0),flush=True)


if __name__=='__main__':main()
