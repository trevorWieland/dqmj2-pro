from ov003_reset488_machine_20261101 import BASE,STACK


def profiles():
    rows=[]
    for n in range(64):
        rows.append(dict(name=f'state-{n}',group=bool(n&1),groupAlias=bool(n&2),previewAlias=bool(n&4),first=[(0x80000003+n*0x10203+i*0xABCD)&0xFFFFFFFF for i in range(3)],second=[(0x7FFFFFFF-n*0x34567-i*0xCDEF)&0xFFFFFFFF for i in range(3)],preview=(0x1234567+n*17)&0xFFFFFFFF,raw=[(n*31+i*17)&255 for i in range(8)],signal=(0x80000000+n*0x10203)&0xFFFFFFFF))
    return rows


def model(result):
    p=result['profile'];g=result['globals'];expected=bytearray(result['before'])
    def put(a,v,n):expected[a-BASE:a-BASE+n]=(v&((1<<n*8)-1)).to_bytes(n,'little')
    def clear(a):put(a,int.from_bytes(expected[a-BASE:a-BASE+4],'little')&~2,4)
    put(g['flagA']+1,0,1)
    if p['group']:
        for index in range(3):clear(result['groupA']+index*0x90+0x7C)
    put(g['flagA'],0,1)
    clear(result['preview']+0x7C)
    put(result['preview']+0x6C,160,4);put(result['preview']+0x70,8,4)
    for index in range(2):
        put(g['flagB']+index,0,1);clear(0x0260407C+index*0x90)
    put(g['signal']+0xC84,1,4)
    cut=STACK-BASE
    if expected[:cut-65536]!=result['after'][:cut-65536]or expected[cut+4096:]!=result['after'][cut+4096:]:raise ValueError(('488 complete effect model differs',p['name']))
    wanted=[(0x021DFD18,[0]),(0x021DFDA8,[0]),(0x021DFDFC,[160,8]),(0x021DFD68,[0,0]),(0x021DFD68,[1,0])]
    if len(result['helperWords'])!=len(wanted)or any(e['address']!=a or e['words'][:len(w)]!=w for e,(a,w)in zip(result['helperWords'],wanted)):raise ValueError('488 caller/helper words differ')
    if result['providedEvents']:raise ValueError('488 provider unexpectedly used')
    if result['returnedR0']!=0x02000000:raise ValueError('488 physical R0 differs')
    return dict(providedCalls=0,lastPhysicalR0=0x02000000,observedCallerHelperCalls=len(wanted),completeNonstackEffects=True)
