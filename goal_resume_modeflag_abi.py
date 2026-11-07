import copy
import gzip
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import match_runtime as compiler
import link_runtime_unit as linker
sys.path.insert(0,str(ROOT/'public_tools'))
from public_tools.native_objects import object_contract
from goal_resume_source1_modeflag_abi_audit import machine_check
from wave20261106_game_main_arm_next_third_bindings import verify_original
from wave20261106_game_main_arm_next_third_models import fixtures,run

LANE=ROOT/'evidence/lanes/parallel-wave20261106/goal-resume-source-1-modeflag-abi'
SOURCE=ROOT/'src/runtime/goal_resume20261106/modeflag_abi'
WORK=ROOT/'work/goal-resume-20261106/modeflag-abi'
API=SOURCE/'modeflag_api.h'


def canonical(value):
    return json.loads(json.dumps(value))


def references():
    return read_json(LANE/'reference-contracts.json')['entries']


def recipe(address):
    return next(r for r in references()if int(r['address'],0)==address)


def dependencies(source):
    result={};pending=[Path(source).resolve()]
    while pending:
        current=pending.pop()
        for name in re.findall(r'^\s*#include\s+"([^"]+)"',current.read_text(),re.M):
            path=(current.parent/name).resolve()
            if not path.is_relative_to(ROOT):raise ValueError('Quoted include escaped the project')
            relative=path.relative_to(ROOT).as_posix()
            if relative not in result:
                result[relative]=sha256(path);pending.append(path)
    return [dict(path=p,sha256=h)for p,h in sorted(result.items())]


def compile_source(source,directory,reference):
    source=Path(source).resolve();directory=Path(directory).resolve()
    if not source.is_relative_to(ROOT/'src')and not source.is_relative_to(WORK):raise ValueError('Unadmitted compiler input root')
    if not directory.is_relative_to(WORK):raise ValueError('Compiler output escaped the disjoint work root')
    executable=ROOT/reference['compilerPath']
    if sha256(executable)!=reference['compilerSha256']:raise ValueError('Pinned compiler changed')
    saved=compiler.WORK,compiler.FLAGS
    try:
        compiler.WORK=directory;compiler.FLAGS=reference['compilerFlags'][:]
        rows,unused=compiler.compare(source,'main',reference['compilerFlags'][0][2:],reference['compilerFlags'][reference['compilerFlags'].index('-inline')+1],False,compiler=executable)
    finally:compiler.WORK,compiler.FLAGS=saved
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError(('Genuine source compile failed',rows))
    row=dict(rows[0],program='',sourceDependencies=dependencies(source))
    if row['compilerFlags']!=reference['compilerFlags']:raise ValueError('Exact compiler flags changed')
    return row


def verify_identity(row,reference):
    fields=lambda r:((r.get('program')or''),r['processor'],r['module'],r['mode'],int(r['address'],0),r['bytes'],r['targetSha256'])
    if fields(row)!=fields(reference):raise ValueError('Closed physical identity or complete native extent differs')


def compare_contract(row,reference):
    verify_identity(row,reference)
    actual=canonical(object_contract(ROOT/row['object']))
    raw=linker.relocation_rows(ROOT/row['object'],row['name'])
    if actual!=reference['allocatedContract']or raw!=reference['rawRelocations']:raise ValueError('Allocated section/symbol/raw relocation contract changed')
    if not row['exactAfterDeclaredRelocation']or row['compiledBytes']!=row['bytes']:raise ValueError('Complete original native match changed')
    return hashlib.sha256(json.dumps(actual,separators=(',',':')).encode()).hexdigest()


