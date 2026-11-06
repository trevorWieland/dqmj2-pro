import random
from ov001_query466_machine_20261101 import BASE, STACK

def valid(row):
    return row['ready'] != 0 and row['flag'] == 0 and row['ac'] == 0

def profiles():
    rows = []
    for index in range(256):
        rng = random.Random(466000 + index)
        p = dict(name=f'mixed-{index}', gate=[0,1,0x80000000,0xFFFFFFFF][index % 4], countRaw=[0,1,3,6,128,255][index % 6], blocked=[(rng.choice([0,1,255]),rng.randrange(3)) for unused in range(6)], actions=[[rng.choice([0,0x76,0x77,0xFFFF]) for unused in range(3)] for side in range(2)])
        for group in ['outer','inner']:
            p[group] = [dict(ready=rng.choice([0,1,128,255]), flag=rng.choice([0,1,255]), ac=rng.choice([0,1,255]), side=rng.choice([0,1,255]), slot=rng.randrange(3), kind97=rng.choice([0,1,3,4,255])) for unused in range(3)]
        rows.append(p)
    for outer in range(3):
        for inner in range(3):
            for blocked in [False,True]:
                p = dict(name=f'ordered-{outer}-{inner}-blocked{blocked}', gate=1, countRaw=int(blocked), blocked=[(1,outer)]*6, actions=[[0x77]*3,[0x77]*3])
                for group, chosen in [('outer',outer),('inner',inner)]:
                    p[group]=[dict(ready=int(slot==chosen),flag=0,ac=0,side=1,slot=slot,kind97=3) for slot in range(3)]
                rows.append(p)
    return rows

def model(result):
    p=result['profile']
    count=(p['countRaw']+128)%256-128
    wanted=0
    if p['gate']:
        for row in p['outer']:
            if not valid(row):continue
            if (row['side'],row['slot']) in [(a if a<128 else a-256,b if b<128 else b-256)for a,b in p['blocked'][:max(count,0)]]:continue
            if p['actions'][int(row['side']!=0)][row['slot']]!=0x77:continue
            if any(valid(target)and target['kind97']<=3 for target in p['inner']):
                wanted=1
                break
    cut=STACK-BASE
    if result['before'][:cut-65536]!=result['after'][:cut-65536]or result['before'][cut+4096:]!=result['after'][cut+4096:]:
        raise ValueError(('466 unexpected nonstack write',p['name']))
    if result['returnedR0']!=wanted:
        raise ValueError(('466 independent predicate differs',p['name'],wanted,result['returnedR0']))
    return dict(expectedReturn=wanted,matchedOriginalPredicate=True)
