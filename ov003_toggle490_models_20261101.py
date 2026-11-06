from ov003_toggle490_machine_20261101 import BASE,STACK


def profiles():
    rows=[]
    for flag in list(range(256))+[0x100,0x10000,0x80000000,0x80000100,0xFFFFFF00,0xFFFFFFFF,0x7FFFFFFF,0x12345678]:
        for state in[0,0xFFFFFFFF]:
            for alias in[False,True]:
                n=len(rows)
                rows.append(dict(name=f'word{flag:08x}-state{state:08x}-alias{alias}',flag=flag,state=state,alias=alias,raw=(n*31+17)&255,signal=(n*0x12345+0x80000000)&0xFFFFFFFF))
    return rows


def model(result):
    p=result['profile'];g=result['globals'];expected=bytearray(result['before'])
    def put(a,v,n):expected[a-BASE:a-BASE+n]=(v&((1<<n*8)-1)).to_bytes(n,'little')
    put(g['flagA'],p['flag'],1)
    a=result['preview']+0x7C
    v=int.from_bytes(expected[a-BASE:a-BASE+4],'little')
    put(a,v|2 if p['flag'] else v&~2,4)
    put(g['signal']+0xC84,1,4)
    cut=STACK-BASE
    if expected[:cut-65536]!=result['after'][:cut-65536]or expected[cut+4096:]!=result['after'][cut+4096:]:raise ValueError(('490 complete effect model differs',p['name']))
    if result['providedEvents']or result['nativeReturns']:raise ValueError('490 unexpected dependency')
    if result['returnedR0']!=g['signal']:raise ValueError('490 last physical R0 differs')
    if len(result['helperWords'])!=1 or result['helperWords'][0]['words'][0]!=p['flag']:raise ValueError('490 incoming full word differs')
    return dict(providedCalls=0,lastPhysicalR0=g['signal'],rawFlagWord=p['flag'],storedLowByte=p['flag']&255,fullWordPredicate=True,alias=p['alias'])
