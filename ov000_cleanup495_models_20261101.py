from ov000_cleanup495_machine_20261101 import BASE,STACK


def profiles():
    rows=[]
    for first in[False,True]:
        for second in[False,True]:
            for alias in[False,True]:
                for mutate in[False,True]:
                    for raw in[0,255]:
                        n=len(rows)
                        rows.append(dict(name=f'state{n}',first=first,second=second,alias=alias,mutate=mutate,raw=raw,words=[[0,0xFFFFFFFF,0x80000000],[0x02680000,0x12345678,1]][n%2]))
    return rows


def model(result):
    p=result['profile'];expected=bytearray(result['before']);wanted=[];free=[];flags=4
    def put(a,v,n):expected[a-BASE:a-BASE+n]=(v&((1<<n*8)-1)).to_bytes(n,'little')
    def word(a):return int.from_bytes(expected[a-BASE:a-BASE+4],'little')
    for slot,channel,mask in[(0x02238518,0,1),(0x02238514,1,2)]:
        resource=word(slot)
        if not resource:continue
        for offset in[0x40,0x44,0x48]:free.append([1,word(resource+offset)])
        for offset in[0x40,0x44,0x48,0x60]:put(resource+offset,0,4)
        put(0x020EDD56,1,1)
        wanted.append(dict(address=0x02084F9C,words=[channel,resource],resourceWords=[0,0,0,0]))
        if channel==0 and p['mutate']:put(0x02238514,0x02603000,4)
        put(0x0223852B,p['raw']^255,1)
        flags|=mask
    put(result['finalByte'],0,1)
    if result['helperWords']!=free:raise ValueError('495 complete incoming free words differ')
    if result['providedEvents']!=wanted:raise ValueError('495 resource-channel/effect-boundary order differs')
    cut=STACK-BASE
    if expected[:cut-65536]!=result['after'][:cut-65536]or expected[cut+4096:]!=result['after'][cut+4096:]:raise ValueError('495 complete nonstack effect differs')
    if result['returnedR0']!=flags:raise ValueError('495 address-predicate/accumulated return differs')
    return dict(result=flags,providedCalls=len(wanted),nativeEmptyArenaFrees=len(free),rawByteIsNotReadByFinalPredicate=True)
