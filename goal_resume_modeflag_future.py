import copy
import gzip
import hashlib
import json
from pathlib import Path
from project import ROOT,read_json,write_json,configuration,sha256
import goal_resume_source1_detail_display_proof as original
from goal_resume_modeflag_abi import LANE,SOURCE,WORK,recipe,compile_source,compare_contract,build,materialize_negative,API
import link_runtime_unit as linker

FUTURE_LANE=LANE/'future-detail'
FUTURE_SOURCE=SOURCE/'detail_display'
FUTURE_WORK=WORK/'future-detail'


def compare(source,directory):
    return [compile_source(source,directory,recipe(0x020721b4))],{}


def compiled(source,directory,negative=False):
    original.compare=compare
    row,body,image=original.build(source,directory,negative)
    row['sourceDependencies']=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in [source.with_name('detail_display.h'),API]]
    return row,body,image


def main():
    FUTURE_LANE.mkdir(parents=True,exist_ok=True)
    if (LANE/'inputs.json').exists():
        for pin in read_json(LANE/'inputs.json')['files']:
            if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen future API input changed')
    row,body,image=compiled(FUTURE_SOURCE/'020721b4.c',FUTURE_WORK/'positive')
    digest=compare_contract(row,recipe(0x020721b4))
    provider,provider_body=build(SOURCE/'runtime07/native_main_0206dc54.c',FUTURE_WORK/'fresh-mode-provider',recipe(0x0206dc54))
    compare_contract(provider,recipe(0x0206dc54))
    source_image=bytearray(image);source_image[0x6dc54:0x6dc70]=provider_body;source_image=bytes(source_image)
    symbols=(ROOT/'config/arm9/symbols.txt').read_text();records=(ROOT/'config/arm9/relocs.txt').read_text()
    native=original.original(row,image,symbols,records)
    traces=[]
    for ordinal,fixture in enumerate(original.fixtures()):
        a=original.run(native,fixture,image,ordinal);b=original.run(body,fixture,source_image,ordinal)
        if a!=b or a['modelFailures']:raise ValueError(('Canonical-API future caller/source behavior differs',ordinal))
        traces.append(dict(fixture=fixture,result=a))
    variants=[('wrong-selector','index==7?13:14','index==7?12:14'),
        ('wrong-mode-gate','available!=0 &&','available==0 &&'),
        ('stale-vs-live-detail','native_fn_02049ffc(renderer);','native_fn_02049ffc(renderer); detail=native_data_021c4f60.detail;')]
    negatives=[]
    text=(FUTURE_SOURCE/'020721b4.c').read_text()
    for i,(label,before,after)in enumerate(variants):
        if text.count(before)!=(2 if label=='wrong-mode-gate'else 1):raise ValueError('Future wrong C is ambiguous')
        folder=FUTURE_WORK/'negative'/str(i)
        bad=materialize_negative(FUTURE_SOURCE/'020721b4.c',folder,text.replace(before,after))
        wrong,code,unused=compiled(bad,folder/'build',True)
        rejected=[]
        for ordinal,f in enumerate(original.fixtures()):
            result=original.run(code,f,source_image,ordinal)
            if result['modelFailures']:rejected.append(ordinal)
        if not rejected:raise ValueError('Wrong future C escaped independent models')
        negatives.append(dict(name=label,rejectedVectors=rejected,proof=wrong))
    rejected=[]
    for key,value in [('program','child'),('processor','arm7'),('module','ov000'),('mode','thumb'),('address','0x20721b8'),('bytes',444),('targetSha256','0'*64)]:
        wrong=copy.deepcopy(row);wrong[key]=value
        try:original.original(wrong,image,symbols,records)
        except ValueError:rejected.append(key)
        else:raise ValueError('Wrong future physical namespace escaped')
    for key,value in [('offset',440),('addend',4),('target','0x21c4f64')]:
        wrong=copy.deepcopy(row);wrong['relocations'][-3][key]=value
        try:original.original(wrong,image,symbols,records)
        except ValueError:rejected.append('menu-'+key)
        else:raise ValueError('Wrong future data origin escaped')
    alias_controls=[]
    for key,value in [('program','child'),('processor','arm7'),('module','ov000'),('mode','thumb'),('address','0x206dc58'),('kind','data')]:
        binding=dict(row['nativeSymbolEntries']['native_fn_0206dc54']);binding[key]=value
        try:linker.verify_binding('native_fn_0206dc54',binding)
        except ValueError:alias_controls.append(key)
        else:raise ValueError('Wrong qualified canonical helper alias escaped actual binding gate')
    folder=FUTURE_WORK/'prototype'
    bad=materialize_negative(FUTURE_SOURCE/'020721b4.c',folder,text)
    header=bad.with_name('detail_display.h')
    header.write_text(header.read_text().replace('native_main_020721b4(s32)','native_main_020721b4(unsigned short)'))
    try:compile_source(bad,folder/'compile',recipe(0x020721b4))
    except ValueError as error:
        if not error.args or not isinstance(error.args[0],tuple)or error.args[0][0]!='Genuine source compile failed':raise
        compiler_failure=error.args[0][1]
    else:raise ValueError('Conflicting future caller prototype escaped compiler')
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
    expected=read_json(ROOT/'evidence/matches/goal-resume20261106-source1-detail-display.json')['generatedTrace']['uncompressedSha256']
    if hashlib.sha256(raw).hexdigest()!=expected:raise ValueError('Canonical API changed frozen complete future behavior trace')
    (FUTURE_LANE/'traces.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    info,unused,unused=linker.measured_module('main')
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm9',module='main',moduleSha256=info['sha256'],allPassed=True,matches=[dict(row,behaviorQualified=True)],canonicalMatchedFunctions=1,canonicalMatchedBytes=456,acceptedSourceCredit=0,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=5,actualNativeHelperReturnsPerSide=sum(len(t['result']['actualHelperReturns'])for t in traces),freshSourceModeProvider=provider,allocatedContractEqual=True,allocatedContractSha256=digest,rawRelocationsEqual=True,negativeEvidence=negatives,bindingLayoutControls=dict(rejected=rejected),prototypeControl=dict(actualCompilerRejected=True,diagnostic=compiler_failure),generatedTrace=dict(path=(FUTURE_LANE/'traces.json.gz').relative_to(ROOT).as_posix(),sha256=sha256(FUTURE_LANE/'traces.json.gz'),uncompressedSha256=hashlib.sha256(raw).hexdigest(),frozenOriginalTraceEqual=True),nativeSymbols={n:b['address']for n,b in row['nativeSymbolEntries'].items()},nativeSymbolBindings=row['nativeSymbolEntries'],acceptanceDependencies=[dict(owner='coordinator',status='qualified-source-view-candidates-pending-adoption',sourceCredit=0,migrationClaim=(LANE/'claim.json').relative_to(ROOT).as_posix(),migrationClaimSha256=sha256(LANE/'claim.json'),requirement='Adopt all five reviewed zero-credit canonical API source views atomically with this future view in a later cohort; frozen174 is excluded.')],producer=Path(__file__).name,producerSha256=sha256(__file__),limits=['Complete456B ordinary C object and genuine MW unit link preserve original bytes, symbols and raw relocations with the declaration-only canonical constvoid* API.','72 fixture pairs preserve the frozen original complete trace. Source-side mode provider is freshly compiled/MW-linked; five actual provider bodies return360 times per side.','Three compiled wrong-C controls reject selector/mode/freshness models. Ten namespace/data-origin controls and actual contradictory caller prototype reject.','Four renderer/handle interfaces remain bounded supplied services; no complete UI/hardware, data/BSS storage or additional provider credit.','456 bytes remain pending coordinator adoption and shared gates; old source/header/typed proposal/READY remain unchanged.'])
    report['canonicalAliasNamespaceControls']=dict(rejected=alias_controls)
    write_json(FUTURE_LANE/'match.json',report)
    print(dict(futureBytes=456,pairs=len(traces),actualCallerReturns=144,actualHelperReturnsPerSide=360,sourceCredit=0),flush=True)


if __name__=='__main__':main()
