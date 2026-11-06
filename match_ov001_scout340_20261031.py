import gc
import gzip
import json
import sys
from pathlib import Path
import match_runtime as compiler
import unicorn
import save_link_snapshots
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
from project import ROOT,configuration,sha256,write_json
import ov001_scout340_fixture_20261031 as F
BASE=ROOT/'src/overlays/ov001_20261031_scout340'
WORK=ROOT/'work/ol340-proof'
PINS=ROOT/'evidence/verification/ov001-scout340-inputs-20261031.json'

def run():
    if sys.version_info[:3]!=(3,
        13,
        5)or unicorn.__version__!='2.1.4':raise ValueError('Scout340 pinned Python/Unicorn differs')
    pins=json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Scout340 frozen source/fixture/context differs')
    config=configuration()
    if sha256(config['rom'])!=config['romSha256']:raise ValueError('Scout340 measured ROM differs')
    metadata,overlay,unused=measured_module('ov001')
    main_metadata,main,unused=measured_module('main')
    compiler.WORK=WORK/'compile'
    rows,unused=compiler.compare(BASE/'source.c','ov001','2','off',True,thumb=False)
    if len(rows)!=1 or rows[0].get('compiledBytes')!=172:raise ValueError('Scout340 complete source extent differs')
    row=rows[0]
    row['sourceDependencies']=[dict(path=str((BASE/'context.h').relative_to(ROOT)),
            sha256=sha256(BASE/'context.h'))]
    bindings=qualified_bindings(row)
    link=WORK/'link'
    proof=validate(row,bindings,link)
    body=(link/'caller.bin').read_bytes()
    candidate=bytearray(overlay)
    offset=F.ENTRY-0x021D7240
    candidate[offset:offset+172]=body
    if bytes(candidate)!=overlay:raise ValueError('Scout340 complete overlay source/native differs')
    save_link_snapshots.DIRECTORY=WORK/'immutable-link'
    row.update(save_link_snapshots.freeze_link(proof))
    row.update(exactAfterGenuineLink=True,linkedMatchingBytes=172,nativeSymbolEntries=bindings)
    results=[]
    summaries=[]
    for index,recipe in enumerate(F.recipes()):
        original=F.execute(main,overlay,recipe)
        rebuilt=F.execute(main,bytes(candidate),recipe)
        if original!=rebuilt:raise ValueError('Scout340 complete original/source result differs')
        results.append(dict(recipe=recipe,result=original))
        summaries.append(dict(case=index,
                recipe=recipe,
                resultSha256=F.sha(F.encoded(original)),
                actualReturns=2*original['actualReturns'],
                unsupportedInvalidReads=2*original['unsupportedInvalidReads'],
                nativeDependencyActualReturns=2*original['nativeDependencyActualReturns'],
                providedCalls=2*original['providedCalls'],
                instructions=original['instructions'],
                ramSha256=original['ramSha256'],
                expectedSignedField26=original['expectedSignedField26']))
        if index%32==0:gc.collect()
    raw=F.encoded(results)
    zipped=gzip.compress(raw,mtime=0)
    artifact=WORK/'raw-traces'/(F.sha(zipped)+'.json.gz')
    artifact.parent.mkdir(parents=True,exist_ok=True)
    artifact.write_bytes(zipped)
    valid=[r for r in summaries if not r['recipe']['invalid']]
    invalid=[r for r in summaries if r['recipe']['invalid']]
    observed=sorted({a for r in results if not r['recipe']['invalid']for a in r['result']['observedCallerBytes']})
    native=[]
    for address,size in F.NATIVE.items():
        image,base,module=(main,0x02000000,'main')if address<0x021D7240 else(overlay,0x021D7240,'ov001')
        native.append(dict(processor='arm9',
                program='',
                module=module,
                mode='arm',
                address=hex(address),
                bytes=size,
                sha256=F.sha(image[address-base:address-base+size]),
                sourceCredit=0))
    row['oracle']=dict(supported=True,
        evidenceClass='Independent bounded signed-byte accumulator/alias/flag/template-clear model with original native actor resolver, flag getter and memset',
        executions=sum(r['actualReturns']for r in valid),
        actualReturns=sum(r['actualReturns']for r in valid),
        nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns']for r in valid),
        providedCalls=sum(r['providedCalls']for r in valid),
        freshMachinePerExecution=True,
        cpu='ARM946',
        instructionBound=3000,
        maximumInstructions=max(r['instructions']for r in valid),
        completeOriginalSourceResultEquality=True,
        independentFullNonstackRamComparison=True,
        observedCallerInstructionBytes=len(observed),
        observedCallerByteOffsets=[a-F.ENTRY for a in observed],
        nativeBodies=native,
        results=valid,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)),
            sha256=F.sha(zipped),
            uncompressedSha256=F.sha(raw),
            bytes=len(zipped),
            gzipMtime=0),
        limits=['Scene block, slot, actor parameter pointer/value, flag word and lower UI/resource effects are supplied deterministic state; no ordinary scene/lifecycle reachability is claimed',
            'Actual DB438 resolves constant side1 and native valid slots0..2; all256 raw signed parameter bytes and both target flag states execute',
            'Thirty additional alias recipes point parameter+B0 at the halfword cleared first, proving late read yields0 before the400 bonus',
            'Main44424 and08D78 execute original code; lowerF1294/2AC08/63C00 are providers with checked explicit arguments, no memory effects and varied caller-saved register clobbers',
            'Template132-byte clear resets its ready byte67; no normal recruitment record33 value or later template builder state is inferred',
            'Native invalid-slot observations are separate and receive zero top-return credit; they are not supported game error paths or application restrictions',
            'Original native dependencies, BSS data and literal labels receive zero new source/data credit'])
    row['unsupportedStateObservations']=dict(executions=2*len(invalid),
        actualReturns=0,
        invalidReads=sum(r['unsupportedInvalidReads']for r in invalid),
        nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns']for r in invalid),
        providedCalls=sum(r['providedCalls']for r in invalid),
        all253OtherRawSlotBytes=True,
        observation='Native signed-slot conversion yields resolvernull, then caller reads address1E8 atPC021F9640 without an intervening null guard; supplied context40/26 stores occurred first',
        results=invalid,
        limitations=['This isolates invalid synthetic slot states and does not establish actual caller domain or whole-game error handling',
            'No failed caller execution is counted as returned or as additional source credit'])
    controls=[]
    for name,old,new,recipe in[('arithmetic',
            '* 0xA;',
            '* 0xB;',
            F.recipes()[1]),
        ('clear',
            '0, 0x84',
            '0, 0x80',
            F.recipes()[0])]:
        directory=ROOT/'nonmatching/overlay-lane/20261031-scout340-negative'/name
        directory.mkdir(parents=True,exist_ok=True)
        value=(BASE/'source.c').read_text().replace(old,new)
        if value==(BASE/'source.c').read_text():raise ValueError('Scout340 ordinary source control missing')
        for p,text in[(directory/'source.c',value),(directory/'context.h',(BASE/'context.h').read_text())]:
            if p.exists()and p.read_bytes()!=text.encode():raise ValueError('Scout340 preserve frozen control')
            p.write_bytes(text.encode())
        compiler.WORK=WORK/'negative'/name/'compile'
        bad,unused=compiler.compare(directory/'source.c','ov001','2','off',True,thumb=False)
        bad_link=WORK/'negative'/name/'link'
        try:bad_proof=validate(bad[0],qualified_bindings(bad[0]),bad_link)
        except ValueError as error:
            bad_proof=error.args[0]
            if not isinstance(bad_proof,dict)or bad_proof.get('caller')!=bad[0]['name']:raise
        try:F.execute(main,overlay,recipe,(bad_link/'caller.bin').read_bytes())
        except ValueError as error:
            failure=error.args[0]
            if failure!='Scout340 complete independent nonstack RAM differs':raise
        else:raise ValueError('Scout340 ordinary source control unexpectedly passed')
        controls.append(dict(name=name,
                expectedRejected=True,
                failure=failure,
                compilation=bad,
                realLinkComparison=bad_proof,
                sourceCredit=0))
    row['rejectedOrdinarySourceControls']=controls
    report=dict(schemaVersion=1,
        romSha256=config['romSha256'],
        processor='arm9',
        program='',
        module='ov001',
        mode='arm',
        moduleInputSha256=metadata['sha256'],
        mainInputSha256=main_metadata['sha256'],
        matches=[row],
        nativeSourceBytes=172,
        functionMatches=1,
        acceptedSourceCredit=0,
        wholeModuleLinked=False,
        sourceReconstructionComplete=False,
        compilationExplanation='Natural signed32 accumulator preserves the original zero/MUL-accumulate lifetime; previous folded/narrow expressions selectedSMULBB and remained166/172',
        experiments=[dict(path='evidence/attempts/ov001-scout339-natural-profiles-20261031.json',
                sha256=sha256(ROOT/'evidence/attempts/ov001-scout339-natural-profiles-20261031.json'))],
        inputFiles=[dict(path=p,
                sha256=sha256(ROOT/p))for p in['ov001_scout340_fixture_20261031.py',
                'src/overlays/ov001_20261031_scout340/source.c',
                'src/overlays/ov001_20261031_scout340/context.h']],
        inputPins=pins['files'],
        generatorSha256=sha256(__file__),
        reproductionCommand='python match_ov001_scout340_20261031.py',
        limitations=['Final acceptance/module/ROM verification belongs to the integrator',
            'Source pending acceptance; all earlier sources and negative experiments stay frozen',
            'No assembly, opcode patch, forced register, artificial padding, fake incoming argument or project-wide ABI migration'])
    write_json(ROOT/'evidence/matches/ov001-20261031-scout340.json',report)
    print(json.dumps(dict(bytes=172,
                actualReturns=row['oracle']['actualReturns'],
                nativeDependencyActualReturns=row['oracle']['nativeDependencyActualReturns'],
                providedCalls=row['oracle']['providedCalls'],
                invalidExecutions=row['unsupportedStateObservations']['executions'],
                invalidActualReturns=0,
                observedCallerInstructionBytes=len(observed))))

if __name__=='__main__':run()