def build(source,directory,reference,negative=False):
    row=compile_source(source,directory/'compile',reference)
    verify_identity(row,reference)
    bindings=copy.deepcopy(reference['nativeSymbolEntries'])
    if int(row['address'],0)!=0x0206dc54 and int(row['address'],0)!=0x020721b4 and not negative:
        row['originalNamespaceWitnesses']=verify_original(row,bindings)
    try:proof=linker.validate(row,bindings,directory/'link')
    except ValueError as error:
        if not negative or not error.args or not isinstance(error.args[0],dict):raise
        proof=dict(exactCallerBytes=False,comparison=error.args[0])
    if negative and proof['exactCallerBytes']:raise ValueError('Wrong source unexpectedly matched the whole native span')
    if linker.relocation_rows(ROOT/row['object'],row['name'])!=linker.relocation_rows(directory/'link/caller.o',row['name']):raise ValueError('Actual linker split changed raw source relocations')
    row.update(realLink=proof,nativeSymbolEntries=bindings,sourceLanguage='C',ordinaryCBytes=0 if negative else row['bytes'],justifiedAssemblyBytes=0)
    return row,(directory/'link/caller.bin').read_bytes()


def materialize_negative(source,folder,text):
    folder.mkdir(parents=True,exist_ok=True)
    target=folder/source.name;target.write_text(text)
    for d in dependencies(source):
        original=ROOT/d['path']
        if original==API:destination=folder.parent/'modeflag_api.h'
        else:destination=folder/original.name
        destination.write_bytes(original.read_bytes())
    return target


def prototype_controls(reference):
    folder=WORK/'prototypes';folder.mkdir(parents=True,exist_ok=True)
    header=API.read_text()
    expected='extern unsigned int native_main_0206dc54(const void *);\nextern unsigned int native_fn_0206dc54(const void *);\n'
    if header!=expected:raise ValueError('Canonical aliases do not declare one identical function type')
    positives=[];negatives=[]
    variants=[('positive','typedef unsigned int (*ModeFlag)(const void *);\nModeFlag definition_pointer=native_main_0206dc54;\nModeFlag import_pointer=native_fn_0206dc54;\n',True),
        ('wrong-definition-prototype','extern unsigned int native_main_0206dc54(void);\n',False),
        ('wrong-import-prototype','extern unsigned int native_fn_0206dc54(void);\n',False),
        ('wrong-concrete-pointer','extern unsigned int native_fn_0206dc54(unsigned int *);\n',False),
        ('wrong-return','extern unsigned short native_fn_0206dc54(const void *);\n',False),
        ('missing-argument','unsigned int probe(void){return native_fn_0206dc54();}\n',False),
        ('extra-argument','unsigned int probe(void){return native_fn_0206dc54(0,0);}\n',False)]
    for label,body,positive in variants:
        source=folder/(label+'.c');source.write_text(header+body);obj=folder/(label+'.o')
        command=[str(ROOT/reference['compilerPath']),*reference['compilerFlags'],'-requireprotos','-w','error','-c',str(source),'-o',str(obj)]
        process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
        if (process.returncode==0)!=positive:raise ValueError(('Canonical prototype control differs',label,process.stdout,process.stderr))
        value=dict(name=label,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr)
        (positives if positive else negatives).append(value)
    return dict(canonicalFunctionType='unsigned int(const void*)',positive=positives,rejected=negatives,sourceCredit=0)


def identity_controls(row,reference):
    rejected=[]
    for key,value in [('program','child'),('processor','arm7'),('module','ov000'),('mode','thumb'),('address',hex(int(row['address'],0)+4)),('bytes',row['bytes']-4),('targetSha256','0'*64)]:
        bad=copy.deepcopy(row);bad[key]=value
        try:verify_identity(bad,reference)
        except ValueError:rejected.append(key)
        else:raise ValueError('Wrong namespace/extent escaped the immutable identity gate')
    bad=dict(row,sourceSha256='0'*64)
    try:linker.validate(bad,row['nativeSymbolEntries'],WORK/'rejected-source')
    except ValueError as error:
        if 'source/immutable compiled object changed'not in str(error):raise
        rejected.append('changed-source-sha256')
    else:raise ValueError('Changed source digest escaped genuine linker gate')
    return dict(address=row['address'],rejected=rejected)


