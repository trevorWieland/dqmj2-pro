import gzip
import json
import sys
from pathlib import Path
import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module,validate
from ov006_cleanup308_fixture_20261031 import execute
from ov006_cleanup308_models_20261031 import ENTRY,NATIVE,recipes
from project import ROOT,configuration,now,sha256,write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

SOURCE=ROOT/'src/overlays/ov006_20261031_cleanup308/source.c'
PINS=ROOT/'evidence/verification/ov006-cleanup308-inputs-20261031.json'
WORK=ROOT/'work/ol308-proof'
REPORT=ROOT/'evidence/matches/ov006-20261031-cleanup308.json'

def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def run():
    if sys.version_info[:3]!=(3,13,5)or __version__!='2.1.4':
        raise ValueError('Cleanup308 pinned Python/Unicorn differs')
    pins=json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:
            raise ValueError('Cleanup308 frozen source/header/fixture/model differs')
    if not all(p.resolve()in{(ROOT/item['path']).resolve()for item in pins['files']}for p in[SOURCE,SOURCE.with_name('context.h')]):
        raise ValueError('Cleanup308 source/header constants are outside pinned inputs')
    config=configuration()
    if sha256(config['rom'])!=config['romSha256']:
        raise ValueError('Cleanup308 measured private ROM differs')
    metadata,overlay,unused=measured_module('ov006')
    main_metadata,main,unused=measured_module('main')
    compiler.WORK=WORK/'c'
    rows,unused=compiler.compare(SOURCE,'ov006','2','off',True,thumb=False)
    if len(rows)!=1 or rows[0].get('compiledBytes')!=104:
        raise ValueError('Cleanup308 complete ordinary C compilation differs')
    row=rows[0]
    row['sourceDependencies']=[dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)),sha256=sha256(SOURCE.with_name('context.h')))]
    bindings=qualified_bindings(row)
    directory=WORK/'l'/row['objectSha256']
    proof=validate(row,bindings,directory)
    linked=(directory/'caller.bin').read_bytes()
    candidate=bytearray(overlay)
    offset=ENTRY-0x021D7240
    candidate[offset:offset+104]=linked
    if bytes(candidate)!=overlay:
        raise ValueError('Cleanup308 complete source/original overlay differs')
    save_link_snapshots.DIRECTORY=WORK/'immutable-links'
    row.update(save_link_snapshots.freeze_link(proof))
    row.update(exactAfterGenuineLink=True,linkedMatchingBytes=104,nativeSymbolEntries=bindings)
    results,summaries=[],[]
    for index,recipe in enumerate(recipes()):
        original=execute(main,overlay,recipe)
        rebuilt=execute(main,bytes(candidate),recipe)
        if original!=rebuilt:
            raise ValueError('Cleanup308 complete source/original executions differ')
        results.append(dict(recipe=recipe,result=original))
        summaries.append(dict(case=index,recipeSha256=compiler.sha(encoded(recipe)),resultSha256=compiler.sha(encoded(original)),actualReturns=2,nativeDependencyActualReturns=2*len(original['nativeDependencyActualReturns']),providedCalls=2*len(original['providedCalls']),instructions=original['instructions'],observedNativeCallerInstructionBytes=len(original['observedCallerInstructionBytes']),ramSha256=original['ramSha256'],stackSha256=original['stackSha256'],pcTraceSha256=compiler.sha(encoded(original['pcTrace'])),writeTraceSha256=compiler.sha(encoded(original['writes']))))
    raw=encoded(dict(romSha256=config['romSha256'],module='ov006',address=hex(ENTRY),results=results))
    compressed=gzip.compress(raw,mtime=0)
    artifact=WORK/'raw-traces'/(compiler.sha(compressed)+'.json.gz')
    artifact.parent.mkdir(parents=True,exist_ok=True)
    artifact.write_bytes(compressed)
    observed=sorted({a for r in results for a in r['result']['observedCallerInstructionBytes']})
    row['oracle']=dict(supported=True,evidenceClass='Independent twenty-five-record cleanup with original SDK pointer arithmetic, nested-null guard, bank-byte getters and word-map store',executions=2*len(results),actualReturns=2*len(results),nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns']for r in summaries),providedCalls=sum(r['providedCalls']for r in summaries),freshMachinePerExecution=True,instructionBound=10000,maximumNativeInstructions=max(r['instructions']for r in summaries),completeImageEquality=True,observedNativeCallerInstructionBytes=len(observed),observedCallerByteOffsets=[a-ENTRY for a in observed],nativeBodies=[dict(processor='arm9',program='',module='main'if a<0x021D7240 else'ov006',mode='arm',address=hex(a),bytes=n,sha256=compiler.sha((main if a<0x021D7240 else overlay)[a-(0x02000000 if a<0x021D7240 else 0x021D7240):a-(0x02000000 if a<0x021D7240 else 0x021D7240)+n]))for a,n in NATIVE.items()],results=summaries,rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)),sha256=compiler.sha(compressed),bytes=len(compressed),format='json+gzip',gzipMtime=0,uncompressedSha256=compiler.sha(raw)),limitations=['All main records02102A18, bank bytes021029D0, map0220F500 and nested-null header objects are supplied BSS fixtures; no original initialization, ownership or scene reachability inferred','Original49AD0 executes all25 lookups for indices4..28; zero first words skip49898, while nonzero pointers execute its original nested-null early return','SDK49898 deeper paths are unsupported; observed R0 is the raw header pointer, not a semantic result meaning or complete original formal ABI proof','Actual48F6C reads the same supplied bank byte twice without intervening writes; banks0..3 are supported by the measured four-word map, other raw bytes remain unsupported','OriginalDDF18/DDF08 preserve the full map word at the same bank; exactly one idempotent data write is independently required, with no invented differing getter results','Native entry volatile register carriers are recorded; no unverified incoming register parameter is fabricated','No providers, device behavior, graphics/resource release or dependency source credit'])
    control=ROOT/'nonmatching/overlay-lane/20261031-cleanup308-negative'
    control.mkdir(parents=True,exist_ok=True)
    old='var_r4 <= 0x1C'
    body=SOURCE.read_text().replace(old,'var_r4 <= 0x1B')
    if body==SOURCE.read_text():
        raise ValueError('Cleanup308 ordinary source control missing')
    for path,text in[(control/'source.c',body),(control/'context.h',SOURCE.with_name('context.h').read_text())]:
        if path.exists()and path.read_bytes()!=text.encode():
            raise ValueError('Cleanup308 preserve earlier control')
        path.write_bytes(text.encode())
    compiler.WORK=WORK/'negative/c'
    bad_rows,unused=compiler.compare(control/'source.c','ov006','2','off',True,thumb=False)
    bad_directory=WORK/'negative/l'
    try:
        bad_link=validate(bad_rows[0],qualified_bindings(bad_rows[0]),bad_directory)
    except ValueError as error:
        bad_link=error.args[0]
    if not isinstance(bad_link,dict)or bad_link.get('caller')!=bad_rows[0]['name']:
        raise ValueError('Cleanup308 ordinary control failed genuine linking')
    directed=recipes()[0]
    try:
        execute(main,overlay,directed,(bad_directory/'caller.bin').read_bytes())
    except ValueError as error:
        failure=error.args[0]
        if failure!='Cleanup308 native entry order differs':
            raise ValueError(('Cleanup308 unexpected control rejection',failure))
    else:
        raise ValueError('Cleanup308 source control unexpectedly passed')
    report=dict(schemaVersion=1,createdUtc=now(),romSha256=config['romSha256'],processor='arm9',program='',module='ov006',mode='arm',moduleInputSha256=metadata['sha256'],mainInputSha256=main_metadata['sha256'],matches=[row],nativeSymbols={item['symbol']:item['target']for item in row['relocations']},isolatedLink=proof,nativeSourceBytes=104,functionMatches=1,acceptedSourceCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,rejectedSourceControl=dict(expectedRejected=True,sourceCredit=0,recipe=directed,failure=failure,compilation=bad_rows,actualLinkComparison=bad_link),inputPins=pins['files'],generatorSha256=sha256(Path(__file__)),limitations=['Module/ROM registration remains integrator-owned','createdUtc is volatile; stable identity excludes only that field','No assembly, opcode patches, invented register parameters, hidden source blobs or dependency source credit'],reproductionCommand='python match_ov006_cleanup308_20261031.py')
    report['deterministicContentSha256']=compiler.sha(encoded({k:v for k,v in report.items()if k!='createdUtc'}))
    write_json(REPORT,report)
    print(json.dumps({k:row['oracle'][k]for k in['actualReturns','nativeDependencyActualReturns','providedCalls','maximumNativeInstructions','observedNativeCallerInstructionBytes']}),flush=True)

if __name__=='__main__':
    run()
