import ov001_rows598_machine_20261101 as M


def profiles():return[dict(name=f'caller-{count}-{modifier}',count=count,modifier=modifier)for count in range(4)for modifier in[0,1,39,40,139,140,65535]]


def model(r):
    p=r['profile'];expected=bytearray(r['before']);expected[M.ROWS-M.BASE:M.ROWS-M.BASE+396]=bytes(396);expected[M.OUTPUT-M.BASE:M.OUTPUT-M.BASE+192]=bytes(192);calls=[]
    for index in range(p['count']):
        for step,address in enumerate(M.STEPS):calls.append(dict(entry=address,preparedWords=[index]if step==0 else[index,p['modifier']],providedR0=0xE5980000|(step<<8)|index,rowsAlreadyZero=True,outputAlreadyZero=True))
    if r['providedCalls']!=calls:raise ValueError('598 independent ordered four-stage prepared calls differ')
    native=r['nativeReturns']
    if[len(native),[ret['entry']for ret in native]]!=[3,[M.GETTER,M.FILL,M.FILL]]:raise ValueError('598 native getter/fill return sequence differs')
    if native[0]['returnedWords'][0]!=p['modifier']or native[1]['inputWords'][:3]!=[M.ROWS,0,396]or native[2]['inputWords'][:3]!=[M.OUTPUT,0,192]:raise ValueError('598 actual16-bit getter/fill contracts differ')
    stack=M.STACK-M.BASE
    if r['after'][:stack-65536]!=expected[:stack-65536]or r['after'][stack+4096:]!=expected[stack+4096:]:raise ValueError('598 independent full RAM differs')
    return dict(count=p['count'],forwardedModifier=p['modifier'],clearedRowBytes=396,clearedOutputBytes=192,providedOrderedStageCalls=len(calls),bothBuffersClearedBeforeAnyStage=True,sourceReturnIsVoidView=True)
