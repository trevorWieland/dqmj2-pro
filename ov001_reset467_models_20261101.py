import struct
from ov001_reset467_machine_20261101 import BASE, STACK, OUTPUT

def profiles():
    rows=[]
    words=[1,0x02620000,0x7FFFFFFF,0x80000000,0xFFFFFFFF]
    for raw in range(256):
        for nonzero in [False,True]:
            rows.append(dict(name=f'raw{raw}-word{nonzero}',raw=raw,word4=words[raw%5] if nonzero else 0,flag1=[0,1,128,255][raw%4]))
    return rows

def model(result):
    p=result['profile']
    expected=bytearray(result['before'])
    normal=p['raw']!=1
    wantedCalls=[0x02068D54,0x02204090,0x02203E60]+[0x021FE54C]*6+[0x021FD354] if normal else []
    if [e['address']for e in result['providedEvents']]!=wantedCalls:raise ValueError(('467 provided boundary order differs',p['name']))
    if normal:
        pairs=[[0,0x7F],[8,0x1D],[8,0x1C],[8,0x18],[8,0x7F],[8,0x1E]]
        if [e['rawCallerWords'][:2]for e in result['providedEvents'][3:9]]!=pairs or result['providedEvents'][-1]['rawCallerWords'][0]!=0:
            raise ValueError('467 explicitly prepared scalar words differ')
        expected[OUTPUT+1-BASE]=0
        struct.pack_into('<I',expected,OUTPUT+4-BASE,0)
        if p['word4']:
            expected[0x020EDD56-BASE]=1
    free=[[2,p['word4']]]if normal and p['word4'] else []
    if result['freePreparedWords']!=free:raise ValueError(('467 measured caller R1 preparation differs',p['name'],result['freePreparedWords'],free))
    cut=STACK-BASE
    if expected[:cut-65536]!=result['after'][:cut-65536]or expected[cut+4096:]!=result['after'][cut+4096:]:raise ValueError(('467 independent complete nonstack effects differ',p['name']))
    if result['returnedR0']!=int(normal):raise ValueError('467 raw gate return differs')
    getters=[r for r in result['nativeReturns']if r['entry']==0x02041814]
    if len(getters)!=1 or getters[0]['returnedR0']!=p['raw'] or 0x020417F8 not in getters[0]['aliases']:raise ValueError('467 actual raw getter return/alias differs')
    return dict(expectedReturn=int(normal),normal=normal,actualEmptyEntryFreeReturns=len(free),providedCalls=len(wantedCalls),freeCallerWords=free)
