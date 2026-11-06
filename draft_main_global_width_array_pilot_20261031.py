import concurrent.futures
import re
from project import ROOT,read_json,write_json,now,sha256
import draft_runtime as drafting
import draft_main_breadth_lane_20261030 as base

WORK=ROOT/'work/main-global-width-array-pilot-20261031'
REPORT=ROOT/'evidence/attempts/main-global-width-array-pilot-20261031.json'


def worker(spec):
    original,address,size,assembly,context,returns,mode=spec
    import draft_main_breadth_lane_20261030 as unit
    unit.WORK=WORK/mode
    if mode=='infer':
        context=re.sub(r'^extern u8 \w+\[\];\n','',context,flags=re.M)
    else:
        context=re.sub(r'^extern u8 (\w+)\[\];',r'extern u32 \1[];',context,flags=re.M)
    row=unit.worker((original,address,size,assembly,context,returns))
    row['globalContextHypothesis']=mode
    return row


def main():
    drafting.OPTIONS=base.options();drafting.WORK=WORK/'input-index';drafting.inputs()
    candidates=[]
    for report in ['main-breadth-round2-20261030','main-breadth-round3-20261031']:
        for row in read_json(ROOT/f'evidence/attempts/{report}.json')['results']:
            alias=row['nativeAlias'];address=int(row['address'],0)
            if not row.get('compilable') or address==0x0203B660 or alias not in drafting.FUNCTION_INPUTS:
                continue
            assembly,context=drafting.FUNCTION_INPUTS[alias]
            if re.search(r'^extern u8 \w+\[\];',context,re.M):
                candidates.append((row,assembly,context))
    candidates.sort(key=lambda item:item[0]['bestSameOffsetBytes']/item[0]['bytes'],reverse=True)
    queue=[]
    for row,assembly,context in candidates[:8]:
        for mode in ['word-array']:
            queue.append((row['nativeAlias'],int(row['address'],0),row['bytes'],assembly,context,drafting.SOURCE_RETURNS,mode))
    result={'sourceCredit':0,'createdUtc':now(),'queueFunctions':len(queue),'contextVariants':len(queue),'results':[],
        'scope':'Empirical comparison of unknown-global context hypotheses; each native width and C access still needs qualification',
        'generatorSha256':sha256(ROOT/'draft_main_global_width_array_pilot_20261031.py')}
    write_json(REPORT,result)
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
        for row in pool.map(worker,queue):
            result['results'].append(row);write_json(REPORT,result)
            print({k:row.get(k) for k in ['address','bytes','globalContextHypothesis','compilable','bestSameOffsetBytes','compilerExact']},flush=True)
    result['finishedUtc']=now();write_json(REPORT,result)


if __name__=='__main__':
    main()
