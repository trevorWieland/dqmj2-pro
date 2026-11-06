import itertools
import struct
import ov000_flag750_machine_20261101 as M
def profiles():
    cases=[];poison=[0,1,0x80000000,0xFFFFFFFF]
    for seed,(resource,pointer,flag,word)in enumerate(itertools.product([0,1,127,0x80000000,0xFFFFFFFF],[0,M.OBJECT],[0,1,128,255],[0,1,2,0xFFFFFFFF])):
        cases.append(dict(name=f'flag-{seed}',seed=seed,resourceWord=resource,pointer=pointer,flag=flag,word=word,poison=[poison[(seed+n)%4]for n in range(4)]))
    return cases
def model(result):
    p=result['profile'];expected=bytearray(result['before']);active=p['resourceWord']!=127 and p['pointer']!=0
    writes=[]
    if active:
        value=p['word']|2 if p['flag']!=0 else p['word']&0xFFFFFFFD;expected[M.OBJECT+0x7C-M.BASE:M.OBJECT+0x80-M.BASE]=struct.pack('<I',value);writes=[[M.OBJECT+0x7C,4,value]];raw=M.OBJECT
    else:raw=127 if p['resourceWord']==127 else 0
    lo,hi=M.STACK-256-M.BASE,M.STACK+32-M.BASE
    if expected[:lo]!=result['after'][:lo]or expected[hi:]!=result['after'][hi:]:raise ValueError(('750 complete nonstack model differs',p['name']))
    if[row[1:]for row in result['nonstackWrites']]!=writes:raise ValueError('750 exact ordered flag-word writes differ')
    if result['coreRegistersAndCpsr'][0]!=raw:raise ValueError(('750 exact raw-word return differs',p['name'],result['coreRegistersAndCpsr'][0],raw))
    calls=[dict(entry=c['entry'],preparedWords=c['preparedWords'])for c in result['nativeCalls']]
    if calls!=([dict(entry=0x0205F98C,preparedWords=[M.OBJECT,0])]if active else[]):raise ValueError('750 actual signed-word facade leaf call differs')
    if len(result['watchedNativeReturns'])!=int(active):raise ValueError('750 actual native leaf-return count differs')
    return dict(active=active,rawR0=raw,completeNonstackModel=True,requiredIncomingArgumentWords=0,poisonedR0ThroughR3=p['poison'],actualNativeDependencyReturns=int(active))
