import struct
import ov001_recruit911_machine_20261102 as M

def profiles():
    rows=[]
    for phase in [10,42,60]:
        for counter in range(256):rows.append(dict(ordinal=len(rows),phase=phase,counter=counter,seed=(counter*0x9E3779B9)&0xFFFFFFFF,gate=counter))
    inverse=pow(0x41C64E6D,-1,1<<32)
    for draw in range(256):rows.append(dict(ordinal=len(rows),phase=30,counter=0xED,seed=(((draw<<16)-0x3039)*inverse)&0xFFFFFFFF,gate=draw))
    for phase in [1,255]:rows.append(dict(ordinal=len(rows),phase=phase,counter=0xCC,seed=0xDEADBEEF,gate=phase))
    return rows

def model(vm,result,getter):
    p=vm.p
    state=bytearray(vm.beforeState)
    seed=p['seed']
    writes=[]
    entries=[dict(entry=hex(M.CHILD),consumedWords=[])]
    if p['phase']in[10,42,60]:
        value=(p['counter']+1)&255
        state[0x18]=value
        writes.append([M.STATE+0x18,1,value])
        threshold=30 if p['phase']==42 else 61
        if value>=threshold:
            state[0x1A]={10:20,42:45,60:70}[p['phase']]
            writes.append([M.STATE+0x1A,1,state[0x1A]])
    elif p['phase']==30:
        seed=(seed*0x41C64E6D+0x3039)&0xFFFFFFFF
        random=(seed>>16)%256
        state[0x1A]=40 if random<128 else 50
        writes=[[M.RNG,4,seed],[M.STATE+0x1A,1,state[0x1A]]]
        entries +=[dict(entry='0x203d294',consumedWords=[256]),dict(entry='0x2026350',consumedWords=[seed>>16,256])]
    failures=[]
    for name,actual,expected in [('raw dispatcher result',result['registers'][0],0),('state effects',result['stateHex'],state.hex()),('seed effects',result['rngState'],seed),('ordered writes',result['writes'],writes),('native consumed inputs',[{k:r[k]for k in ['entry','consumedWords']}for r in result['nativeEntries']],entries)]:
        if actual!=expected:failures.append(name)
    if getter['registers'][0]!=(M.SCRATCH if p['gate']else 0):failures.append('raw scratch getter gate')
    if getter['writes']or getter['rngState']!=seed or getter['stateHex']!=state.hex():failures.append('getter purity')
    expectedReturns=['0x2026350','0x203d294',hex(M.CHILD)]if p['phase']==30 else[hex(M.CHILD)]
    if[r['entry']for r in result['nativePhysicalReturns']]!=expectedReturns:failures.append('physical native return chain')
    return failures
