import gc
import gzip
import json
import struct
import sys
from pathlib import Path
import match_runtime as compiler
import unicorn
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
from project import ROOT,configuration,sha256,write_json
from probe_ov000_birth329_20261031 import BirthMachine,inputs,ENTRY,CAPS,STACK,SAVED_START,SAVED_END
import ov000_birth330_models_20261031 as M
BASE=ROOT/'nonmatching/overlay-lane/20261031-birth330'
WORK=ROOT/'work/ol330-proof'

def digest(raw):return compiler.sha(raw)
def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def execute(arm,save,assets,overlay,recipe,body=None):
    obj=BirthMachine(arm,save,assets,overlay,recipe['seed'])
    if body is not None:obj.u.mem_write(ENTRY,body)
    rows=[save[0x1E8+i*132:0x1E8+(i+1)*132]for i in range(100)]
    args,pointers,parents=M.setup(obj,rows,recipe)
    before=bytes(obj.u.mem_read(0x02000000,0x800000))
    expected,caps=M.model(before,args,pointers,parents,assets,recipe['seed'])
    if obj.birth(args)!=M.CHILD:raise ValueError('Birth330 scratch pointer differs')
    after=bytes(obj.u.mem_read(0x02000000,0x800000))
    cut=STACK-0x10000-0x02000000
    end=STACK+0x1000-0x02000000
    if after[:cut]!=expected[:cut]or after[end:]!=expected[end:]:
        bad=next(i for i,(a,b)in enumerate(zip(after,expected))if a!=b and not cut<=i<end)
        raise ValueError(('Birth330 independent nonstack RAM differs',
                hex(0x02000000+bad),
                after[bad],
                expected[bad]))
    expected_calls=[]
    for offset,cap,entry in zip(M.OFFSETS,caps,CAPS):
        average=(M.word(parents[0],offset,2,True)+M.word(parents[1],offset,2,True))>>2
        expected_calls.extend([(entry,cap)]*(2 if average>=cap else 1))
    observed=[(int(r['entry'],0),r['result'])for r in obj.returned if int(r['entry'],0)in CAPS]
    if expected_calls!=observed:raise ValueError('Birth330 independent cap call/results differ')
    cap_args=[args[2],
        0,
        M.word(parents[0],
            0x18,
            2,
            True)&0xFFFFFFFF,
        parents[0][0x1A],
        M.word(parents[1],
            0x18,
            2,
            True)&0xFFFFFFFF,
        parents[1][0x1A]]
    for event in obj.trace:
        if int(event['entry'],0)in CAPS and event['arguments']+event['stackWords']!=cap_args:
            raise ValueError('Birth330 six caller words differ')
    if any(r['entry']=='0x203d294'for r in obj.trace):raise ValueError('Birth330 unexpected scoped RNG call')
    if len([r for r in obj.trace if r['provider']])!=1:raise ValueError('Birth330 supplied XP count differs')
    child=after[M.CHILD-0x02000000:M.CHILD-0x02000000+132]
    if child[0x33]!=recipe['scratch33']:raise ValueError('Birth330 raw33 preservation differs')
    result=dict(actualReturns=1,
        instructions=obj.steps,
        nativeDependencyActualReturns=len(obj.returned)-1,
        providedCalls=1,
        arguments=args,
        childSha256=digest(child),
        savedRegionUnchanged=after[SAVED_START-0x02000000:SAVED_END-0x02000000]==before[SAVED_START-0x02000000:SAVED_END-0x02000000],
        raw33=child[0x33],
        rngCalls=0,
        trace=obj.trace,
        nativeReturns=obj.returned,
        writes=obj.writes,
        output=child.hex(),
        caps=list(caps))
    if not result['savedRegionUnchanged']:raise ValueError('Birth330 saved input changed')
    del obj
    return result

