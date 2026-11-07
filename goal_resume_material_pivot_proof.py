import copy
import gzip
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
from goal_resume_material_pivot import SOURCE,LANE,WORK,common,guarded_render,qualify_consumers
from goal_resume_material_pivot_data import build,COMPILER,FLAGS
from goal_resume_material_pivot_behavior import fixtures,run,validate
from goal_resume_resource_path_contracts import dependencies


def type_controls():
    cases=[('positive',common()+'extern const NativeMaterialPivot native_data_main_020d9068;\n',True),('wrong-word-width',common().replace('unsigned long masks[8]','unsigned long long masks[8]'),False),('wrong-pivot-count',common().replace('pivots[9][4]','pivots[8][4]'),False),('wrong-overall-const',common()+'extern NativeMaterialPivot native_data_main_020d9068;\n',False)]
    results=[]
    for index,(name,text,expected)in enumerate(cases):
        folder=WORK/'types'/str(index);folder.mkdir(parents=True,exist_ok=True);source=folder/'type.c';obj=folder/'type.o';source.write_text(text)
        process=subprocess.run([str(COMPILER),*FLAGS,'-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
        if(process.returncode==0)!=expected:raise ValueError(('Actual canonical data type control differs',name,process.stdout,process.stderr))
        results.append(dict(name=name,expectedPass=expected,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    return results


def wrong_data(image):
    text=(SOURCE/'data.c').read_text();variants=[('wrong-mask-flag-bit','0x8000UL','0x4000UL','material'),('wrong-pivot-exclusion','#define REMAIN_SECOND(i) ((i)==2?1:2)','#define REMAIN_SECOND(i) ((i)==2?0:2)','pivot')];results=[]
    for index,(name,before,after,kind)in enumerate(variants):
        if text.count(before)!=1:raise ValueError('Wrong mathematical data predicate is ambiguous')
        folder=WORK/'wrong-data'/str(index);folder.mkdir(parents=True,exist_ok=True);source=folder/'data.c';source.write_text(text.replace(before,after));payload,row=build(source,folder/'build');mutated=bytearray(image);mutated[0xd9068:0xd90ac]=payload
        if payload==image[0xd9068:0xd90ac]or any(value>=9 for value in payload[32:]):raise ValueError('Wrong-data control is unchanged or would leave the valid matrix-index domain')
        rejected=[];unaffected=0
        for ordinal,fixture in enumerate(fixtures()):
            if fixture['kind']!=kind:continue
            result=run(bytes(mutated),fixture,ordinal)
            if result['modelFailures']:rejected.append(dict(ordinal=ordinal,failures=result['modelFailures']))
            else:unaffected+=1
        if not rejected or not unaffected:raise ValueError('Wrong data does not distinguish affected and unaffected model cases')
        results.append(dict(name=name,compiledData=row,rejected=rejected,unaffectedCases=unaffected,allPivotIndicesRemainIn0To8=True))
    return results


def main():
    if sha256(LANE/'claim.json')!='9640e9e4e00b52fe8c8b8afc7e2fc55ac8df4cd19f8fd6cc455a852093de1ad2':raise ValueError('Frozen bounded material/pivot claim changed')
    if(LANE/'inputs.json').exists():
        for pin in read_json(LANE/'inputs.json')['files']:
            if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen material proof input changed',pin['path']))
    code,expected,blocked=guarded_render()
    if(SOURCE/'data.c').read_text()!=code or(SOURCE/'material_pivot.h').read_text()!=common():raise ValueError('Independent semantic C/common declaration changed')
    refs=read_json(LANE/'reference-contracts.json')['entries']
    header_closure=[]
    for ref in refs:
        if sha256(ROOT/ref['source'])!=ref['sourceSha256']:raise ValueError('Accepted original source changed')
        for dependency in ref['sourceDependencies']:
            if sha256(ROOT/dependency['path'])!=dependency['sha256']:raise ValueError('Accepted original header/input changed')
        original=ROOT/ref['source'];view=SOURCE/'consumers'/f"{int(ref['address'],0):08x}"/original.name;expected_source=original.read_text().replace('.field_0000[','.masks[').replace('.field_0020[','.pivots[')
        if view.read_text()!=expected_source:raise ValueError('Consumer changed beyond necessary canonical typed field access')
        old_header=original.with_name('context_00.h');new_header=view.with_name('context_00.h');pattern=r'typedef struct \{\n[^{}]*\} NativeStorage_020d9068;\nextern[^;]*native_data_main_020d9068;\n';old_body=old_header.read_text();found=list(re.finditer(pattern,old_body))
        if len(found)!=1:raise ValueError('Previous typed storage declaration is ambiguous')
        include='#include "'+os.path.relpath(SOURCE/'material_pivot.h',new_header.parent).replace('\\','/')+'"\n';expected_header=old_body[:found[0].start()]+include+old_body[found[0].end():]
        if new_header.read_text()!=expected_header:raise ValueError('Mirrored consumer header changes beyond the canonical aggregate declaration')
        header_closure.append(dict(previousSource=ref['source'],previousSourceSha256=sha256(original),previousHeader=old_header.relative_to(ROOT).as_posix(),previousHeaderSha256=sha256(old_header),view=view.relative_to(ROOT).as_posix(),viewSha256=sha256(view),viewHeader=new_header.relative_to(ROOT).as_posix(),viewHeaderSha256=sha256(new_header),statementControlFlowExactlyPreservedExceptTypedFields=True,allOtherHeaderDeclarationsUnchanged=True))
    write_json(LANE/'common-header-closure.json',dict(commonHeader=dict(path=(SOURCE/'material_pivot.h').relative_to(ROOT).as_posix(),sha256=sha256(SOURCE/'material_pivot.h')),consumers=header_closure,dataContainsIdenticalDeclaration=True,dataIncludesHeaderAtCompileTime=False,SDKU32='unsigned long, actual target width4',constAggregate='const unsigned long masks[8]; const unsigned char pivots[9][4]',originalEnclosingObjectAndAlignmentClaimed=False))
    qualify_consumers();consumer_proof=read_json(LANE/'consumers-qualified.json');payload,data=build(SOURCE/'data.c',WORK/'data-positive',expected);image=(ROOT/'extract/arm9/arm9.bin').read_bytes()
    if hashlib.sha256(image).hexdigest()!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'or payload!=image[0xd9068:0xd90ac]:raise ValueError('Fresh mathematical data differs from pinned original storage')
    replaced=bytearray(image);replaced[0xd9068:0xd90ac]=payload;migrations=[]
    for entry in consumer_proof['results']:
        row=entry['view']['row'];real=entry['view']['realLink'];body=(ROOT/real['lcf']).with_name('caller.bin').read_bytes();address=int(row['address'],0);replaced[address-0x02000000:address-0x02000000+row['bytes']]=body;row.update(realLink=real,sourceDependencies=dependencies(ROOT/row['source']),nativeSymbolEntries=next(r['nativeSymbolEntries']for r in refs if r['address']==row['address']),sourceLanguage='C',ordinaryCBytes=row['bytes'],justifiedAssemblyBytes=0,sourceCredit=0,previousSource=next(r['source']for r in refs if r['address']==row['address']));migrations.append(row)
    if bytes(replaced)!=image:raise ValueError('Qualified data/consumer replacements change a native initialized byte')
    traces=[]
    for ordinal,fixture in enumerate(fixtures()):
        a=run(image,fixture,ordinal);b=run(bytes(replaced),fixture,ordinal)
        if a!=b or a['modelFailures']:raise ValueError(('Original/fresh reader, real helper or independent model differs',ordinal,fixture,a['modelFailures'],b['modelFailures']))
        traces.append(dict(fixture=fixture,result=a))
    negatives=wrong_data(image);types=type_controls();unsupported=[]
    for pivot in range(9,16):
        try:validate(dict(kind='pivot',pivot=pivot))
        except ValueError:unsupported.append(pivot)
        else:raise ValueError('Unsupported pivot would reach native/C execution')
    namespace=[]
    for key,value in [('program','child'),('processor','arm7'),('module','ov000'),('kind','function'),('mode','arm'),('address','0x020d906c'),('bytes',64)]:
        bad=dict(data,**{key:value});fields=lambda r:((r.get('program')or''),r['processor'],r['module'],r['kind'],r['mode'],r['address'],r['bytes'])
        if fields(bad)==fields(data):raise ValueError('Wrong bounded data identity escaped comparison')
        namespace.append(key)
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();trace=LANE/'traces.json.gz';trace.write_bytes(gzip.compress(raw,mtime=0));data.update(inputModuleSha256=hashlib.sha256(image).hexdigest(),targetSha256=hashlib.sha256(payload).hexdigest(),outputSha256=hashlib.sha256(payload).hexdigest(),exactBytes=True,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,sourceCredit=0,boundedOriginalStorageView=True,originalDeclarationAlignmentClaimed=False)
    limits=['Only the bounded68B aggregate and two additive zero-credit2280B source views are proposed. Original source/header/object/producers remain unchanged.','SDK u32 remains unsigned long4. Both consumer views use the same const aggregate declaration and preserve every original statement/control-flow structure except necessary typed field names.','All416 native/source pairs cover material selectors0..7 and valid pivot0..8/signs/signed16 coefficient boundaries. Invalid compressed-node pivots9..15 are rejected by fixture admission without native/C execution; no runtime C guard is added.','The actual original14B Thumb zero-matrix helper executes288 times per side. Scale-one callback is a supplied interface; no GPU/hardware/whole-scene behavior or provider source credit is claimed.','Generic matcher1119/1120 diagnostic is retained; unchanged allocated/raw contracts and pinned genuine MW output establish complete1120B native equality, including ARM/Thumb interworking.','Data adds zero functions, executable/BSS/encoded/padding bytes. Shared data-aware admission, full20-module/container checks and committed closure remain coordinator-owned.']
    report=dict(schemaVersion=1,status='material-pivot-data-and-zero-credit-migrations-qualified',romSha256=configuration()['romSha256'],sourceCredit=0,data=data,migrations=migrations,consumerContracts=consumer_proof,readerPairs=len(traces),actualReaderReturns=2*len(traces),actualThumbHelperReturnsPerSide=sum(len(t['result']['actualHelperReturns'])for t in traces),independentModels=['Two material color bitfield blends for all64 selector pairs and two bit patterns','Row/column pivot exclusion and signed coefficient/sign flags with actual Thumb matrix zeroing','Complete command advance/result pointers/const table access widths/scale-one callback arguments'],generationGuard=dict(blockedOriginalReads=blocked),negativeData=negatives,typeControls=types,unsupportedPivotAdmissionControls=dict(values=unsupported,executed=False,runtimeGuardAdded=False),namespaceControls=namespace,generatedTrace=dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace),uncompressedSha256=hashlib.sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=limits)
    write_json(LANE/'qualification.json',report);shared=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm9',module='main',moduleSha256=hashlib.sha256(image).hexdigest(),allPassed=True,qualification=dict(path=(LANE/'qualification.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'qualification.json')),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=limits)
    write_json(ROOT/'evidence/matches/goal-resume20261107-material-pivot-data68.json',dict(shared,functionMatched=0,functionMatches=[],dataMatches=[data],ordinaryFunctionCredit=0,executableSectionBytes=0,allocatedZeroFillBytes=0,initializedDataObjects=1,initializedDataBytes=68,encodedAssetBytes=0,measuredZeroAlignmentBytes=0,sourceCredit=0))
    native_bindings={name:value for row in migrations for name,value in row['nativeSymbolEntries'].items()};write_json(ROOT/'evidence/matches/goal-resume20261107-material-pivot-migrations2280.json',dict(shared,matches=migrations,nativeSymbolEntries=native_bindings,zeroCreditMigrationFunctions=2,preservedMigrationBytes=2280,acceptedFunctionCountDelta=0,acceptedByteCreditDelta=0,sourceCredit=0))
    print(dict(dataBytes=68,migrations=2,migrationBytes=2280,pairs=len(traces),actualThumbReturnsPerSide=report['actualThumbHelperReturnsPerSide'],wrongDataRejected=[len(n['rejected'])for n in negatives],unsupportedPivotsNotExecuted=unsupported,sourceCredit=0),flush=True)


if __name__=='__main__':main()
