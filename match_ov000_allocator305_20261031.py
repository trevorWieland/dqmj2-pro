import gzip
import json
import sys
from pathlib import Path
import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module,validate
from ov000_allocator305_fixture_20261031 import execute
from ov000_allocator305_models_20261031 import ENTRY,NATIVE,recipes,table_data
from project import ROOT,configuration,now,sha256,write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCE=ROOT/'src/overlays/ov000_20261031_allocator305/source.c'
PINS=ROOT/'evidence/verification/ov000-allocator305-inputs-20261031.json'
WORK=ROOT/'work/ol305-proof'
REPORT=ROOT/'evidence/matches/ov000-20261031-allocator305.json'

def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def run():
    if sys.version_info[:3]!=(3,13,5)or __version__!='2.1.4':
        raise ValueError('Allocator305 pinned Python/Unicorn differs')
    pins=json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:
            raise ValueError('Allocator305 frozen source/header/fixture/model differs')
    config=configuration()
    if sha256(config['rom'])!=config['romSha256']:
        raise ValueError('Allocator305 measured private ROM differs')
    metadata,overlay,unused=measured_module('ov000')
    main_metadata,main,unused=measured_module('main')
    compiler.WORK=WORK/'c'
    rows,unused=compiler.compare(SOURCE,'ov000','2','off',True,thumb=False)
    if len(rows)!=1 or rows[0].get('compiledBytes')!=200:
        raise ValueError('Allocator305 complete ordinary C compilation differs')
    row=rows[0]
    row['sourceDependencies']=[dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)),sha256=sha256(SOURCE.with_name('context.h')))]
    bindings=qualified_bindings(row)
    directory=WORK/'l'/row['objectSha256']
    proof=validate(row,bindings,directory)
    linked=(directory/'caller.bin').read_bytes()
    candidate=bytearray(overlay)
    offset=ENTRY-0x021D7240
    candidate[offset:offset+200]=linked
    if bytes(candidate)!=overlay:
        raise ValueError('Allocator305 complete source/original overlay differs')
    save_link_snapshots.DIRECTORY=WORK/'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    row.update(exactAfterGenuineLink=True,linkedMatchingBytes=200,nativeSymbolEntries=bindings)
    results,summaries=[],[]
    for index,recipe in enumerate(recipes()):
        original=execute(main,overlay,recipe)
        rebuilt=execute(main,bytes(candidate),recipe)
        if original!=rebuilt:
            raise ValueError('Allocator305 complete source/original executions differ')
        results.append(dict(recipe=recipe,result=original))
        summaries.append(dict(case=index,recipeSha256=compiler.sha(encoded(recipe)),resultSha256=compiler.sha(encoded(original)),actualReturns=2,nativeDependencyActualReturns=2*len(original['nativeDependencyActualReturns']),providedCalls=2*len(original['providedCalls']),instructions=original['instructions'],observedNativeCallerInstructionBytes=len(original['observedCallerInstructionBytes']),ramSha256=original['ramSha256'],stackSha256=original['stackSha256'],pcTraceSha256=compiler.sha(encoded(original['pcTrace'])),writeTraceSha256=compiler.sha(encoded(original['writes']))))
    raw=encoded(dict(romSha256=config['romSha256'],module='ov000',address=hex(ENTRY),results=results))
    compressed=gzip.compress(raw,mtime=0)
    artifact=WORK/'raw-traces'/(compiler.sha(compressed)+'.json.gz')
    artifact.parent.mkdir(parents=True,exist_ok=True)
    artifact.write_bytes(compressed)
    observed=sorted({a for r in results for a in r['result']['observedCallerInstructionBytes']})
    row['oracle']=dict(supported=True,evidenceClass='Independent sixteen-record allocator with original token scans, eight-record descriptor lookup and native setup zero-result branch',executions=2*len(results),actualReturns=2*len(results),nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns']for r in summaries),providedCalls=sum(r['providedCalls']for r in summaries),freshMachinePerExecution=True,instructionBound=10000,maximumNativeInstructions=max(r['instructions']for r in summaries),completeImageEquality=True,observedNativeCallerInstructionBytes=len(observed),observedCallerByteOffsets=[a-ENTRY for a in observed],nativeBodies=[dict(processor='arm9',program='',module='ov000',mode='arm',address=hex(a),bytes=n,sha256=compiler.sha(overlay[a-0x021D7240:a-0x021D7240+n]))for a,n in NATIVE.items()],results=summaries,rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)),sha256=compiler.sha(compressed),bytes=len(compressed),format='json+gzip',gzipMtime=0,uncompressedSha256=compiler.sha(raw)),table=dict(address='0x0222BAF4',nextSymbol='0x0222BB18',bytes=36,sha256=compiler.sha(table_data()),authoredDataCredit=0),limitations=['Record arena02243E3C, token words02231F64 and descriptors0224373C are supplied BSS fixtures; no original construction, ordinary scene reachability, ownership or lifecycle inferred','All16 first-free positions and a full arena are exercised, with raw nonzero occupied bytes and later free records; full arenas returnFFFFFFFF without calls or writes','All18 selectors use the actual original36-byte halfword table bounded by the next configured symbol; other selectors remain unsupported','Caller input words1..4 retain all32 bits; stack-byte fields and signed halfword field use low8/16 bits with independent upper padding patterns','OriginalDF950/DF544/DF578 cover raw token present and absent/full table branches; the resource-copy/loading branch is unsupported','Original212F80 and212804 run with supplied first matching descriptor among8 records; main4106C remains a provider returning0, so later setup paths remain unsupported','Native stack scale, rotation and position vectors are independently checked before the SDK boundary; volatile register carriers are recorded without asserting additional formal arguments','No actual SDK zero-result preconditions, resource validity, renderer behavior or native scene semantics are certified','Dependencies, original table bytes and supplied BSS gain zero new source/function/data credit'])
    control=ROOT/'nonmatching/overlay-lane/20261031-allocator305-negative'
    control.mkdir(parents=True,exist_ok=True)
    old='M2C_FIELD(temp_r5, s8 *, 0x105) = 1;'
    body=SOURCE.read_text().replace(old,old.replace('= 1;','= 2;'))
    if body==SOURCE.read_text():
        raise ValueError('Allocator305 ordinary source control missing')
    for path,text in[(control/'source.c',body),(control/'context.h',SOURCE.with_name('context.h').read_text())]:
        if path.exists()and path.read_bytes()!=text.encode():
            raise ValueError('Allocator305 preserve earlier control')
        path.write_bytes(text.encode())
    compiler.WORK=WORK/'negative/c'
    bad_rows,unused=compiler.compare(control/'source.c','ov000','2','off',True,thumb=False)
    bad_directory=WORK/'negative/l'
    try:
        bad_link=validate(bad_rows[0],qualified_bindings(bad_rows[0]),bad_directory)
    except ValueError as error:
        bad_link=error.args[0]
    if not isinstance(bad_link,dict)or bad_link.get('caller')!=bad_rows[0]['name']:
        raise ValueError('Allocator305 ordinary control failed genuine linking')
    directed=recipes()[0]
    try:
        execute(main,overlay,directed,(bad_directory/'caller.bin').read_bytes())
    except ValueError as error:
        failure=error.args[0]
        if failure!='Allocator305 independent ordered state differs':
            raise ValueError(('Allocator305 unexpected control rejection',failure))
    else:
        raise ValueError('Allocator305 source control unexpectedly passed')
    report=dict(schemaVersion=1,createdUtc=now(),romSha256=config['romSha256'],processor='arm9',program='',module='ov000',mode='arm',moduleInputSha256=metadata['sha256'],mainInputSha256=main_metadata['sha256'],matches=[row],nativeSymbols={item['symbol']:item['target']for item in row['relocations']},isolatedLink=proof,nativeSourceBytes=200,functionMatches=1,acceptedSourceCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,rejectedSourceControl=dict(expectedRejected=True,sourceCredit=0,recipe=directed,failure=failure,compilation=bad_rows,actualLinkComparison=bad_link),inputPins=pins['files'],generatorSha256=sha256(Path(__file__)),limitations=['Module/ROM registration remains integrator-owned','createdUtc is volatile; stable identity excludes only that field','No assembly, opcode patches, invented register parameters, hidden source blobs or dependency source credit'],reproductionCommand='python match_ov000_allocator305_20261031.py')
    report['deterministicContentSha256']=compiler.sha(encoded({k:v for k,v in report.items()if k!='createdUtc'}))
    write_json(REPORT,report)
    print(json.dumps({k:row['oracle'][k]for k in['actualReturns','nativeDependencyActualReturns','providedCalls','maximumNativeInstructions','observedNativeCallerInstructionBytes']}),flush=True)

if __name__=='__main__':
    run()
