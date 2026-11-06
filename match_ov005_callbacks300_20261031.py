import gzip
import json
import sys
from pathlib import Path
import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module,validate
from ov005_callbacks300_fixture_20261031 import execute
from ov005_callbacks300_models_20261031 import UPDATE,EXIT,SPECS,NATIVE,recipes,table_data
from project import ROOT,configuration,now,sha256,write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

BASE=ROOT/'src/overlays/ov005_20261031_callbacks300'
PINS=ROOT/'evidence/verification/ov005-callbacks300-inputs-20261031.json'
WORK=ROOT/'work/ol300-proof'
REPORT=ROOT/'evidence/matches/ov005-20261031-callbacks300.json'

def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def run():
    if sys.version_info[:3]!=(3,13,5)or __version__!='2.1.4':
        raise ValueError('Callbacks300 pinned Python/Unicorn differs')
    pins=json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:
            raise ValueError('Callbacks300 frozen source/header/fixture/model differs')
    config=configuration()
    if sha256(config['rom'])!=config['romSha256']:
        raise ValueError('Callbacks300 measured private ROM differs')
    metadata,overlay,unused=measured_module('ov005')
    main_metadata,main,unused=measured_module('main')
    matches=[]
    for entry,directory in[(UPDATE,'update'),(EXIT,'exit')]:
        source=BASE/directory/'source.c'
        compiler.WORK=WORK/directory/'c'
        rows,unused=compiler.compare(source,'ov005','2','off',True,thumb=False)
        if len(rows)!=1 or rows[0].get('compiledBytes')!=SPECS[entry]:
            raise ValueError('Callbacks300 complete ordinary source compilation differs')
        row=rows[0]
        row['sourceDependencies']=[dict(path=str(source.with_name('context.h').relative_to(ROOT)),sha256=sha256(source.with_name('context.h')))]
        bindings=qualified_bindings(row)
        link_directory=WORK/directory/'l'/row['objectSha256']
        proof=validate(row,bindings,link_directory)
        linked=(link_directory/'caller.bin').read_bytes()
        candidate=bytearray(overlay)
        offset=entry-0x021D7240
        candidate[offset:offset+SPECS[entry]]=linked
        if bytes(candidate)!=overlay:
            raise ValueError('Callbacks300 complete source/original overlay differs')
        save_link_snapshots.DIRECTORY=WORK/directory/'immutable-links'
        row.update(save_link_snapshots.freeze_link(proof))
        row['exactAfterGenuineLink']=True
        row['linkedMatchingBytes']=SPECS[entry]
        row['nativeSymbolEntries']=bindings
        results,summaries=[],[]
        for index,recipe in enumerate(r for r in recipes()if r['entry']==entry):
            original=execute(main,overlay,recipe)
            rebuilt=execute(main,bytes(candidate),recipe)
            if original!=rebuilt:
                raise ValueError('Callbacks300 complete source/original execution differs')
            results.append(dict(recipe=recipe,result=original))
            summaries.append(dict(case=index,recipeSha256=compiler.sha(encoded(recipe)),resultSha256=compiler.sha(encoded(original)),actualReturns=2,nativeDependencyActualReturns=2*len(original['nativeDependencyActualReturns']),providedCalls=2*len(original['providedCalls']),instructions=original['instructions'],observedNativeCallerInstructionBytes=len(original['observedCallerInstructionBytes']),ramSha256=original['ramSha256'],stackSha256=original['stackSha256'],pcTraceSha256=compiler.sha(encoded(original['pcTrace'])),writeTraceSha256=compiler.sha(encoded(original['writes']))))
        raw=encoded(dict(romSha256=config['romSha256'],module='ov005',address=hex(entry),results=results))
        compressed=gzip.compress(raw,mtime=0)
        artifact=WORK/directory/'raw-traces'/(compiler.sha(compressed)+'.json.gz')
        artifact.parent.mkdir(parents=True,exist_ok=True)
        artifact.write_bytes(compressed)
        observed=sorted({a for r in results for a in r['result']['observedCallerInstructionBytes']})
        native_addresses={int(item['address'],16)for r in results for item in r['result']['nativeDependencyActualReturns']}
        row['oracle']=dict(supported=True,evidenceClass='Independent bounded update/exit state models with actual original getters, gate, cleanup loops and pointer clear; explicit lower providers',executions=2*len(results),actualReturns=2*len(results),nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns']for r in summaries),providedCalls=sum(r['providedCalls']for r in summaries),freshMachinePerExecution=True,instructionBound=10000,maximumNativeInstructions=max(r['instructions']for r in summaries),completeImageEquality=True,observedNativeCallerInstructionBytes=len(observed),observedCallerByteOffsets=[a-entry for a in observed],nativeBodies=[dict(processor='arm9',program='',module='main'if a<0x021D7240 else'ov005',mode='arm',address=hex(a),bytes=NATIVE[a],sha256=compiler.sha((main if a<0x021D7240 else overlay)[a-(0x02000000 if a<0x021D7240 else 0x021D7240):a-(0x02000000 if a<0x021D7240 else 0x021D7240)+NATIVE[a]]))for a in sorted(native_addresses)],results=summaries,rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)),sha256=compiler.sha(compressed),bytes=len(compressed),format='json+gzip',gzipMtime=0,uncompressedSha256=compiler.sha(raw)),limits=['All BSS state, pointer objects, record arrays, raw flags/keys, slot-map values and lower-provider effects are supplied deterministic fixtures; no ordinary lifecycle or full-scene reachability inferred','Native gate09DC executes its raw-word early return, key-mask and cleanup paths; its key getter2A634 and lower UI/resource operations are providers','Updater samples all256 ECB raw bytes, all61 original callback-table slots, special selector61, unsigned counter wrap and late flag/counter reads; unlisted/invalid indices are unsupported','Callback arguments remain zero explicit words with rawR0 code-pointer carriers recorded; original formal callback signatures and bodies remain unqualified','Exit89B64 is a Thumb provider entered through actual source/original BLX; other lower SDK/UI/cache operations remain ARM providers with checked explicit arguments and declared synthetic effects','Native06A0 traverses26 supplied records at indices4..29 and uses supplied48F6C return values whose low signed byte is0..3; original SDK domain and other indices remain unqualified','NativeDFA64/DFA54 read/write a supplied four-word map at021ED11C; full word values and alias indices are preserved, without asserting original object typedef','NativeFEB8/E0B10 execute original code, including null/nonnull485B4, raw127 resource flag, signed release-byte reread and three descriptor references; lower release bodies are provided','Physical exitR0 forwards the supplied653AC result, with no semantic return meaning or wide-return claim','Original dependency bodies, callback table bytes and BSS test data receive zero new function/source/data credit'])
        old,new=('+= 1U;','+= 2U;')if entry==UPDATE else('native_fn_020befb8(0);','native_fn_020befb8(1);')
        control=ROOT/'nonmatching/overlay-lane/20261031-callbacks300-negative'/directory
        control.mkdir(parents=True,exist_ok=True)
        body=source.read_text().replace(old,new)
        if body==source.read_text():
            raise ValueError('Callbacks300 ordinary source control missing')
        for path,text in[(control/'source.c',body),(control/'context.h',source.with_name('context.h').read_text())]:
            if path.exists()and path.read_bytes()!=text.encode():
                raise ValueError('Callbacks300 preserve frozen control')
            path.write_bytes(text.encode())
        compiler.WORK=WORK/directory/'negative/c'
        bad_rows,unused=compiler.compare(control/'source.c','ov005','2','off',True,thumb=False)
        bad_directory=WORK/directory/'negative/l'
        try:
            bad_link=validate(bad_rows[0],qualified_bindings(bad_rows[0]),bad_directory)
        except ValueError as error:
            bad_link=error.args[0]
        if not isinstance(bad_link,dict)or bad_link.get('caller')!=bad_rows[0]['name']:
            raise ValueError('Callbacks300 ordinary control failed genuine linking')
        directed=next(r for r in recipes()if r['entry']==entry and(entry!=UPDATE or(r['byte']==0 and r['aux28']==0)))
        try:
            execute(main,overlay,directed,(bad_directory/'caller.bin').read_bytes())
        except ValueError as error:
            failure=error.args[0]
            expected='Callbacks300 complete independent RAM differs'if entry==UPDATE else'Callbacks300 independent provider arguments differ'
            if failure!=expected and not(isinstance(failure,tuple)and failure[0]==expected):
                raise ValueError(('Callbacks300 unexpected control rejection',failure))
        else:
            raise ValueError('Callbacks300 ordinary source control unexpectedly passed')
        row['rejectedSourceControl']=dict(expectedRejected=True,sourceCredit=0,recipe=directed,failure=failure,compilation=bad_rows,actualLinkComparison=bad_link)
        matches.append(row)
        print(json.dumps(dict(address=hex(entry),bytes=SPECS[entry],actualReturns=row['oracle']['actualReturns'],nativeDependencyActualReturns=row['oracle']['nativeDependencyActualReturns'],providedCalls=row['oracle']['providedCalls'])),flush=True)
    report=dict(schemaVersion=1,createdUtc=now(),romSha256=config['romSha256'],processor='arm9',program='',module='ov005',mode='arm',moduleInputSha256=metadata['sha256'],mainInputSha256=main_metadata['sha256'],matches=matches,nativeSymbols={item['symbol']:item['target']for row in matches for item in row['relocations']},nativeSourceBytes=sum(SPECS.values()),functionMatches=2,acceptedSourceCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,callbackTable=dict(address='0x021E7778',nextSymbol='0x021E786C',bytes=244,sha256=compiler.sha(table_data()),authoredDataCredit=0),inputPins=pins['files'],generatorSha256=sha256(Path(__file__)),conservativeMinimumCounterexample=dict(report='evidence/verification/main-pointer-clear299-20261031.json',sha256=sha256(ROOT/'evidence/verification/main-pointer-clear299-20261031.json'),actualReturns=256,sourceCredit=0),limitations=['Final module/ROM registration remains integrator responsibility','createdUtc is volatile; stable identity excludes only that field','Source callbacks and SDK prototypes are scope-qualified call views, without a project-wide ABI migration','No assembly, opcode patching, invented incoming registers or dependency credit'],reproductionCommand='python match_ov005_callbacks300_20261031.py')
    report['deterministicContentSha256']=compiler.sha(encoded({k:v for k,v in report.items()if k!='createdUtc'}))
    write_json(REPORT,report)

if __name__=='__main__':
    run()
