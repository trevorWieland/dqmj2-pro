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
from save_link_snapshots import freeze_link
import probe_ov000_birth329_20261031 as B
import ov001_recruit360_fixture_20261031 as F
import ov001_recruit360_models_20261031 as M
SOURCE=ROOT/'src/overlays/ov001_20261031_recruit360/source.c'
WORK=ROOT/'work/ol360-proof'
PINS=ROOT/'evidence/verification/ov001-recruit360-inputs-20261031.json'

def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def execute(arm,save,assets,overlay,recipe,body=None):
    obj=F.Machine(arm,save,assets,overlay,recipe['seed'])
    M.setup(obj,recipe)
    if body is not None:obj.u.mem_write(F.ENTRY,body)
    before=bytes(obj.u.mem_read(0x02000000,0x800000))
    value=obj.controller()
    after=bytes(obj.u.mem_read(0x02000000,0x800000))
    model=M.model(before,after,value,obj.provided,recipe)
    result=dict(recipe=recipe,model=model,actualReturns=1,nativeDependencyActualReturns=len(obj.returned)-1,providedCalls=len(obj.provided),instructions=obj.steps,trace=obj.trace,nativeReturns=obj.returned,writes=obj.writes,observedCodeBytes=sorted(obj.observed),ramSha256=c.sha(after),_ram=after)
    del obj
    return result

