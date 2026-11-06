import gc
import gzip
import json
import sys
from pathlib import Path
import match_runtime as c
import unicorn
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
import ov001_template349_fixture_20261031 as F
import ov001_template349_models_20261031 as M
import probe_ov000_birth329_20261031 as B
SOURCE=ROOT/'nonmatching/overlay-lane/20261031-template348/plain-division-array/source.c'
WORK=ROOT/'work/ol349-proof'
PINS=ROOT/'evidence/verification/ov001-template349-inputs-20261031.json'

def encoded(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()

def execute(arm,save,assets,overlay,recipe,body=None):
    obj=F.Machine(arm,save,assets,overlay,recipe['seed'])
    actor,parameter=M.setup(obj,recipe)
    obj.captureOriginal=body is None
    if body is not None:obj.u.mem_write(F.ENTRY,body)
    before=bytes(obj.u.mem_read(0x02000000,0x800000))
    expected,template=M.model(before,recipe,actor,parameter,assets)
    value=obj.call_template(0 if recipe['null']else M.ACTOR)
    after=bytes(obj.u.mem_read(0x02000000,0x800000))
    lo,hi=B.STACK-0x10000-0x02000000,B.STACK+0x1000-0x02000000
    if after[:lo]!=expected[:lo]or after[hi:]!=expected[hi:]:
        bad=next(i for i,(a,b)in enumerate(zip(after,expected))if a!=b and not lo<=i<hi)
        raise ValueError(('Template349 complete independent nonstack RAM differs',
                hex(0x02000000+bad),
                after[bad],
                expected[bad]))
    if value!=(0 if recipe['null']else 1):raise ValueError('Template349 independent return differs')
    if any(r['entry']=='0x203d294'for r in obj.trace):raise ValueError('Template349 unexpected scoped RNG call')
    after_template=bytes(obj.u.mem_read(M.TEMPLATE,132))
    result=dict(actualReturns=1,
        result=value,
        instructions=obj.steps,
        template=after_template.hex(),
        templateSha256=c.sha(after_template),
        raw13=after_template[0x13],
        nativeDependencyActualReturns=len(obj.returned)-1,
        providedCalls=0,
        observedOriginalCodeBytes=sorted(obj.observed),
        trace=obj.trace,
        nativeReturns=obj.returned,
        writes=obj.writes,
        nonstackRamSha256=c.sha(after[:lo]+after[hi:]),
        rngCalls=0)
    del obj
    return result

def run():
    if sys.version_info[:3]!=(3,
        13,
        5)or unicorn.__version__!='2.1.4':raise ValueError('Template349 pinned runtime differs')
    pins=json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Template349 frozen source/fixture/ABI inputs differ')
    arm,save,assets=B.inputs()
    metadata,overlay,unused=measured_module('ov001')
    c.WORK=WORK/'compile'
    rows,unused=c.compare(SOURCE,'ov001','2','off',True,thumb=False)
    row=rows[0]
    row['sourceDependencies']=[dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)),
            sha256=sha256(SOURCE.with_name('context.h')))]
    link=WORK/'link'
    try:proof=validate(row,qualified_bindings(row),link)
    except ValueError as error:
        proof=error.args[0]
        if not isinstance(proof,dict)or proof.get('caller')!=row['name']:raise
    body=(link/'caller.bin').read_bytes()
    results=[]
    for index,recipe in enumerate(M.recipes(assets)):
        original=execute(arm,save,assets,overlay,recipe)
        candidate=execute(arm,save,assets,overlay,recipe,body)
        for field in['template','raw13','rngCalls','providedCalls','result']:
            if original[field]!=candidate[field]:raise ValueError(('Template349 native/source relevant effects differ',
                    field,
                    recipe))
        results.append(dict(recipe=recipe,original=original,candidate=candidate))
        gc.collect()
    c.WORK=WORK/'negative-legacy/compile'
    old_rows,unused=c.compare(ROOT/'nonmatching/overlay-lane/20261031-scout338/ov001/021fb214-arm/source.c',
        'ov001',
        '2',
        'off',
        True,
        thumb=False)
    old=old_rows[0]
    old_link=WORK/'negative-legacy'
    try:old_proof=validate(old,qualified_bindings(old),old_link)
    except ValueError as error:
        old_proof=error.args[0]
        if not isinstance(old_proof,dict)or old_proof.get('caller')!=old['name']:raise
    try:execute(arm,save,assets,overlay,M.recipes(assets)[0],(old_link/'caller.bin').read_bytes())
    except Exception as error:
        from unicorn import UcError,UC_ERR_READ_UNMAPPED
        if not isinstance(error,UcError)or error.errno!=UC_ERR_READ_UNMAPPED:raise
        rejection=repr(error)
    else:raise ValueError('Template349 older unaccepted extra-sign/erased-input draft unexpectedly passed')
    control=ROOT/'nonmatching/overlay-lane/20261031-template349-negative'
    control.mkdir(parents=True,exist_ok=True)
    text=SOURCE.read_text()
    for name in['sp0','temp_r11','temp_r4','temp_r5','temp_r6','temp_r8']:
        original='(('+name+' * var_r9) / 100)'
        bad='(((u32) ('+name+' * var_r9) >> 0x1F) + (('+name+' * var_r9) / 100))'
        if text.count(original)!=1:raise ValueError('Template349 signed arithmetic control pattern missing')
        text=text.replace(original,bad)
    for path,value in[(control/'source.c',
            text),
        (control/'context.h',
            SOURCE.with_name('context.h').read_text())]:
        if path.exists()and path.read_bytes()!=value.encode():raise ValueError('Template349 preserve control')
        path.write_bytes(value.encode())
    c.WORK=WORK/'negative-arithmetic/compile'
    bad_rows,unused=c.compare(control/'source.c','ov001','2','off',True,thumb=False)
    bad_link=WORK/'negative-arithmetic/link'
    try:bad_proof=validate(bad_rows[0],qualified_bindings(bad_rows[0]),bad_link)
    except ValueError as error:
        bad_proof=error.args[0]
        if not isinstance(bad_proof,dict)or bad_proof.get('caller')!=bad_rows[0]['name']:raise
    try:execute(arm,save,assets,overlay,M.recipes(assets)[0],(bad_link/'caller.bin').read_bytes())
    except ValueError as error:
        arithmetic_rejection=error.args[0]
        if not isinstance(arithmetic_rejection,
            tuple)or arithmetic_rejection[:2]!=('Template349 complete independent nonstack RAM differs',
            '0x2239abc'):raise
    else:raise ValueError('Template349 extra-sign control unexpectedly passed')
    arithmetic_control=dict(sourceCredit=0,
        compilation=bad_rows,
        genuineLinkComparison=bad_proof,
        expectedRejected=True,
        failure=arithmetic_rejection)
    raw=encoded(results)
    zipped=gzip.compress(raw,mtime=0)
    artifact=WORK/'raw-traces'/(c.sha(zipped)+'.json.gz')
    artifact.parent.mkdir(parents=True,exist_ok=True)
    artifact.write_bytes(zipped)
    report=dict(schemaVersion=1,
        romSha256=configuration()['romSha256'],
        processor='arm9',
        program='',
        module='ov001',
        mode='arm',
        address=hex(F.ENTRY),
        bytes=1352,
        moduleSha256=metadata['sha256'],
        sourceCredit=0,
        exact=False,
        sourceReconstructionComplete=False,
        compilation=row,
        genuineLinkComparison=proof,
        pairs=len(results),
        actualReturns=2*len(results),
        originalNativeDependencyActualReturns=sum(r['original']['nativeDependencyActualReturns']for r in results),
        candidateNativeDependencyActualReturns=sum(r['candidate']['nativeDependencyActualReturns']for r in results),
        providedCalls=0,
        freshMachinePerExecution=True,
        cpu='ARM946',
        instructionBound=200000,
        maximumInstructions=max(r[k]['instructions']for r in results for k in['original',
                'candidate']),
        independentFullNonstackRamComparison=True,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)),
            sha256=c.sha(zipped),
            uncompressedSha256=c.sha(raw),
            bytes=len(zipped),
            gzipMtime=0),
        results=[dict(recipe=r['recipe'],
                actualReturns=2,
                originalSha256=c.sha(encoded(r['original'])),
                candidateSha256=c.sha(encoded(r['candidate'])),
                raw13=r['original']['raw13'],
                instructions=[r['original']['instructions'],
                    r['candidate']['instructions']])for r in results],
        rejectedOlderDraft=dict(sourceCredit=0,
            compilation=old,
            realLinkComparison=old_proof,
            expectedRejected=True,
            failure=rejection),
        rejectedArithmeticControl=arithmetic_control,
        observedOriginalCallerInstructionBytes=len({a for r in results for a in r['original']['observedOriginalCodeBytes']}),
        qualifiedGetter347=dict(path='evidence/verification/main-row43-347-native-20261031.json',
            sha256=sha256(ROOT/'evidence/verification/main-row43-347-native-20261031.json')),
        limits=['Zero source/function credit: source1340-byte genuine output remains different from original1352; this is a complete functional draft in a qualified subset',
            'Raw mode3/7, supplied actor/parameter block and actual measured assets execute original helpers without any function provider',
            'Normal raw modes, percentage RNG/XP-file setup, extra-skill selection and other caller/lifecycle states remain untested',
            'Null actor and signed16 stat/addend extremes, both raw flag10 histories, packed species alias, raw variant values and contiguous/gapped skill pairs are modeled independently',
            'Whole nonstack RAM is independently modeled for each execution; original/source code and stack placement differ and are not claimed identical',
            'Main63C00 raw flag10 setter and its conditional second bank/flag76 effects execute and match three-word bit models; no progression meaning or persistence is inferred',
            'Raw template13 is cleared and remains0 in these runs, but this does not establish every ordinary scouting/newborn context or a game field name',
            'Caller physical species/variant words at44F9C are restored in this fresh source; accepted void-signature source and prior projections remain unchanged',
            'No assembly, opcode patch, fake input register, accepted-source edit or application change'],
        inputPins=pins['files'],mainInputSha256=c.sha(arm),assetHashes={k:c.sha(v)for k,v in assets.items()},generatorSha256=sha256(__file__),
        reproductionCommand='python prove_ov001_template349_20261031.py')
    write_json(ROOT/'evidence/application/ov001-template349-functional-20261031.json',report)
    print(json.dumps({k:report[k]for k in['pairs',
                    'actualReturns',
                    'originalNativeDependencyActualReturns',
                    'candidateNativeDependencyActualReturns',
                    'providedCalls',
                    'maximumInstructions',
                    'exact']}))

if __name__=='__main__':run()
