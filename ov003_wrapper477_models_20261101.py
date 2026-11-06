import struct
from ov003_wrapper477_machine_20261101 import BASE,STACK

def profiles():
    rows=[]
    for index in[-1,0,1,31,127]:
        for low in[0,1,32767,32768,65535]:
            for cache in[False,True]:
                for mutate in[False,True]:
                    n=len(rows)
                    rows.append(dict(name=f'index{index}-low{low}-cache{cache}-mutate{mutate}',index=index,stackWord=0xDEAD0000|low,words=[[0,0,0],[0xFFFFFFFF,0x80000000,0x7FFFFFFF],[0x12345678,0x9ABCDEF0,0x80010002]][n%3],cache=cache,mutate=mutate,texture=(0xF0000000+n)&0xFFFFFFFF,bytes=[n&255,(n*7)&255,(n*11)&255,(n*13)&255],flags=(0x80000000+n*19)&0xFFFFFFFF,oldState=(0x40000000+n*17)&0xFFFFFFFF,mapped=0xA0000000+n))
    return rows

def model(result):
    p=result['profile']
    resource=0x02601000
    expected=bytearray(result['before'])
    def put(address,value,size):expected[address-BASE:address-BASE+size]=(value&((1<<size*8)-1)).to_bytes(size,'little')
    if p['mutate']:
        put(result['holder'],0x02600400,4)
        put(0x02600004,0x02601400,4)
    if p['cache']:put(resource+0x64,0,4)
    for offset,value,size in[(0x3C,p['words'][0],1),(0x3D,p['words'][1],1),(0x3E,p['words'][2],2),(0x68,p['mapped'],4),(0x18,p['flags']|2,4),(0x10,p['oldState'],4),(0x0C,16,4),(0x70,p['stackWord'],2),(0x72,0,2)]:put(resource+offset,value,size)
    wanted=[(0x020875B4,[resource,p['bytes'][1],p['bytes'][2],p['bytes'][3],p['bytes'][0],p['texture']])]
    if p['cache']:wanted.append((0x020470E4,[0x02605000]))
    wanted.extend([(0x027FE400,[0x02602000,0]),(0x0205DC70,[p['words'][0]&255,p['words'][1]&255,p['words'][2]&65535])])
    if len(result['providedEvents'])!=len(wanted)or any(e['address']!=a or e['rawCallerWords'][:len(words)]!=words for e,(a,words)in zip(result['providedEvents'],wanted)):
        raise ValueError(('477 provided word contract differs',p['name']))
    signed=(p['stackWord']+32768)%65536-32768
    if result['setterWords']!=[[resource+0x3C,8,0],[resource+0x3C,signed&0xFFFFFFFF,0]]:raise ValueError(('477 signed fifth-word/cached resource flow differs',p['name']))
    cut=STACK-BASE
    if expected[:cut-65536]!=result['after'][:cut-65536]or expected[cut+4096:]!=result['after'][cut+4096:]:raise ValueError(('477 complete nonstack effect model differs',p['name']))
    if result['returnedR0']!=resource+0x3C:raise ValueError('477 last physical R0 differs')
    return dict(providedCalls=len(wanted),lastPhysicalR0=resource+0x3C,signedFifthWord=signed,actualNestedSetterReturns=2)