def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('Recruit360 pinned runtime differs')
    pins=json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Recruit360 frozen source/fixture/model differs')
    arm,save,assets=B.inputs()
    metadata,overlay,unused=measured_module('ov001')
    c.WORK=WORK/'compile'
    rows,unused=c.compare(SOURCE,'ov001','2','off',True,thumb=False)
    row=rows[0]
    row['sourceDependencies']=[dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)),sha256=sha256(SOURCE.with_name('context.h')))]
    proof=validate(row,qualified_bindings(row),WORK/'link')
    row['genuineLinkComparison']=freeze_link(proof)
    row['exactBytes']=628
    body=(WORK/'link/caller.bin').read_bytes()
    if len(body)!=628:raise ValueError('Recruit360 complete source extent differs')
    summaries=[]
    observed=set()
    for recipe in M.recipes():
        original=execute(arm,save,assets,overlay,recipe)
        candidate=execute(arm,save,assets,overlay,recipe,body)
        if original!=candidate:raise ValueError('Recruit360 complete original/source RAM or trace differs')
        original.pop('_ram')
        raw=encoded(original)
        zipped=gzip.compress(raw,mtime=0)
        artifact=WORK/'raw-traces'/(c.sha(zipped)+'.json.gz')
        artifact.parent.mkdir(parents=True,exist_ok=True)
        artifact.write_bytes(zipped)
        observed.update(original['observedCodeBytes'])
        summaries.append(dict(recipe=recipe,actualReturns=2,nativeDependencyActualReturns=2*original['nativeDependencyActualReturns'],providedCalls=2*original['providedCalls'],instructions=original['instructions'],model=original['model'],rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)),sha256=c.sha(zipped),uncompressedSha256=c.sha(raw),bytes=len(zipped),gzipMtime=0)))
        del original,candidate
        gc.collect()
    controls=[]
    for name,old,new in[('byte-store','M2C_FIELD(native_data_ov001_0223df1c, u32 *, var_r2 * 4)','M2C_FIELD(native_data_ov001_0223df1c, u8 *, var_r2 * 4)'),('required-pointer','native_fn_ov001_0220ad70(native_fn_ov001_02202360(6));','native_fn_ov001_0220ad70(native_fn_ov001_02202360(6) + 1);')]:
        folder=ROOT/'nonmatching/overlay-lane/20261031-recruit360-negative'/name
        folder.mkdir(parents=True,exist_ok=True)
        text=SOURCE.read_text()
        if text.count(old)!=1:raise ValueError('Recruit360 control pattern differs')
        text=text.replace(old,new)
        for path,value in[(folder/'source.c',text),(folder/'context.h',SOURCE.with_name('context.h').read_text())]:
            if path.exists()and path.read_bytes()!=value.encode():raise ValueError('Recruit360 preserve control')
            path.write_bytes(value.encode())
        c.WORK=WORK/'negative'/name/'compile'
        bad_rows,unused=c.compare(folder/'source.c','ov001','2','off',True,thumb=False)
        directory=WORK/'negative'/name/'link'
        try:bad_proof=validate(bad_rows[0],qualified_bindings(bad_rows[0]),directory)
        except ValueError as error:
            bad_proof=error.args[0]
            if not isinstance(bad_proof,dict)or bad_proof.get('caller')!=bad_rows[0]['name']:raise
        try:execute(arm,save,assets,overlay,M.recipes()[2],(directory/'caller.bin').read_bytes())
        except ValueError as error:
            failure=error.args[0]
            prefix=failure[0]if isinstance(failure,tuple)else failure
            if prefix not in['Recruit360 independent complete nonstack RAM/return model differs','Recruit360 independent provider contract differs']:raise
        else:raise ValueError('Recruit360 compiled control unexpectedly passed')
        controls.append(dict(name=name,compilation=bad_rows,genuineLinkComparison=bad_proof,expectedRejected=True,failure=failure,sourceCredit=0))
    oracle=dict(pairs=len(summaries),actualReturns=2*len(summaries),nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns']for r in summaries),providedCalls=sum(r['providedCalls']for r in summaries),freshMachinePerExecution=True,cpu='ARM946',instructionBound=50000,maximumInstructions=max(r['instructions']for r in summaries),independentCompleteNonstackRamComparison=True,completeOriginalSourceRamTraceEquality=True,observedOriginalCallerInstructionBytes=len(observed),nativeCodeBytes=604,literalBytes=24,compiledNegativeControls=controls,results=summaries,limits=['UI/resource/window operations use explicit bounded side-effect-free providers; their actual behavior,scene initialization and hardware effects are not established','Original caller628 and actual62A10/FBE70/4518C/45128/4514C/62AA0/62AD0/62A50/62A88/22360/AAA0 execute; native helper actual returns are counted separately from providers','A synthetic nonnull count16 archive with explicit cumulative offsets exercises both original4518C output words; no original file contents or container meaning are inferred','The16-byte descriptor uses natural alignment of native-written fields0/2/4/5/8/C/D; padding and a complete original type remain unproven','The coordinate caller initializes four bytes and the provider captures those four; actualB0F0 callee extent/effects remain unqualified','Raw phases0/1/3 and default signed32 values,ready template,known recordUID,synthetic groups and already-mapped main/overlay code are supplied prerequisites','AD70/AF68 requiredR0 is proven by original pointer save/dereference; new caller explicitly forwards22360 result,with other historical/formal ABI questions retained','Native global alias is modeled:223DEF8+30 is the fourth32-bit word at223DF1C; phase1 first writes32 then replaces it by archive chunk1 size','No rendering,whole-scene,record creation,progression,persistence,application or UI behavior is claimed from the provided-operation corpus'])
    row['oracle']=oracle
    facts=[]
    for address,size in[(0x0220AD70,400),(0x0220AF68,124),(0x02202360,20),(0x0220AAA0,24)]:
        start=address-0x021D7240
        facts.append(dict(module='ov001',address=hex(address),mode='arm',bytes=size,nativeSpanSha256=c.sha(overlay[start:start+size])))
    main=measured_module('main')[1]
    facts.append(dict(module='main',address='0x0204518C',mode='arm',bytes=56,nativeSpanSha256=c.sha(main[0x4518C:0x4518C+56]),observedOutputWrites=['STR[R0_original+0]','STR[R0_original+4]']))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],module='ov001',moduleSha256=metadata['sha256'],processor='arm9',program='',matches=[row],proposedSourceBytes=628,acceptedSourceCredit=0,preferredSourceChanges=False,nativeInterfaceFacts=facts,mainInputSha256=c.sha(arm),inputPins=pins['files'],generatorSha256=sha256(__file__),reproductionCommand='python match_ov001_recruit360_20261031.py')
    write_json(ROOT/'evidence/matches/ov001-20261031-recruit360.json',report)
    print(json.dumps(dict(exactBytes=628,actualReturns=oracle['actualReturns'],nativeDependencyActualReturns=oracle['nativeDependencyActualReturns'],providedCalls=oracle['providedCalls'],observedCodeBytes=len(observed))))

if __name__=='__main__':run()
