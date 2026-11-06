import concurrent.futures
import re
from project import ROOT,configuration,read_json,write_json,now,sha256
import draft_runtime as drafting
from draft_main_breadth_lane_20261030 import options
from qualified_call_contexts_20261031 import apply,catalogue
from qualified_main_runtime_contexts_v2_20261031 import catalogue as runtime_catalogue
from project_matched_c_abi_contexts_20261031 import catalogue as projected_catalogue
from native_argument_contexts_20261031 import apply as native_apply,PATH as NATIVE_PATH
from generated_word_type_hypotheses_20261031 import install

WORK=ROOT/'work/main-large-breadth13-20261031'
REPORT=ROOT/'evidence/attempts/main-large-breadth13-20261031.json'
PROJECTED_PATH=ROOT/'evidence/attempts/projected-matched-c-abi-contexts-20261031.json'
PROJECTED=read_json(PROJECTED_PATH)['contracts']


def worker(spec):
    import draft_runtime as unit
    import match_runtime as compiler
    name,address,size,mode,assembly,context,returns=spec
    unit.OPTIONS=options();unit.OPTIONS.thumb=mode=='thumb';unit.OPTIONS.compiler_variants=True
    unit.WORK=WORK/f'{mode}-{address:08x}';compiler.WORK=unit.WORK/'compile'
    relevant=[r for r in PROJECTED if r['alias'] in assembly]
    context,native_contracts=native_apply(context,assembly)
    context,contracts=apply(context,'main',relevant+catalogue()+runtime_catalogue())
    contracts.extend(native_contracts)
    unit.FUNCTION_INPUTS={name:(assembly,context)};unit.FUNCTION_ADDRESSES={name:f'{address:08x}'};unit.SOURCE_RETURNS=returns
    policy=install(unit);result=unit.one(name);result['generatedTypePolicy']=policy;attempts=result.get('attempts',[]);compiled=[x for x in attempts if x.get('compiledBytes')]
    best=max(compiled,key=lambda x:x.get('matchingBytes',0),default={})
    result.update(processor='arm9',program=None,module='main',mode=mode,address=hex(address),bytes=size,sourceCredit=0,accepted=False,generatedHypothesis=True,qualifiedContextContracts=contracts,compilable=bool(compiled),compilerExact=any(x.get('exactAfterDeclaredRelocation') for x in compiled),bestSameOffsetBytes=best.get('matchingBytes',0),reviewRequired=['native boundaries and argument ABI','defined source semantics and memory extents','genuine module linking','independent native contracts','regressions and ROM match'])
    return result


def main():
    from ledger_state import collect_matches
    selected,rejected=collect_matches(configuration()['romSha256']);assert not rejected
    used={(row['mode'],int(row['address'],0)) for row in read_json(ROOT/'evidence/attempts/main-expanded-breadth12-20261031.json')['results']}
    symbols=(ROOT/'config/arm9/symbols.txt').read_text();queue=[]
    for mode in ['arm','thumb']:
        drafting.FUNCTION_INPUTS={};drafting.FUNCTION_ADDRESSES={};drafting.SOURCE_RETURNS={}
        drafting.OPTIONS=options();drafting.OPTIONS.thumb=mode=='thumb';drafting.WORK=WORK/f'input-{mode}';drafting.inputs()
        candidates=[]
        for name,length,location in re.findall(r'^(\S+) kind:function\('+mode+r',size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)',symbols,re.M):
            address,size=int(location,0),int(length,0)
            if not (0x02000800<=address<0x02040000 or address>=0x020D0000) or not 64<=size<=65536:continue
            if (mode,address) in used:continue
            if ('main',mode,address) in selected or name not in drafting.FUNCTION_INPUTS:continue
            assembly,context=drafting.FUNCTION_INPUTS[name]
            candidates.append((name,address,size,mode,assembly,context,dict(drafting.SOURCE_RETURNS)))
        candidates.sort(key=lambda x:(-x[2],x[1]));queue.extend(candidates[:128])
    queue.sort(key=lambda row:(-row[2],row[1]));queue=queue[:128]
    report={'createdUtc':now(),'lane':'integrator-main-large-breadth13','sourceCredit':0,'queueFunctions':len(queue),'queueNativeBytes':sum(x[2] for x in queue),'compilerProcesses':3,'compilerFamiliesPerFunction':3,'results':[],'acceptedSourceChanged':False,'generatorSha256':sha256(ROOT/'draft_main_large_breadth13_20261031.py'),'prototypeCatalogueSha256':sha256(PROJECTED_PATH),'nativeArgumentCatalogueSha256':sha256(NATIVE_PATH)}
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
