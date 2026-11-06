import gc
import gzip
import json
import re
import struct
import sys
from pathlib import Path
import match_runtime as compiler
import unicorn
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
import ov000_commit336_fixture_20261031 as F
import prove_ov000_selection333_20261031 as S
import probe_ov000_birth329_20261031 as B
SOURCE=ROOT/'nonmatching/overlay-lane/20261031-commit336/source.c'
WORK=ROOT/'work/ol336-proof'

def encoded(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def uid(row):return int.from_bytes(row[20:24],'little')
def records(raw):return[raw[i*132:(i+1)*132]for i in range(100)]
def keyed(raw):return{uid(row):row for row in records(raw)if uid(row)}

def recipes():
    return[dict(role=role,
            raw33=raw,
            seed=seed,
            itemA=a,
            itemB=b,
            alias=alias)for role,
        raw,
        seed,
        a,
        b,
        alias in[('stored',
                0,
                0,
                0,
                0,
                False),
            ('active_split',
                1,
                1,
                181,
                0,
                False),
            ('active_adjacent',
                127,
                0xFFFFFFFF,
                0,
                182,
                False),
            ('reserve_split',
                255,
                0x12345678,
                181,
                182,
                False),
            ('reserve_adjacent',
                57,
                1,
                182,
                181,
                False),
            ('cross',
                13,
                0,
                0,
                0,
                False),
            ('alias',
                99,
                1,
                0,
                0,
                True)]]

def groups(role,a,b,other):
    if role=='active_split':return[a,other,b,0,0,0]
    if role=='active_adjacent':return[a,b,other,0,0,0]
    if role=='reserve_split':return[0,0,0,a,other,b]
    if role=='reserve_adjacent':return[0,0,0,a,b,other]
    if role=='cross':return[a,0,0,b,0,0]
    if role=='alias':return[a,other,0,0,0,0]
    return[0]*6

def compact(values,parents):
    result=list(values)
    for base in[0,3]:
        for index in range(3):
            if result[base+index]in parents:
                result[base+index:base+3]=result[base+index+1:base+3]+[0]
    return result

def execute(arm,save,assets,overlay,recipe,body=None):
    obj=F.Machine(arm,save,assets,overlay,recipe['seed'])
    selected=[row for row in records(save[0x1E8:0x1E8+13200])if uid(row)][:3]
    a,b,other=[uid(r)for r in selected]
    if recipe['alias']:b=a
    for ident,item in[(a,recipe['itemA']),(b,recipe['itemB'])]:
        row=next(i for i,r in enumerate(records(bytes(obj.u.mem_read(B.RECORDS,13200))))if uid(r)==ident)
        obj.u.mem_write(B.RECORDS+row*132+0x31,bytes([item]))
    supplied_groups=groups(recipe['role'],a,b,other)
    obj.u.mem_write(0x021BD540,struct.pack('<6I',*supplied_groups))
    obj.u.mem_write(0x022474FB,bytes([recipe['raw33']]))
    obj.word(0x020F6044,recipe['seed'])
    child_species=int.from_bytes(selected[0][24:26],'little')
    B.BirthMachine.birth(obj,[a,b,child_species,0,0])
    prep_providers=sum(r['provider']for r in obj.trace)
    if prep_providers!=1:raise ValueError('Commit336 preparation XP provider count differs')
    if body is not None:obj.u.mem_write(F.ENTRY,body)
    before=bytes(obj.u.mem_read(0x02000000,0x800000))
    before_rows=bytes(obj.u.mem_read(B.RECORDS,13200))
    parents=[keyed(before_rows)[i]for i in[a,b]]
    scratch=bytes(obj.u.mem_read(0x022474C8,132))
    counter=obj.read_word(0x021BD520)
    table=assets['ItemTbl.bin'][8:]
    flags=assets['EnmyKindTbl.bin'][8+100*child_species+4:8+100*child_species+6]
    selector,final_rng,draws=S.model(table[88*parents[0][0x31]+42],
        table[88*parents[1][0x31]+42],
        recipe['seed'],
        bool(int.from_bytes(flags,
                'little')&0x8000))
    expected_uid=(counter+1)&0xFFFFFFFF
    expected_child=bytearray(132)
    expected_child[20:24]=struct.pack('<I',expected_uid)
    expected_child[24:27]=scratch[24:27]
    expected_child[0x20:0x40]=scratch[0x20:0x40]
    expected_child[0x40:0x7A]=scratch[0x40:0x7A]
    expected_child[0x1B]=selector
    expected_child[0x1E]=scratch[0x1E]
    expected_child[0x1C]=scratch[0x1C]
    expected_child[0x1D]=scratch[0x1D]
    expected_live=keyed(before_rows)
    for ident in{a,b}:expected_live.pop(ident)
    expected_live[expected_uid]=bytes(expected_child)
    result=obj.commit([a,b])
    after=bytes(obj.u.mem_read(0x02000000,0x800000))
    after_rows=bytes(obj.u.mem_read(B.RECORDS,13200))
    after_groups=list(struct.unpack('<6I',obj.u.mem_read(0x021BD540,24)))
    if result!=expected_uid or keyed(after_rows)!=expected_live or after_groups!=compact(supplied_groups,
        {a,
            b})or obj.read_word(0x021BD520)!=expected_uid or obj.read_word(0x020F6044)!=final_rng:
        raise ValueError(('Commit336 independent live-record/group/counter/RNG effects differ',recipe))
    live_ids=[uid(r)for r in records(after_rows)if uid(r)]
    if live_ids!=sorted(live_ids):raise ValueError('Commit336 native nonzero UID order differs')
    if keyed(after_rows)[result][0x33]!=recipe['raw33']:raise ValueError('Commit336 raw33 propagation differs')
    if any(r['provider']for r in obj.trace):raise ValueError('Commit336 unsupported commit-stage function provider')
    observed=[r['arguments'][0]for r in obj.trace if r['entry']=='0x203d294']
    returned=[r['result']for r in obj.returned if r['entry']=='0x203d294']
    if observed!=[r['limit']for r in draws]or returned!=[r['result']for r in draws]:raise ValueError('Commit336 independent RNG call sequence differs')
    result=dict(recipe=recipe,
        actualReturns=1,
        returnedUid=result,
        parentUids=[a,
            b],
        beforeLiveRecords=len(keyed(before_rows)),
        afterLiveRecords=len(expected_live),
        raw33=recipe['raw33'],
        groupsBefore=supplied_groups,
        groupsAfter=after_groups,
        selector=selector,
        rngDraws=draws,
        finalRngState=final_rng,
        instructions=obj.steps,
        nativeDependencyActualReturns=len(obj.returned)-1,
        rngActualReturns=len(draws),
        providedCommitCalls=0,
        providedPreparationCalls=prep_providers,
        sourceStage='original builder with explicit XP provider, then original or exact-source244-byte call chain',
        trace=obj.trace,
        nativeReturns=obj.returned,
        writes=obj.writes,
        childSha256=compiler.sha(bytes(expected_child)),
        liveRecordsSha256=compiler.sha(encoded({str(k):v.hex()for k,
                    v in expected_live.items()})),
        _ram=after,
        _before=before)
    del obj
    return result

def run():
    if sys.version_info[:3]!=(3,
        13,
        5)or unicorn.__version__!='2.1.4':raise ValueError('Commit336 pinned runtime differs')
    if sha256(ROOT/'src/runtime/ov000-drafts01/native_ov000_0222900c.c')!='b780006f5fc18fc7508cf79f97c1e4f905a7bcca473d063878f48d20f38bdc8c':raise ValueError('Commit336 frozen accepted source differs')
    arm,save,assets=B.inputs()
    metadata,overlay,unused=measured_module('ov000')
    compiler.WORK=WORK/'compile'
    rows,unused=compiler.compare(SOURCE,'ov000','2','off',True,thumb=False)
    proof=validate(rows[0],qualified_bindings(rows[0]),WORK/'link')
    body=(WORK/'link/caller.bin').read_bytes()
    if len(body)!=244:raise ValueError('Commit336 complete source extent differs')
    summaries=[]
    for recipe in recipes():
        original=execute(arm,save,assets,overlay,recipe)
        candidate=execute(arm,save,assets,overlay,recipe,body)
        if original!=candidate:raise ValueError('Commit336 complete original/source RAM or trace differs')
        original.pop('_ram');original.pop('_before')
        raw=encoded(original)
        zipped=gzip.compress(raw,mtime=0)
        artifact=WORK/'raw-traces'/(compiler.sha(zipped)+'.json.gz')
        artifact.parent.mkdir(parents=True,exist_ok=True)
        artifact.write_bytes(zipped)
        summaries.append(dict(recipe=recipe,
                actualReturns=2,
                nativeDependencyActualReturns=2*original['nativeDependencyActualReturns'],
                rngActualReturns=2*original['rngActualReturns'],
                providedCommitCalls=0,
                providedPreparationCalls=2,
                returnedUid=original['returnedUid'],
                raw33=original['raw33'],
                groupsBefore=original['groupsBefore'],
                groupsAfter=original['groupsAfter'],
                beforeLiveRecords=original['beforeLiveRecords'],
                afterLiveRecords=original['afterLiveRecords'],
                selector=original['selector'],
                rngDraws=original['rngDraws'],
                finalRngState=original['finalRngState'],
                instructions=original['instructions'],
                rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)),
                    sha256=compiler.sha(zipped),
                    uncompressedSha256=compiler.sha(raw),
                    bytes=len(zipped),
                    gzipMtime=0)))
        del original,candidate
        gc.collect()
        print(json.dumps(dict(case=recipe['role'],
                    returns=2,
                    raw33=recipe['raw33'],
                    instructions=summaries[-1]['instructions'])),
            flush=True)
    control=ROOT/'nonmatching/overlay-lane/20261031-commit336-negative/source.c'
    control.parent.mkdir(parents=True,exist_ok=True)
    value=SOURCE.read_text().replace('temp_r4_2 = native_fn_02062a10(arg0);',
        'temp_r4_2 = native_fn_02062a10(arg1);')
    if value==SOURCE.read_text():raise ValueError('Commit336 ordinary UID source control missing')
    if control.exists()and control.read_bytes()!=value.encode():raise ValueError('Commit336 preserve frozen control')
    control.write_bytes(value.encode())
    compiler.WORK=WORK/'negative/compile'
    bad,unused=compiler.compare(control,'ov000','2','off',True,thumb=False)
    bad_directory=WORK/'negative/link'
    try:bad_proof=validate(bad[0],qualified_bindings(bad[0]),bad_directory)
    except ValueError as error:
        bad_proof=error.args[0]
        if not isinstance(bad_proof,dict)or bad_proof.get('caller')!=bad[0]['name']:raise
    try:execute(arm,save,assets,overlay,recipes()[1],(bad_directory/'caller.bin').read_bytes())
    except ValueError as error:
        rejection=error.args[0]
        if not isinstance(rejection,
            tuple)or rejection[0]!='Commit336 independent live-record/group/counter/RNG effects differ':raise
    else:raise ValueError('Commit336 ordinary UID source control unexpectedly passed')
    rejected=dict(sourceCredit=0,
        compilation=bad,
        genuineLinkComparison=bad_proof,
        expectedRejected=True,
        failure=rejection,
        source=str(control.relative_to(ROOT)),
        sha256=sha256(control))
    bodies=[]
    for address in sorted(F.WATCH):
        module='main'if address<0x021D7240 else'ov000'
        meta,image,symbols=measured_module(module)
        found=re.search(r'kind:function\(arm,size=(0x[0-9a-f]+)\) addr:0x'+f'{address:08x}'+r'$',symbols,re.M)
        if found is None:raise ValueError(('Commit336 selected native body boundary differs',hex(address)))
        size=int(found[1],0)
        base=int(meta['base'],0)
        bodies.append(dict(processor='arm9',
                program='',
                module=module,
                mode='arm',
                address=hex(address),
                bytes=size,
                sha256=compiler.sha(image[address-base:address-base+size]),
                sourceCredit=0))
    report=dict(schemaVersion=1,
        romSha256=configuration()['romSha256'],
        processor='arm9',
        program='',
        module='ov000',
        mode='arm',
        address=hex(F.ENTRY),
        bytes=244,
        moduleSha256=metadata['sha256'],
        acceptedSourceCredit=0,
        duplicateFunctionCredit=0,
        alternativeSourceOnly=True,
        acceptedSourceUnchanged=True,
        compilation=rows,
        realLinkProof=proof,
        pairs=len(summaries),
        actualReturns=sum(r['actualReturns']for r in summaries),
        nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns']for r in summaries),
        rngActualReturns=sum(r['rngActualReturns']for r in summaries),
        providedCommitCalls=0,
        providedPreparationCalls=sum(r['providedPreparationCalls']for r in summaries),
        instructionBound=2000000,
        maximumInstructions=max(r['instructions']for r in summaries),
        freshMachinePerExecution=True,
        completeOriginalSourceRamAndTraceEquality=True,
        independentModelScope=['All live132-byte records by UID',
            'Raw active/reserve group words with actual forward iteration and compact-left removal',
            'UID counter and returned newUID',
            'Full32-byte scratch20..3F copy including raw33,58-byte ancestry copy and individual field writers',
            'Actual native RNG17/conditional1024 sequence and final state'],
        results=summaries,
        inputFiles=[dict(path=p,
                sha256=sha256(ROOT/p))for p in['ov000_commit336_fixture_20261031.py',
                'probe_ov000_birth329_20261031.py',
                'prove_ov000_selection333_20261031.py',
                'evidence/application/preparation_machine_20261029.py',
                'src/runtime/ov000-drafts01/native_ov000_0222900c.c']],
        limits=['New source only makes the already measured first UID argument explicit and declares its32-bit callee input; accepted source remains unchanged and zero duplicate source credit is requested',
            'The full commit-stage original code executes with0 function providers; earlier original scratch preparation uses one declared arbitrary XP provider per execution',
            'Groups/item bytes/scratch33/seeds are synthetic supplied arrangements; ordinary caller initialization, eligibility, normal record33 value, item payment and persistence remain unproven',
            'Independent models cover the listed live-record/group/counter/copy/RNG state; unused-row permutation and other flag bitmap effects are compared completely original/source but are not independently semantically modeled',
            'Forward iteration over compacting groups can leave a raw matching UID in a supplied adjacent arrangement; do not label this a game bug or application rule without lifecycle/caller evidence',
            'Missing/null parent UID, exhausted allocation, counter wrap and unsupported malformed records remain untested error paths',
            'No app, frozen source, registry, ledger or shared build file is edited'],
        selectedNativeBodies=bodies,
        rejectedOrdinarySourceControl=rejected,
        mainSha256=compiler.sha(arm),
        assetHashes={k:compiler.sha(v)for k,
            v in assets.items()},
        generatorSha256=sha256(__file__),
        reproductionCommand='python prove_ov000_commit336_20261031.py')
    write_json(ROOT/'evidence/application/ov000-commit336-native-20261031.json',report)
    print(json.dumps({k:report[k]for k in['pairs',
                    'actualReturns',
                    'nativeDependencyActualReturns',
                    'rngActualReturns',
                    'providedCommitCalls',
                    'providedPreparationCalls',
                    'maximumInstructions']}))

if __name__=='__main__':run()
