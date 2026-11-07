import copy
import gzip
import hashlib
import json
import match_runtime as compiler
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
from goal_resume_resource_path_future import FUTURE_SOURCE,FUTURE_LANE,FUTURE_WORK,OLD_LANE,LANE
from goal_resume_resource_path_compile import compile_source,normalized,object_contract,linker
from goal_resume_resource_path_contracts import dependencies,negative_source
from goal_resume_resource_selection_oracle import fixtures,run
from goal_resume_resource_selection_proof import original,helper_contracts


def records():return read_json(FUTURE_LANE/'reference-contracts.json')['entries']


def snapshot():
    destination=FUTURE_LANE/'reference-contracts.json'
    if destination.exists():raise ValueError('Frozen typed future source contracts exist')
    entries=[]
    for row in read_json(FUTURE_LANE/'first-compile.json')['functions']:
        entry=dict(row,compilerPath='tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe',allocatedContract=normalized(object_contract(ROOT/row['object'])),rawRelocations=linker.relocation_rows(ROOT/row['object'],row['name']),expectedWholeNativeMatch=int(row['address'],0)==0x02061470)
        entries.append(entry)
    write_json(destination,dict(status='frozen-single-typed-compile-contracts',sourceCredit=0,entries=entries,rule='The268B view is a complete native-match candidate;432B remains a measured nonmatching typed-source residual. Contracts freeze the one approved source/profile attempt, not an accepted baseline.'))


def build(source,folder,ref,negative=False):
    row=compile_source(source,folder/'c',ref);row.update(sourceDependencies=dependencies(source),sourceLanguage='C',sourceCredit=0)
    if not negative:
        if normalized(object_contract(ROOT/row['object']))!=ref['allocatedContract']or linker.relocation_rows(ROOT/row['object'],row['name'])!=ref['rawRelocations']:raise ValueError('The single typed-source allocated/raw contract changed')
        if row['sourceSha256']!=ref['sourceSha256']:raise ValueError('Frozen typed source changed')
    try:real=linker.validate(row,ref['nativeSymbolEntries'],folder/'l')
    except ValueError as error:
        if not error.args or not isinstance(error.args[0],dict):raise
        real=dict(exactCallerBytes=False,comparison=error.args[0])
    if not negative and real['exactCallerBytes']!=ref['expectedWholeNativeMatch']:raise ValueError('Native match status changed from the single approved attempt')
    if linker.relocation_rows(ROOT/row['object'],row['name'])!=linker.relocation_rows(folder/'l/caller.o',row['name']):raise ValueError('Genuine future linker split changed raw relocations')
    row.update(realLink=real,nativeSymbolEntries=ref['nativeSymbolEntries'],ordinaryCBytes=268 if real['exactCallerBytes']and not negative else 0,justifiedAssemblyBytes=0)
    return row,(folder/'l/caller.bin').read_bytes()


