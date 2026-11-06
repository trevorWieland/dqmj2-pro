import struct
from main_query480_machine_20261101 import BASE,STACK,OUTPUT

def profiles():
    rows=[]
    for flags in[0,1,2,3,0xFFFFFFFF]:
        for cached in[0,0x02610000,0xFFFFFFFF]:
            for arg3 in[0,1,0x80000000]:
                for out in['null','separate','row','cache']:
                    n=len(rows)
                    rows.append(dict(name=f'flags{flags}-cache{cached}-arg3{arg3}-{out}',handle=0,lookup='valid',objectIndex=0,newIndex=2,mutate=bool(n%2),type=[0,1,65535][n%3],flags=flags,arg2=[0,-1,0x7FFFFFFF][n%3],arg3=arg3,out=out,cached=[cached,0x02611000,[0x02613000,0,0x80000000][n%3]],validation=0,created=[0,0x02612000,0xFFFFFFFF][n%3]))
    for handle in[0,1,3,0xFFFFFFFF,0x80000000]:
        for lookup in['valid','no-table','count0','empty-row']:
            rows.append(dict(rows[0],name=f'lookup-{handle}-{lookup}',handle=handle,lookup=lookup,out='separate'))
    for error in[1,2,4,6,8,0x80000000,0xFFFFFFFF]:
        rows.append(dict(rows[1],name=f'validation-{error}',validation=error,mutate=True,out='separate'))
    for created in[0,0x02612000]:
        for arg3 in[0,1]:
            rows.append(dict(rows[0],name=f'create-{created}-{arg3}',flags=1,created=created,arg3=arg3,out='separate',cached=[0,0,0],mutate=False))
    return rows

def model(result,original):
    p=result['profile']
    expected=bytearray(result['before'])
    events=[]
    def put(a,v):struct.pack_into('<I',expected,a-BASE,v&0xFFFFFFFF)
    valid=p['lookup']=='valid'and p['handle']in[0,1,2]
    value=None
    if not valid:
        wanted=2
    else:
        events.append((0x0203928C,[p['type'],p['flags']&0xFFFFFFFF,p['arg2']&0xFFFFFFFF,p['arg3']&0xFFFFFFFF,0]))
        if p['mutate']:
            for index in range(3):put(0x02601200+index*0x20,p['newIndex'])
        if p['validation']:
            wanted=p['validation']
        else:
            objectIndex=p['newIndex']if p['mutate']else p['objectIndex']
            value=p['cached'][objectIndex]
            if p['flags']&1 and not value:
                constant=struct.unpack_from('<I',original['arm'],0x02039560-BASE)[0]
                events.append((0x02039458,[objectIndex,constant,0x02600000 if p['arg3']else 0,objectIndex,p['arg2']&0xFFFFFFFF]))
                value=p['created']
                if value and p['arg3']:put(0x02603014+objectIndex*16,value)
                wanted=0 if value else 6
            else:wanted=0
            if wanted==0 and result['outputPointer']:put(result['outputPointer'],value)
    if len(result['providedEvents'])!=len(events)or any(e['address']!=a or e['rawCallerWords']!=words for e,(a,words)in zip(result['providedEvents'],events)):raise ValueError(('480 provided input/validation/factory order differs',p['name'],result['providedEvents'],events))
    cut=STACK-BASE
    if expected[:cut-65536]!=result['after'][:cut-65536]or expected[cut+4096:]!=result['after'][cut+4096:]:raise ValueError(('480 complete independent nonstack effects differ',p['name']))
    if result['returnedR0']!=wanted:raise ValueError(('480 independent error/result differs',p['name'],wanted,result['returnedR0']))
    return dict(expectedReturn=wanted,outputValueWritten=value if wanted==0 and result['outputPointer']else None,providedCalls=len(events))
