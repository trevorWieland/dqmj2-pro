import copy
from ov001_conditions494_machine_20261101 import BASE,STACK


def profiles():
    rows=[]
    def base(name):return dict(name=name,bits=0,rows=[dict(active=1,stored=0,kind=0,trigger=1 if i==0 else 0,fields={},count=0,tags=[])for i in range(3)])
    rows.append(base('base'))
    for slot in range(3):
        for trigger in[-128,-1,0,1,127]:
            p=base(f'trigger-{slot}-{trigger}')
            for i in range(3):p['rows'][i]['trigger']=trigger if i==slot else 0
            rows.append(p)
        for count in[0,1,2,8,225,226,255]:
            for at in sorted({0,max(0,count-1)}):
                p=base(f'tag-slot{slot}-n{count}-at{at}');p['rows'][slot]['count']=count;p['rows'][slot]['tags']=[(at,'target')];rows.append(p)
        for field in['active','stored','kind']:
            for value in[0,1,128,255]:
                p=base(f'valid-{slot}-{field}-{value}');p['rows'][slot][field]=value;p['rows'][slot]['count']=1;p['rows'][slot]['tags']=[(0,'target')];rows.append(p)
        for offset in[0x235,0x236,0x238,0x239,0x23A,0x23B,0x24E,0x24F,0x250,0x24C,0x237,0x23C]:
            for value in[1,255]:
                p=base(f'field-{slot}-{offset:x}-{value}');p['rows'][slot]['fields'][hex(offset)]=value;p['rows'][slot]['count']=1;p['rows'][slot]['tags']=[(0,'target')];rows.append(p)
    for bits in[0,1,2,127,128,254,255]:
        for count in[0,1,255]:
            p=base(f'bits-{bits}-n{count}');p['bits']=bits
            for r in p['rows']:r['count']=count;r['tags']=[(max(0,count-1),'target')]
            rows.append(p)
    for count in[0,1,255]:
        p=base(f'no-target-n{count}')
        for r in p['rows']:r['count']=count;r['tags']=[(max(0,count-1),0x38)]
        rows.append(p)
    return rows


def model(result):
    data=result['before'];entry=result['entry'];selector=6 if entry==0x0221D6EC else 9;tag=0x39 if selector==6 else 0x3A
    def byte(a):return data[a-BASE]
    def signed(a):return(byte(a)+128)%256-128
    def word(a):return int.from_bytes(data[a-BASE:a-BASE+4],'little')
    def valid(a):return byte(a+0x31C)!=0 and byte(a+0x1FF)==0 and byte(word(a+0x1E8)+0xAC)==0
    actors=[0x02620000+i*0x440 for i in range(3)]
    allowed=any(valid(a)and signed(a+0x22C+selector)>=1 for a in actors)
    expected=0
    eligible=[]
    if allowed:
        expected=1
        for a in actors:
            status=valid(a)and all(signed(a+o)==0 for o in[0x236,0x235,0x238,0x239,0x23A,0x23B,0x24E,0x24F,0x250,0x24C,0x237])
            status=status and signed(a+0x23C)==0 and not(byte(result['bits'])&1)
            eligible.append(status)
            if status and any(byte(a+0x35E+i)==tag for i in range(byte(a+0x323))):expected=0;break
    if result['helperWords']!=[[0x02620000,selector,1,0]]:raise ValueError('494 original policy input words differ')
    if result['providedEvents']:raise ValueError('494 unexpected provider')
    if result['returnedR0']!=expected:raise ValueError(('494 independent condition result differs',result['profile']['name'],expected,result['returnedR0']))
    cut=STACK-BASE
    if data[:cut-65536]!=result['after'][:cut-65536]or data[cut+4096:]!=result['after'][cut+4096:]:raise ValueError('494 unexpected nonstack effect')
    return dict(result=expected,initialPolicyPassed=allowed,selectorOffset=hex(0x22C+selector),rawTag=tag,visitedEligibility=eligible,providedCalls=0)