def third_behavior(rows,bodies,image):
    traces=[];negatives=[]
    for row in rows:
        name=f"{int(row['address'],0):08x}"
        if name=='0206dc54':continue
        native=image[int(row['address'],0)-0x02000000:int(row['address'],0)-0x02000000+row['bytes']]
        for ordinal,fixture in enumerate(fixtures(name)):
            a=run(row,native,fixture,image,ordinal);b=run(row,bodies[name],fixture,image,ordinal)
            if a!=b or a['modelFailures']or not a['actualTopReturn']:raise ValueError(('Inherited independent model differs',name,ordinal))
            traces.append(dict(address=row['address'],fixture=fixture,result=a))
    variants=[('wrong-record-stride','0207211c','offset=index*12','offset=index*16',lambda f:f['index']in[1,2]),
        ('wrong-flag-position','0207211c','1U<<(index-3)','1U<<(index-2)',lambda f:3<=f['index']<=9 and f['flags']==255),
        ('stale-counter','02071b28','u32 amount=native_fn_02065d28(native_data_020daf42[i*2]);\n        result=native_data_021c50e8.counter-amount;','u32 cached=native_data_021c50e8.counter;\n        u32 amount=native_fn_02065d28(native_data_020daf42[i*2]);\n        result=cached-amount;',lambda f:f['mutate']),
        ('wrong-signed-id','02071b28','native_fn_02065d28(native_data_020daf42[i*2])','native_fn_02065d28((u8)native_data_020daf42[i*2])',lambda f:True),
        ('wrong-widget','02073090','native_fn_02049ad0(25)','native_fn_02049ad0(26)',lambda f:True),
        ('wrong-option','02073090','if(option!=0)','if(option==0)',lambda f:True),
        ('wrong-nibble','0207313c','native_data_021c5a24.flags.low','native_data_021c5a24.flags.high',lambda f:bool(f['flags']&15)!=bool(f['flags']>>4)),
        ('wrong-category','0207313c','status=15','status=14',lambda f:f['kind']==26 and f['flags']&15==0)]
    for label,name,before,after,select in variants:
        source=SOURCE/'third'/(name+'.c');text=source.read_text()
        if text.count(before)!=1:raise ValueError('Wrong C mutation is ambiguous')
        folder=WORK/'third-negative'/label
        bad=materialize_negative(source,folder,text.replace(before,after));wrong,body=build(bad,folder/'build',recipe(int(name,16)),True)
        rejected=[]
        for ordinal,f in enumerate([f for f in fixtures(name)if select(f)]):
            value=run(wrong,body,f,image,ordinal)
            if not value['modelFailures']or not value['actualTopReturn']:raise ValueError(('Actual wrong C escaped independent model',label))
            rejected.append(dict(fixture=f,failures=value['modelFailures']))
        if not rejected:raise ValueError('Wrong C control has no selected cases')
        negatives.append(dict(name=label,rejected=rejected,proof=wrong))
    return traces,negatives


