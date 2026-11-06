from ov005_controller500_machine_20261101 import BASE,STACK


def profiles():
    rows=[]
    for state in list(range(32))+[127,255]:
        for n in range(8):
            rows.append(dict(name=f'state{state}-inputs{n}',state=state,keys=[0,0x100,0x200,4,8,0xFF7,0x101,0x208][n],service=[0,1,4,0xFFFFFFFF][n%4],rawMode=[0,1,2,255][n%4],busy=n%2,progress=[0,47,48,0xFFFFFFFF][n%4],kind=4 if n&4 else 0,reset=n%2,enabled=(n>>1)&1,scroll=[0,32,256,288][n%4],step=32 if n%2 else -32,phase=[0,1,127,255][n%4],delta=[0,1,-1,32][n%4],signedFlag=[0,1,255,0][n%4],position=[0,128,256,512][n%4]))
    return rows


def model(result):
    p=result['profile'];state=p['state'];expected=bytearray(result['before']);io=bytearray(result['ioBefore'])
    def put(a,v,size):expected[a-BASE:a-BASE+size]=(v&((1<<(8*size))-1)).to_bytes(size,'little')
    if p['reset']==1:put(0x021E9822,0,2)
    footer=True;value=9
    if state in [19,29,30,31,127,255]:pass
    elif state==28:footer=False;value=2
    elif state==27:
        if p['rawMode']!=1 and p['busy']==0:footer=False;value=0x12345678
    elif state==26:
        if p['rawMode']!=1:put(0x021E981C,0,1)
    elif state==25:
        if p['delta']:
            scroll=p['phase'];packed=(scroll&511)|((scroll<<16)&0x01FF0000);io[0x10:0x14]=packed.to_bytes(4,'little');put(0x021E987C,scroll+p['delta'],1)
    elif state==24:put(0x021E981C,25,1)
    elif state==23:
        if p['rawMode']!=1:put(0x021E981C,24,1)
    elif state==22:
        if p['service']==1:put(0x021E981C,0,1)
    elif state==21:put(0x021E981C,22,1)
    elif state==12:
        if p['rawMode']!=1:put(0x021E981C,22,1)
    elif state==2:
        if p['busy']==0:
            footer=False;value=15 if 48<=p['progress']<0x80000000 else 1
            if p['kind']==4:value=2
            put(0x021E981C,28,1)
    else:return dict(independentlyModeled=False)
    if footer:put(0x020FF028,1,4);put(0x021E9822,p['keys'],2)
    cut=STACK-BASE
    if expected[:cut-65536]!=result['after'][:cut-65536]or expected[cut+4096:]!=result['after'][cut+4096:]:raise ValueError(('500 independently modeled nonstack effect differs',p['name']))
    if bytes(io)!=result['ioAfter']:raise ValueError(('500 mapped MMIO storage model differs',p['name']))
    if result['returnedR0']!=value:raise ValueError(('500 independently modeled result differs',p['name'],value,result['returnedR0']))
    return dict(independentlyModeled=True,result=value,footer=footer,physicalMmioEffectsNotClaimed=True)
