import copy
import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
from goal_resume_resource_path_views import SOURCE,LANE,WORK
from goal_resume_resource_path_contracts import recipes,recipe,view,replay_builds,build,identity,negative_source,linker
from goal_resume_resource_path_behavior import fixtures,run,qualify,HELPERS,module_image
from goal_resume_resource_path_compile import geometry


def prototype_controls():
    ref=recipe(0x0202a8e0);folder=WORK/'prototype-controls';folder.mkdir(parents=True,exist_ok=True)
    header=(SOURCE/'resource_path_api.h').read_text()
    positive='typedef unsigned int (*SizeAPI)(const void *);\ntypedef unsigned int (*LoadAPI)(const void *,unsigned int);\nSizeAPI size_definition=native_main_0202a8e0,size_import=native_fn_0202a8e0;\nLoadAPI load_definition=native_main_0203cc3c,load_import=native_fn_0203cc3c;\nunsigned int probe(const char *,unsigned int);\nunsigned int probe(const char *path,unsigned int heap){return native_fn_0202a8e0(path)+native_fn_0203cc3c(path,heap);}\n'
    cases=[('canonical-positive',positive,True),('size-word-argument','extern unsigned int native_fn_0202a8e0(unsigned int);\n',False),('size-void-prototype','extern unsigned int native_fn_0202a8e0(void);\n',False),('load-word-path','extern unsigned int native_fn_0203cc3c(unsigned int,unsigned int);\n',False),('load-signed-heap','extern unsigned int native_fn_0203cc3c(const void*,int);\n',False),('load-pointer-return','extern void *native_fn_0203cc3c(const void*,unsigned int);\n',False),('missing-size-path','unsigned int probe(void){return native_fn_0202a8e0();}\n',False),('missing-load-heap','unsigned int probe(void){return native_fn_0203cc3c(0);}\n',False),('extra-size-argument','unsigned int probe(void){return native_fn_0202a8e0(0,0);}\n',False),('SDK-word-is-not-API-word','typedef unsigned long SDKWord;\nextern SDKWord native_fn_0202a8e0(const void*);\n',False)]
    results=[]
    for label,body,passed in cases:
        if not passed and 'unsigned int probe(void){'in body:body='unsigned int probe(void);\n'+body
        source=folder/(label+'.c');obj=folder/(label+'.o');source.write_text(header+body)
        process=subprocess.run([str(ROOT/ref['compilerPath']),*ref['compilerFlags'],'-requireprotos','-w','error','-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
        if(process.returncode==0)!=passed:raise ValueError(('Typed API compiler control differs',label,process.stdout,process.stderr))
        results.append(dict(name=label,expectedPass=passed,exitCode=process.returncode,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),stdout=process.stdout,stderr=process.stderr))
    aliases=[]
    for address in[0x0202a8e0,0x0203cc3c]:
        ref=recipe(address)
        for prefix in['func_','native_fn_','native_main_']:
            name=prefix+f'{address:08x}';binding=dict(program='',processor='arm9',module='main',address=hex(address),mode='arm',kind='function')
            if linker.verify_binding(name,binding)!=address:raise ValueError('Canonical source/report alias differs')
            aliases.append(dict(name=name,role='native-report-original-alias'if prefix=='func_'else'canonical-C-identifier',binding=binding))
    return dict(canonicalCIdentifiers=4,nativeOriginalReportAliases=2,aliases=aliases,compilerCases=results)


def identity_controls(rows):
    controls=[]
    for result in rows:
        row=result['view'];ref=recipe(int(row['address'],0));rejected=[]
        for key,value in [('program','child'),('processor','arm7'),('module','ov000'if row['module']=='main'else'main'),('mode','thumb'),('address',hex(int(row['address'],0)+4)),('bytes',row['bytes']-4),('targetSha256','0'*64),('name','native_main_00000000')]:
            wrong=dict(row,**{key:value})
            try:identity(wrong,ref)
            except ValueError:rejected.append(key)
            else:raise ValueError('Wrong namespace/alias/extent escaped frozen gate')
        wrong=dict(row,sourceSha256='0'*64)
        try:linker.validate(wrong,row['nativeSymbolEntries'],WORK/'rejected-source'/f'{int(row["address"],0):08x}')
        except ValueError as error:
            if 'source/immutable compiled object changed'not in str(error):raise
            rejected.append('changed-source-sha256')
        else:raise ValueError('Changed source escaped real native-link source guard')
        controls.append(dict(identity=result['identity'],rejected=rejected))
    return controls


def wrong_c(source_bodies):
    variants=[('wrong-size-status',0x0202a8e0,'native_data_020edec8 = 0;','native_data_020edec8 = 3;'),('wrong-load-selector',0x0203cc3c,'(u32)path, heap, 1','(u32)path, heap, 0'),('lost-incoming-path',0x02043018,'native_fn_0202a8e0((const void *)arg0)','native_fn_0202a8e0((const void *)0)')]
    results=[]
    for index,(label,address,before,after)in enumerate(variants):
        ref=recipe(address);folder=WORK/'wrong-C'/str(index);source=negative_source(view(ref),folder/'source',before,after);row,body=build(source,folder/'build',ref,True)
        mutated=dict(source_bodies);mutated[(ref['module'],address)]=body;rejected=[]
        for ordinal,fixture in enumerate(fixtures()):
            if fixture['address']!=address:continue
            result=run(fixture,mutated,ordinal)
            if result['modelFailures']:rejected.append(dict(ordinal=ordinal,failures=result['modelFailures']))
        if not rejected:raise ValueError('Compiled wrong C escaped independent API model')
        results.append(dict(name=label,source=row,rejected=rejected))
    return results


def main():
    if(LANE/'inputs.json').exists():
        for pin in read_json(LANE/'inputs.json')['files']:
            if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen API proof input changed',pin['path']))
    sdk=geometry(recipe(0x0202a8e0));results=replay_builds();bodies={(r['view']['module'],int(r['view']['address'],0)):(ROOT/r['view']['realLink']['lcf']).with_name('caller.bin').read_bytes()for r in results}
    traces=qualify(bodies);prototypes=prototype_controls();namespace=identity_controls(results);negatives=wrong_c(bodies)
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();trace=LANE/'traces.json.gz';trace.write_bytes(gzip.compress(raw,mtime=0))
    migration_rows=[r['view']for r in results]
    for row in migration_rows:row.update(sourceCredit=0,previousSourceCreditPreserved=True)
    native_helpers=[]
    for address,size in HELPERS.items():
        unused,image=module_image('main');body=image[address-0x02000000:address-0x02000000+size]
        native_helpers.append(dict(program='',processor='arm9',module='main',mode='arm',address=hex(address),bytes=size,sha256=hashlib.sha256(body).hexdigest(),helperSourceCredit=0))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm9',allPassed=True,matches=migration_rows,functions=27,bytes=4812,canonicalMatchedFunctions=27,canonicalMatchedBytes=4812,acceptedFunctionCountDelta=0,acceptedByteCreditDelta=0,sourceCredit=0,zeroCreditMigrationFunctions=27,originalClaimAccepted173Functions=23,originalClaimPrepared174Functions=4,allocatedComparisons=results,prototypeControls=prototypes,namespaceAndSourceControls=namespace,behavior=dict(pairs=len(traces),actualTopReturns=2*len(traces),actualHelperReturnsPerSide=sum(len(t['result']['actualHelperReturns'])for t in traces),originalAndFreshFullRegistersCPSRMemoryEqual=True,nativeHelpers=native_helpers,independentModels=['Unsigned file-length/status and real SDK record path','Heap/rounded allocation/signed alignment and read ownership','Incoming filename word/capacity and read-state flags','Original overlay two-bit palette route','Four-byte filename table entries and real free wrapper','Native1399-record44-byte stride and compact16-bit fields']),wrongC=negatives,generatedTrace=dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace),uncompressedSha256=hashlib.sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=['All27 previous sources and new views are independently freshly compiled against actual frozen original allocated/symbol/raw-relocation contracts and genuinely linked as complete native function spans.','The62 new native/source pairs exercise the typed providers and five reviewed caller boundaries; inherited closed behavior for other identical bodies is preserved, not replayed or generalized to whole scenes.','Real native FSInitFile/FSOpenFile/FSCloseFile and archive/free wrappers execute. Filesystem find/open-command, allocator/read backend and UI upload services remain bounded supplied interfaces.','SDK u32 remains unsigned long; the two canonical top API return/heap words are unsigned int. Existing public caller signatures and unrelated data/API views remain unchanged.','No whole-program ISO-C repair, whole-module integration, new source credit or prepared174 acceptance is asserted.'])
    write_json(LANE/'qualification.json',report)
    for module in['main','ov000','ov005','ov006']:
        selected=[r for r in migration_rows if r['module']==module];native_bindings={}
        for row in selected:
            for name,binding in row['nativeSymbolEntries'].items():
                if name in native_bindings and native_bindings[name]!=binding:raise ValueError('Canonical module contains conflicting qualified bindings')
                native_bindings[name]=binding
        unused,image=module_image(module)
        canonical=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm9',module=module,moduleSha256=hashlib.sha256(image).hexdigest(),allPassed=True,matches=selected,canonicalMatchedFunctions=len(selected),canonicalMatchedBytes=sum(r['bytes']for r in selected),acceptedFunctionCountDelta=0,acceptedByteCreditDelta=0,acceptedSourceCredit=0,nativeSymbolEntries=native_bindings,qualification=dict(path=(LANE/'qualification.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'qualification.json')),sdkTypeGeometry=sdk,producer=Path(__file__).name,producerSha256=sha256(__file__),limits=report['limits'])
        write_json(ROOT/'evidence/matches'/('goal-resume20261107-resource-path-api-'+module+'.json'),canonical)
    print(dict(functions=27,preservedBytes=4812,pairs=len(traces),actualHelperReturnsPerSide=report['behavior']['actualHelperReturnsPerSide'],prototypeCases=len(prototypes['compilerCases']),identitySourceControls=sum(len(c['rejected'])for c in namespace),wrongCRejected=[len(r['rejected'])for r in negatives],sourceCredit=0),flush=True)


if __name__=='__main__':main()