def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':
        raise ValueError('Birth330 pinned Python/Unicorn differs')
    arm,save,assets=inputs()
    metadata,overlay,unused=measured_module('ov000')
    compiler.WORK=WORK/'compile'
    rows,unused=compiler.compare(BASE/'source.c','ov000','2','off',False,thumb=False)
    if len(rows)!=1:raise ValueError('Birth330 source unit differs')
    row=rows[0]
    row['sourceDependencies']=[dict(path=str(p.relative_to(ROOT)),
            sha256=sha256(p))for p in sorted(BASE.glob('*'))if p.suffix in['.h',
            '.inc']]
    bindings=qualified_bindings(row)
    link=WORK/'real-link'
    try:proof=validate(row,bindings,link)
    except ValueError as error:
        proof=error.args[0]
        if not isinstance(proof,dict)or proof.get('caller')!=row['name']:raise
    body=(link/'caller.bin').read_bytes()
    if len(body)!=row['compiledBytes']:raise ValueError('Birth330 full actual linked extent differs')
    results=[]
    for recipe in M.recipes():
        original=execute(arm,save,assets,overlay,recipe)
        candidate=execute(arm,save,assets,overlay,recipe,body)
        for field in['output',
            'caps',
            'savedRegionUnchanged',
            'raw33',
            'rngCalls',
            'providedCalls',
            'nativeDependencyActualReturns']:
            if original[field]!=candidate[field]:raise ValueError(('Birth330 original/C relevant effect differs',
                    field,
                    recipe))
        results.append(dict(recipe=recipe,original=original,candidate=candidate))
        gc.collect()
    control=ROOT/'nonmatching/overlay-lane/20261031-birth330-negative'
    control.mkdir(parents=True,exist_ok=True)
    for path in sorted(BASE.glob('*')):
        value=path.read_text()
        if path.name=='part01.inc':
            changed=value.replace('var_r2_2 = arg4 +','var_r2_2 = 1 + arg4 +')
            if changed==value:raise ValueError('Birth330 skill-point source control missing')
            value=changed
        target=control/path.name
        if target.exists()and target.read_bytes()!=value.encode():raise ValueError('Birth330 frozen control differs')
        target.write_bytes(value.encode())
    compiler.WORK=WORK/'negative/compile'
    bad,unused=compiler.compare(control/'source.c','ov000','2','off',False,thumb=False)
    bad_directory=WORK/'negative/link'
    try:bad_proof=validate(bad[0],qualified_bindings(bad[0]),bad_directory)
    except ValueError as error:
        bad_proof=error.args[0]
        if not isinstance(bad_proof,dict)or bad_proof.get('caller')!=bad[0]['name']:raise
    try:execute(arm,save,assets,overlay,M.recipes()[0],(bad_directory/'caller.bin').read_bytes())
    except ValueError as error:
        rejection=error.args[0]
        if not isinstance(rejection,
            tuple)or rejection[:2]!=('Birth330 independent nonstack RAM differs',
            '0x2247504'):raise
    else:raise ValueError('Birth330 ordinary source control unexpectedly passed')
    rejected=dict(sourceCredit=0,
        compilation=bad,
        genuineLinkComparison=bad_proof,
        expectedRejected=True,
        failure=rejection,
        sourceInputs=[dict(path=str(p.relative_to(ROOT)),
                sha256=sha256(p))for p in sorted(control.glob('*'))])
    raw=encoded(results)
    zipped=gzip.compress(raw,mtime=0)
    artifact=WORK/'raw-traces'/(digest(zipped)+'.json.gz')
    artifact.parent.mkdir(parents=True,exist_ok=True)
    artifact.write_bytes(zipped)
    report=dict(schemaVersion=1,
        romSha256=configuration()['romSha256'],
        processor='arm9',
        program='',
        module='ov000',
        mode='arm',
        address=hex(ENTRY),
        bytes=1644,
        moduleSha256=metadata['sha256'],
        acceptedSourceCredit=0,
        functionMatchCredit=0,
        exact=False,
        compilation=row,
        genuineLinkComparison=proof,
        linkedBytes=len(body),
        linkedSha256=digest(body),
        pairs=len(results),
        actualReturns=2*len(results),
        nativeDependencyActualReturns=sum(r[k]['nativeDependencyActualReturns']for r in results for k in['original',
                'candidate']),
        providedCalls=2*len(results),
        freshMachinePerExecution=True,
        cpu='ARM946',
        instructionBound=200000,
        maximumInstructions=max(r[k]['instructions']for r in results for k in['original',
                'candidate']),
        independentFullNonstackRamComparison=True,
        sourceAndNativeEffectsAgree=True,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)),
            sha256=digest(zipped),
            uncompressedSha256=digest(raw),
            bytes=len(zipped),
            gzipMtime=0),
        results=[dict(recipe=r['recipe'],
                originalSha256=digest(encoded(r['original'])),
                candidateSha256=digest(encoded(r['candidate'])),
                nativeDependencyActualReturns=r['original']['nativeDependencyActualReturns'],
                instructions=[r['original']['instructions'],
                    r['candidate']['instructions']],
                raw33=r['original']['raw33'])for r in results],
        sourceInputs=[dict(path=str(p.relative_to(ROOT)),
                sha256=sha256(p))for p in[BASE/'source.c',
                BASE/'context.h',
                BASE/'part00.inc',
                BASE/'part01.inc',
                ROOT/'probe_ov000_birth329_20261031.py',
                ROOT/'ov000_birth330_models_20261031.py',
                ROOT/'evidence/application/preparation_machine_20261029.py']],
        limits=['This is functional/nonmatching evidence: original1644B versus genuine linked source extent remains different; zero exact/decompiled credit',
            'Parent records are deterministic synthetic modifications of copied captured records, including aliasing; upstream lifecycle/ordinary synthesis eligibility is unproven',
            'Child variant is supplied0, causing actual cap helper7B790 fast path; nonzero variant/trait modifier paths are unqualified here',
            'The six cap results are independently modeled from actual EnmyKindTbl raw u16 fields; six physical caller words are checked without claiming original formal arity',
            '020634CC XP lookup is supplied with an arbitrary declared result; no actual file/XP curve behavior is claimed',
            'Main UID lookups, cap wrappers, table pointer/arithmetic and name copy bodies execute original bytes; listed native dependency returns count only selected strict PC/SP/preserved-register frames',
            'Scratch initialization is supplied random bytes; raw33 preservation is a unit effect, not evidence of a real newborn default or persistent record value',
            'RNG absence applies only to these builder runs;0222900C and its2976C dependency are distinct and can draw RNG',
            'HP20/24 is forced to1 when nonpositive; MP22/26 has no equivalent forced-positive rule in this function',
            'Malformed field widths and bounded negative skill points are tested as raw native behavior, without asserting game-valid records',
            'Invalid/missing parent UIDs and null lookup returns are unsupported; no lookup-failure/error-path proof is claimed','All code/data inputs remain private and no app/frozen source/shared registry is edited'],
        rejectedOrdinarySourceControl=rejected,
        mainSha256=compiler.sha(arm),
        assetHashes={k:compiler.sha(v)for k,
            v in assets.items()},
        pythonVersion=list(sys.version_info[:3]),
        unicornVersion=unicorn.__version__,
        generatorSha256=sha256(__file__),
        reproductionCommand='python prove_ov000_birth330_20261031.py')
    write_json(ROOT/'evidence/application/ov000-birth330-functional-20261031.json',report)
    print(json.dumps({k:report[k]for k in['pairs',
                    'actualReturns',
                    'nativeDependencyActualReturns',
                    'providedCalls',
                    'maximumInstructions',
                    'linkedBytes',
                    'exact']}))

if __name__=='__main__':run()
