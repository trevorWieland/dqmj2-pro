import struct
import ov001_selector917_machine_20261102 as M


def profiles():
    rows=[]
    inverse=pow(0x41C64E6D,-1,1<<32)
    def add(threshold,draw,busy):
        rows.append(dict(ordinal=len(rows),threshold=threshold,firstDraw=draw,busy=busy,phase=30,counter=0xED,gate=len(rows)&255,seed=(((draw<<16)-0x3039)*inverse)&0xFFFFFFFF,selector=12,subphase=110))
    for threshold in [-32768,-1,0,1,500,999,1000,32767]:
        for draw in [0,1,127,128,499,500,998,999]:add(threshold,draw,0)
    for draw in range(1000):add(500,draw,0)
    for busy in [1,0xFFFFFFFF]:
        for threshold in [-32768,-1,0,1,500,999,1000,32767]:add(threshold,500,busy)
    return rows


def logical_providers(result):
    return [{k:v for k,v in row.items()if k!='rawCallerWords'}for row in result['provided']]


def model(vm,result):
    p=vm.p
    state=bytearray(vm.beforeState)
    seed=p['seed']
    entries=[dict(entry='0x205fd60',consumedWords=[])]
    returns=['0x205fd60']
    writes=[]
    provided=[]
    if p['busy']==0:
        seed=(seed*0x41C64E6D+0x3039)&0xFFFFFFFF
        draw=(seed>>16)%1000
        if draw!=p['firstDraw']:raise ValueError('917 inverse seed recipe differs')
        selector=13 if draw<p['threshold']else 14
        state[0xA]=selector
        state[0xF]=0
        writes=[[M.RNG,4,seed],[M.STATE+0xA,1,selector],[M.STATE+0xF,1,0]]
        entries +=[dict(entry='0x203d294',consumedWords=[1000]),dict(entry='0x2026350',consumedWords=[seed>>16,1000])]
        returns +=['0x2026350','0x203d294']
        provided=[dict(target=hex(M.NOTICE),consumedWords=[0,1],returnWord=0xC0DEC0DE)]
    failures=[]
    for name,actual,expected in [('selector state',result['stateHex'],state.hex()),('seed',result['rngState'],seed),('ordered writes',result['writes'],writes),('consumed native entry words',[{k:r[k]for k in ['entry','consumedWords']}for r in result['nativeEntries']],entries),('notification service contract',logical_providers(result),provided),('actual return chain',[r['entry']for r in result['nativePhysicalReturns']],returns),('raw selector result',result['registers'][0],0)]:
        if actual!=expected:failures.append(name)
    return failures
