import struct
from main_dispatch481_machine_20261101 import BASE,STACK,OUTPUT,FLAGS

def profiles():
    rows=[]
    for flags in[0,1,2,3,0x80000000,0xFFFFFFFF]:
        for flags24 in[0,1,0x80000000,0xFFFFFFFF]:
            for gap in[0,0x02610000]:
                for swap in[False,True]:
                    n=len(rows)
                    options=[0,0x02610000,0x02612000]
                    rows.append(dict(name=f'flags{flags}-flags24{flags24}-gap{gap}-swap{swap}',flags=flags,flags24=flags24,gap=gap,swapLock=swap,afterB=[0,1,2,3][n%4],afterOuterCallback=[3,0,1,2][(n//3)%4],outerGap=options[n%3],innerGap=options[(n//2)%3],queueGap=options[(n//5)%3],tailGap=options[(n//7)%3]))
    return rows

def model(result,original):
    p=result['profile']
    expected=bytearray(result['before'])
    events=[]
    flags,gap=p['flags'],p['gap']
    def event(address,args):
        events.append((address,[v&0xFFFFFFFF for v in args]))
        return 0x90000000|len(events)
    def put(a,v):struct.pack_into('<I',expected,a-BASE,v&0xFFFFFFFF)
    event(0x0200708C,[0x020F5508])
    if p['swapLock']:gap=0x02612000;put(FLAGS,gap)
    if gap:event(0x0200708C,[gap+0x4C8])
    if flags&2 and p['flags24']&1:
        event(0x0203B90C,[OUTPUT])
        flags=p['afterB'];put(OUTPUT+0x110,flags)
    if flags&1:
        event(0x027FE400,[OUTPUT])
        flags=p['afterOuterCallback'];put(OUTPUT+0x110,flags)
        gap=p['outerGap'];put(FLAGS,gap)
    if flags&1:
        event(0x0203A688,[OUTPUT])
        event(0x027FE400,[OUTPUT])
        gap=p['innerGap'];put(FLAGS,gap)
        queue=struct.unpack_from('<I',original['arm'],0x0203A648-BASE)[0]
        event(0x0203A70C,[queue,OUTPUT])
        gap=p['queueGap'];put(FLAGS,gap)
        if gap:event(0x0203A70C,[gap+0x4E0,OUTPUT])
        event(0x0203A260,[OUTPUT])
        gap=p['tailGap'];put(FLAGS,gap)
    event(0x02007110,[0x020F5508])
    wanted=event(0x02007110,[gap+0x4C8]) if gap else 0
    seen=result['providedEvents']
    if len(seen)!=len(events)or any(e['address']!=a or e['rawCallerWords'][:len(args)]!=args for e,(a,args)in zip(seen,events)):
        raise ValueError(('481 independent call/pointer/order differs',p['name'],[(hex(e['address']),e['rawCallerWords'][:2])for e in seen],events))
    cut=STACK-BASE
    if expected[:cut-65536]!=result['after'][:cut-65536]or expected[cut+4096:]!=result['after'][cut+4096:]:raise ValueError(('481 complete independent nonstack effects differ',p['name']))
    if result['returnedR0']!=wanted:raise ValueError(('481 independent physical return differs',p['name'],wanted,result['returnedR0']))
    return dict(providedCalls=len(events),lastPhysicalR0=wanted,finalGapWord=gap,finalFlagsWord=flags)