def main():
    LANE.mkdir(parents=True,exist_ok=True)
    if (LANE/'inputs.json').exists():
        for pin in read_json(LANE/'inputs.json')['files']:
            if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen ABI migration input changed: '+pin['path'])
    claim=read_json(LANE/'claim.json')
    for pin in claim['sourceViews']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Authorized source view changed')
    accepted=[r for r in references()if int(r['address'],0)!=0x020721b4]
    rows=[];bodies={};contracts=[];controls=[]
    for ref in accepted:
        name=f"{int(ref['address'],0):08x}";directory=WORK/'positive'/name
        old=compile_source(ROOT/ref['source'],directory/'previous-source',ref)
        old_hash=compare_contract(old,ref)
        row,body=build(ROOT/ref['newSource'],directory/'new-source',ref)
        contract_hash=compare_contract(row,ref)
        if old_hash!=contract_hash:raise ValueError('Fresh old/new allocated contracts differ')
        contracts.append(dict(address=row['address'],previousSource=ref['source'],previousSourceSha256=ref['sourceSha256'],previousCanonicalObjectSha256=ref['objectSha256'],freshPrevious=old,allocatedContractSha256=contract_hash,allocatedContractEqual=True,rawRelocationsEqual=True,fullContainerEqual=old['objectSha256']==row['objectSha256']))
        rows.append(row);bodies[name]=body;controls.append(identity_controls(row,ref))
        print('proved ABI view',name,row['bytes'],flush=True)
    if len(rows)!=5 or sum(r['bytes']for r in rows)!=580:raise ValueError('Zero-credit migration scope differs')
    info,image,unused=linker.measured_module('main')
    helper_native=image[0x6dc54:0x6dc70]
    native_check=machine_check(helper_native);source_check=machine_check(bodies['0206dc54'])
    if native_check!=source_check:raise ValueError('Actual ignored-R0 original/source behavior differs')
    source_check=dict(source_check,originalOnly=False,compiledSourceExecuted=True)
    traces,negative=third_behavior(rows,bodies,image)
    helper=next(r for r in rows if int(r['address'],0)==0x0206dc54)
    source=ROOT/helper['source'];text=source.read_text()
    bad=materialize_negative(source,WORK/'helper-negative',text.replace('var_r0 = 1;','var_r0 = 2;'))
    wrong,body=build(bad,WORK/'helper-negative/build',recipe(0x0206dc54),True)
    changed=dict(helper,source=bad.relative_to(ROOT).as_posix())
    try:linker.validate(changed,helper['nativeSymbolEntries'],WORK/'rejected-changed-source')
    except ValueError as error:
        if 'source/immutable compiled object changed'not in str(error):raise
        changed_source=dict(rejected=True,actualChangedSource=changed['source'],expectedPreviousSha256=helper['sourceSha256'],actualSourceSha256=sha256(bad))
    else:raise ValueError('Actual changed source escaped its pinned source hash')
    try:machine_check(body)
    except AssertionError:helper_negative=dict(rejected=True,proof=wrong)
    else:raise ValueError('Wrong helper return escaped independent ignored-R0 model')
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();(LANE/'third-traces.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm9',module='main',moduleSha256=info['sha256'],allPassed=True,matches=rows,canonicalMatchedFunctions=5,canonicalMatchedBytes=580,acceptedSourceCredit=0,acceptedFunctionCountDelta=0,acceptedByteCreditDelta=0,allocatedComparisons=contracts,identityControls=controls,prototypeControls=prototype_controls(recipe(0x0206dc54)),helperBehavior=dict(native=native_check,freshLinkedSource=source_check,pairedCases=1536,actualReturns=3072),helperWrongC=helper_negative,thirdCases=len(traces),thirdActualCallerReturns=2*len(traces),thirdNegativeEvidence=negative,generatedTrace=dict(path=(LANE/'third-traces.json.gz').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'third-traces.json.gz'),uncompressedSha256=hashlib.sha256(raw).hexdigest()),sourceCreditPendingSharedAcceptance=True,producer=Path(__file__).name,producerSha256=sha256(__file__),limits=['Five existing complete functions/580 initialized bytes are source-view migrations with zero new credit; original sources and reports remain unchanged.','Each fresh object retains all allocated sections, defined/referenced symbols and raw relocations, and genuine MW unit linking reproduces every original native byte. Whole-module integration remains coordinator-owned.','Four inherited independent caller models retain scripted provider boundaries and give no provider/data/BSS/storage credit.','Generic const void* closes this qualified function API only; inherited global data views and computed indirect call targets are not generalized.'])
    report['changedActualSourceControl']=changed_source
    write_json(LANE/'match.json',report)
    print(dict(migratedFunctions=5,preservedBytes=580,sourceCredit=0,thirdPairs=len(traces),helperPairs=1536),flush=True)


if __name__=='__main__':main()
