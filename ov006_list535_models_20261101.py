import struct
import ov006_list535_machine_20261101 as M


def classify(word,mask=0x1FFFFF):
    flags=(word>>11)&mask;kind=flags&3
    if kind in[1,2]:return kind
    if kind!=3:return 0
    if flags&16 and not flags&8:return 5
    if flags&4 and flags&8:return 4
    return 3


def profiles():
    out=[]
    def add(name,words,countAfter=None,alias=False):out.append(dict(name=name,words=words,countAfter=countAfter,alias=alias,poison=0xA5))
    for count in range(65):add(f'prefix-{count}',[((i%3+1|[0,16,12][i%3])<<11)|((i*71)&2047)if i<count else(i*71)&2047 for i in range(64)])
    for index in range(64):add(f'single-{index}',[(((3|[0,16,12][index%3])<<11)|2047)if i==index else i&2047 for i in range(64)])
    for flags in[0,1,2,3,7,11,15,19,27,31,0x1FFFFF]:add(f'flags-{flags:x}',[(flags<<11)|i for i in range(64)])
    for seed in[0,1,0x89ABCDEF,0xFFFFFFFF]:
        word=seed;words=[]
        for i in range(64):word=(word*1664525+1013904223)&0xFFFFFFFF;words.append(word)
        add(f'raw-{seed:x}',words)
    for count in[-1,0,1,3,64]:add(f'after-{count}',[0x9800]+[0]*63,countAfter=count)
    for count in[1,32,64]:add(f'alias-{count}',[0x7800 if i<count else 0 for i in range(64)],alias=True)
    return out


def model(result,original):
    p=result['profile'];before=result['before'];want=bytearray(before);values=[classify(word,original['mask'])for word in p['words']];ids=[i+1 for i,value in enumerate(values)if value];count=len(ids);after=count if p['countAfter']is None or not count else p['countAfter'];pointer=(original['table']if p['alias']else M.OUTPUT)if count else 0
    def word(address,value):struct.pack_into('<I',want,address-M.BASE,value&0xFFFFFFFF)
    word(M.STATE,after);word(M.STATE+8,pointer)
    if result['classifierInputs']!=list(range(64)):raise ValueError('535 classifier indices differ')
    actual=[r for r in result['nativeReturns']if r['entry']==M.CLASSIFY]
    if [r['inputR0']for r in actual]!=list(range(64))or[r['returnedR0']for r in actual]!=values:raise ValueError('535 original classifiers differ from independent wordflags')
    if len(result['providedEvents'])!=int(count!=0):raise ValueError('535 unexpected supplied allocator count')
    if count:
        e=result['providedEvents'][0]
        if e['preparedWords']!=[1,count*12,4]or e['returnedPointer']!=pointer:raise ValueError('535 independent allocation contract differs')
        if after>0:
            if after>64:raise ValueError('535 unsupported postallocation count exceeds measured localarray')
            padded=ids+[0]*(64-count)
            for i in range(after):word(pointer+12*i+8,padded[i])
    expected=M.STATE if not count else after&0xFFFFFFFF
    if result['returnedR0']!=expected:raise ValueError('535 physical result differs')
    begin=M.ENTRY-M.BASE;end=begin+max(M.SIZE,result['extent']);cut=M.STACK-M.BASE
    if result['after'][:begin]!=bytes(want[:begin])or result['after'][end:cut-65536]!=bytes(want[end:cut-65536])or result['after'][cut+4096:]!=bytes(want[cut+4096:]):raise ValueError('535 complete independent nonstack RAM differs')
    return dict(originalClassifications=values,selectedIds=ids,selectedCount=count,postallocationCount=after,physicalR0=expected,outputPointer=pointer,providedCalls=int(count!=0))