def main():
    for pin in read_json(FUTURE_LANE/'inputs.json')['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen typed-future proof input changed')
    info,image,symbols=linker.measured_module('main');rows=[];traces=[];differences=[]
    for ref in records():
        address=int(ref['address'],0);row,body=build(ROOT/ref['source'],ROOT/'work/p-api700'/f'{address:08x}',ref);native=original(ref,image,symbols)
        for ordinal,fixture in enumerate(fixtures()):
            if fixture['address']!=address:continue
            span=max(len(native),len(body));a=run(native,fixture,image,ordinal,span);b=run(body,fixture,image,ordinal,span)
            if a['modelFailures']or b['modelFailures']or a['observation']!=b['observation']:raise ValueError(('Typed future C ABI behavior/model differs',hex(address),ordinal,a['modelFailures'],b['modelFailures']))
            delta=[i for i,(x,y)in enumerate(zip(a['rawRegisters'],b['rawRegisters']))if x!=y]
            if delta or a['cpsr']!=b['cpsr']:differences.append(dict(address=row['address'],ordinal=ordinal,registers=delta,nativeCpsr=a['cpsr'],sourceCpsr=b['cpsr']))
            if ref['expectedWholeNativeMatch']and(delta or a['cpsr']!=b['cpsr']):raise ValueError('Matched268B caller changed full machine observations')
            traces.append(dict(fixture=fixture,observation=a['observation'],nativeRegisters=a['rawRegisters'],sourceRegisters=b['rawRegisters'],nativeCpsr=a['cpsr'],sourceCpsr=b['cpsr']))
        rows.append(row)
    variants=[('wrong-sentinel',0x02061088,'code==-1','code==-2'),('unsigned-format-code',0x02061088,'(s32)code','(s32)(u8)code'),('wrong-free-heap',0x02061088,'native_fn_0202a498(2,resource)','native_fn_0202a498(3,resource)'),('wrong-palette-zero',0x02061470,'u16 zero=0','u16 zero=1'),('wrong-signed-flag-gate',0x02061470,'[0x273]!=0','[0x273]==1'),('wrong-bitmap-length',0x02061470,'0,0x900','0,0x800'),('wrong-final-flag',0x02061470,'[1]=1','[1]=0')]
    negatives=[]
    for index,(label,address,before,after)in enumerate(variants):
        ref=next(r for r in records()if int(r['address'],0)==address);folder=ROOT/'work/p-api700-neg'/str(index);source=negative_source(ROOT/ref['source'],folder/'s',before,after);wrong,body=build(source,folder/'b',ref,True);rejected=[]
        for ordinal,fixture in enumerate(fixtures()):
            if fixture['address']!=address:continue
            try:outcome=run(body,fixture,image,ordinal)
            except(ValueError,AssertionError)as error:rejected.append(dict(ordinal=ordinal,reason=type(error).__name__));continue
            if outcome['modelFailures']:rejected.append(dict(ordinal=ordinal,failures=outcome['modelFailures']))
        if not rejected:raise ValueError('Compiled typed-future wrong C escaped independent model')
        negatives.append(dict(name=label,proof=wrong,rejected=rejected))
    controls=[]
    for ref in records():
        rejected=[]
        for key,value in [('program','child'),('processor','arm7'),('module','ov000'),('mode','thumb'),('address',hex(int(ref['address'],0)+4)),('bytes',ref['bytes']-4),('targetSha256','0'*64)]:
            wrong=copy.deepcopy(ref);wrong[key]=value
            try:original(wrong,image,symbols)
            except ValueError:rejected.append(key)
            else:raise ValueError('Wrong complete future native namespace escaped gate')
        folder=ROOT/'work/p-api700-types'/f'{int(ref["address"],0):08x}';folder.mkdir(parents=True,exist_ok=True)
        header=(FUTURE_SOURCE/'resource_selection.h').read_text();address=int(ref['address'],0)
        before='native_main_02061088(u32,u32,u32)'if address==0x02061088 else'native_main_02061470(void)';after='native_main_02061088(u32,u32,u16)'if address==0x02061088 else'native_main_02061470(u32)'
        if header.count(before)!=1:raise ValueError('Wrong public prototype mutation is ambiguous')
        header=header.replace(before,after).replace('#include "../resource_path_api.h"','#include "'+(FUTURE_SOURCE.parent/'resource_path_api.h').as_posix()+'"')
        bad_header=folder/'resource_selection.h';bad_header.write_text(header);source=folder/f'{address:08x}.c';source.write_text((ROOT/ref['source']).read_text().replace('#include "resource_selection.h"','#include "'+bad_header.as_posix()+'"'))
        saved=compiler.WORK,compiler.FLAGS
        try:
            compiler.WORK=folder/'c';compiler.FLAGS=ref['compilerFlags'][:];failed,unused=compiler.compare(source,'main',ref['compilerFlags'][0][2:],ref['compilerFlags'][ref['compilerFlags'].index('-inline')+1],False,compiler=ROOT/ref['compilerPath'])
        finally:compiler.WORK,compiler.FLAGS=saved
        if len(failed)!=1 or not failed[0].get('compileFailed'):raise ValueError('Contradictory actual future public prototype escaped compiler')
        controls.append(dict(address=ref['address'],namespaceRejected=rejected,actualCompilerPrototypeRejected=True,diagnostic=failed[0]))
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();trace=FUTURE_LANE/'traces.json.gz';trace.write_bytes(gzip.compress(raw,mtime=0));helpers=helper_contracts(image)
    limits=['The268B02061470 is a complete genuine native-match candidate;432B02061088 remains nonmatching at345/432 bytes and receives zero proposed acceptance credit.','Both use the one unchanged approved sp1p5 recipe and differ from preserved old source only by the canonical typed API and obsolete path integer-cast removal. No source/profile search is performed.','All85 pairs satisfy independent bounded C ABI observations and models; the268B candidate also preserves full raw GPR/CPSR. Raw caller-clobbered register differences for432B are explicitly retained.','Ten real original helper bodies execute, with formatter/filesystem/archive/video leaves supplied as declared bounded interfaces. The separate27-row migration proof qualifies the real SDK/archive API closure; no scene/filesystem/hardware or helper/data source credit is added.','The268B candidate depends on coordinator adoption of the27-row/4812B zero-credit canonical API migration and all shared gates; neither source is automatically accepted.']
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],status='typed-future-qualified-split-match-and-residual',sourceCredit=0,functions=rows,originalFunctions=2,originalBytes=700,compiledBytes=sum(r['compiledBytes']for r in rows),pairs=len(traces),actualTopReturns=2*len(traces),actualHelperReturnsPerSide=sum(len(t['observation']['actualHelperReturns'])for t in traces),realHelpers=helpers,rawRegisterDifferences=differences,negativeEvidence=negatives,namespaceControls=controls,canonicalApiDependency=dict(path=(LANE/'ready.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'ready.json')),generatedTrace=dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace),uncompressedSha256=hashlib.sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=limits)
    write_json(FUTURE_LANE/'qualification.json',report)
    matched=[r for r in rows if r['realLink']['exactCallerBytes']]
    canonical=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm9',module='main',moduleSha256=info['sha256'],allPassed=True,matches=matched,canonicalMatchedFunctions=1,canonicalMatchedBytes=268,acceptedSourceCredit=0,nativeSymbolEntries=matched[0]['nativeSymbolEntries'],qualification=dict(path=(FUTURE_LANE/'qualification.json').relative_to(ROOT).as_posix(),sha256=sha256(FUTURE_LANE/'qualification.json')),canonicalApiDependency=report['canonicalApiDependency'],producer=Path(__file__).name,producerSha256=sha256(__file__),limits=limits)
    write_json(ROOT/'evidence/matches/goal-resume20261107-resource-path-display268.json',canonical)
    print(dict(functions=2,matchedCandidateBytes=268,residualBytes=432,pairs=len(traces),actualHelperReturnsPerSide=report['actualHelperReturnsPerSide'],wrongCRejected=[len(n['rejected'])for n in negatives],rawRegisterDifferenceVectors=len(differences),sourceCredit=0),flush=True)


if __name__=='__main__':main()
