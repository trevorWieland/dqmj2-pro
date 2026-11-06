import concurrent.futures
import re
from project import ROOT,configuration,read_json,write_json,now,sha256
import draft_runtime as drafting
from draft_main_breadth_lane_20261030 import options
from qualified_call_contexts_20261031 import apply,catalogue
from qualified_main_runtime_contexts_v2_20261031 import catalogue as runtime_catalogue
from project_matched_c_abi_contexts_20261031 import catalogue as projected_catalogue

WORK=ROOT/'work/main-projected-callers07-20261031'
REPORT=ROOT/'evidence/attempts/main-projected-callers07-20261031.json'
PROJECTED_PATH=ROOT/'evidence/attempts/projected-matched-c-abi-contexts-20261031.json'
PROJECTED=read_json(PROJECTED_PATH)['contracts']


def worker(spec):
    import draft_runtime as unit
    import match_runtime as compiler
    name,address,size,mode,assembly,context,returns=spec
    unit.OPTIONS=options();unit.OPTIONS.thumb=mode=='thumb';unit.OPTIONS.compiler_variants=True
    unit.WORK=WORK/f'{mode}-{address:08x}';compiler.WORK=unit.WORK/'compile'
    relevant=[r for r in PROJECTED if r['alias'] in assembly]
    context,contracts=apply(context,'main',relevant+catalogue()+runtime_catalogue())
    unit.FUNCTION_INPUTS={name:(assembly,context)};unit.FUNCTION_ADDRESSES={name:f'{address:08x}'};unit.SOURCE_RETURNS=returns
    result=unit.one(name);attempts=result.get('attempts',[]);compiled=[x for x in attempts if x.get('compiledBytes')]
    best=max(compiled,key=lambda x:x.get('matchingBytes',0),default={})
    result.update(processor='arm9',program=None,module='main',mode=mode,address=hex(address),bytes=size,sourceCredit=0,accepted=False,generatedHypothesis=True,qualifiedContextContracts=contracts,compilable=bool(compiled),compilerExact=any(x.get('exactAfterDeclaredRelocation') for x in compiled),bestSameOffsetBytes=best.get('matchingBytes',0),reviewRequired=['native boundaries and argument ABI','defined source semantics and memory extents','genuine module linking','independent native contracts','regressions and ROM match'])
    return result


def main():
    from ledger_state import collect_matches
    selected,rejected=collect_matches(configuration()['romSha256']);assert not rejected
    used=set()
    for path in ['main-breadth-lane-20261030','main-breadth-round2-20261030','main-breadth-round3-20261031']:
        used.update(('arm',int(x['address'],0)) for x in read_json(ROOT/f'evidence/attempts/{path}.json')['results'])
    used.update((x['mode'],int(x['address'],0)) for x in read_json(ROOT/'evidence/attempts/main-mixed-breadth04-20261031.json')['results'])
    symbols=(ROOT/'config/arm9/symbols.txt').read_text();queue=[]
    for mode in ['arm','thumb']:
        drafting.FUNCTION_INPUTS={};drafting.FUNCTION_ADDRESSES={};drafting.SOURCE_RETURNS={}
        drafting.OPTIONS=options();drafting.OPTIONS.thumb=mode=='thumb';drafting.WORK=WORK/f'input-{mode}';drafting.inputs()
        candidates=[]
        for name,length,location in re.findall(r'^(\S+) kind:function\('+mode+r',size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)',symbols,re.M):
            address,size=int(location,0),int(length,0)
            if not 0x02000800<=address<0x02040000 or not 128<=size<=16384:continue
            if ('main',mode,address) in selected or name not in drafting.FUNCTION_INPUTS:continue
            assembly,context=drafting.FUNCTION_INPUTS[name]
            if not any(row['alias'] in assembly for row in PROJECTED):continue
            candidates.append((name,address,size,mode,assembly,context,dict(drafting.SOURCE_RETURNS)))
        candidates.sort(key=lambda x:(-x[2],x[1]));queue.extend(candidates[:40])
    report={'createdUtc':now(),'lane':'integrator-main-projected-callers07','sourceCredit':0,'queueFunctions':len(queue),'queueNativeBytes':sum(x[2] for x in queue),'compilerProcesses':3,'compilerFamiliesPerFunction':3,'results':[],'acceptedSourceChanged':False,'generatorSha256':sha256(ROOT/'draft_main_projected_callers07_20261031.py'),'prototypeCatalogueSha256':sha256(PROJECTED_PATH)}
    write_json(REPORT,report);print({k:report[k] for k in ['queueFunctions','queueNativeBytes','compilerProcesses']},flush=True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        pending=[pool.submit(worker,spec) for spec in queue]
        for future in concurrent.futures.as_completed(pending):
            report['results'].append(future.result())
            for label,predicate in [('drafted',lambda x:'draftSource' in x),('compilable',lambda x:x['compilable']),('compilerExact',lambda x:x['compilerExact'])]:
                report[label+'Functions']=sum(predicate(x) for x in report['results']);report[label+'NativeBytes']=sum(x['bytes'] for x in report['results'] if predicate(x))
            write_json(REPORT,report);print({k:report[k] for k in ['draftedFunctions','compilableFunctions','compilerExactFunctions']},flush=True)
    report['finishedUtc']=now();write_json(REPORT,report)


if __name__=='__main__':
    main()
