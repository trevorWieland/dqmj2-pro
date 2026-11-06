import struct
from ov000_tables469_machine_20261101 import BASE,STACK

def profiles():
    rows=[]
    masks=[0,1,1<<21,(1<<22)-1,0x155555,0x2AAAAA]
    words=[0,0x0263F000,0xFFFFFFFF,0x80000000,0x12345678]
    for index in range(48):
        mask=masks[index%len(masks)]
        rows.append(dict(name=f'mask{mask:06x}-case{index}',slot=[0,1,128,255][index%4],contextPointer=0x0264F000 if index&1 else 0,first=[0x02620000+slot*0x100 if mask>>slot&1 else 0 for slot in range(22)],objectSlots=[(index*11+slot*17)&255 for slot in range(22)],second=words[index%5:]+words[:index%5]))
    return rows

def model(result):
    p=result['profile']
    wanted=[]
    free=[]
    expected=bytearray(result['before'])
    for index,pointer in enumerate(p['first']):
        if pointer:
            wanted.append((0x0204861C,[1,p['objectSlots'][index]]))
            free.append([2,pointer])
            struct.pack_into('<I',expected,0x02246348+index*4-BASE,0)
    if p['contextPointer']:wanted.append((0x020485B4,[p['contextPointer']]))
    wanted.append((0x020484DC,[1,p['slot']]))
    for index,pointer in enumerate(p['second']):
        wanted.append((0x0205F920,[pointer,1,2]))
        free.append([2,pointer])
        struct.pack_into('<I',expected,0x0224632C+index*4-BASE,0)
    events=result['providedEvents']
    if len(events)!=len(wanted) or any(e['address']!=a or e['rawCallerWords'][:len(args)]!=args for e,(a,args)in zip(events,wanted)):
        raise ValueError(('469 provided boundary/explicit input words differ',p['name']))
    if result['freePreparedWords']!=free:raise ValueError(('469 native free caller words differ',p['name']))
    expected[0x020EDD56-BASE]=1
    cut=STACK-BASE
    if expected[:cut-65536]!=result['after'][:cut-65536]or expected[cut+4096:]!=result['after'][cut+4096:]:raise ValueError(('469 complete nonstack model differs',p['name']))
    if result['returnedR0']!=0:raise ValueError('469 last physical empty-entry result differs')
    returns=[r for r in result['nativeReturns']if r['entry']==0x0202A498]
    if len(returns)!=len(free)or any(r['returnedR0']for r in returns):raise ValueError('469 actual native empty-entry return differs')
    return dict(providedCalls=len(wanted),actualEmptyEntryFreeReturns=len(free),firstCleared=sum(bool(v)for v in p['first']),secondCleared=5,lastPhysicalR0=0)
