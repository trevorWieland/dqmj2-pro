import functools
import random
import struct
from project import ROOT

UPDATE,EXIT,CTX,AUX=0x021E19B8,0x021E1A6C,0x021ED438,0x021ED234
ECB,SHARED,SLOT,OBJECT,KEYS,RECORDS=0x021E981E,0x021ED348,0x021E74A8,0x023F0100,0x023F0000,0x023E0000
MAP=0x021ED11C
SPECS={UPDATE:180,EXIT:56}
NATIVE={0x021DECB0:12,0x021E0A68:12,0x021E09DC:128,0x021E0A84:12,0x021E0A74:16,0x021E0E6C:48,0x021E06A0:104,0x021DFA64:16,0x021DFA54:16,0x021DFEB8:192,0x021E0B10:88,0x020485B4:20}

def word(v):
    return v&0xFFFFFFFF

def signed8(v):
    v=v&255
    return v-256 if v&128 else v

@functools.lru_cache(maxsize=1)
def table_data():
    overlay=(ROOT/'extract/arm9_overlays/ov005.bin').read_bytes()
    return overlay[0x021E7778-0x021D7240:0x021E786C-0x021D7240]

def recipes():
    rows=[dict(seed=300000+i,entry=UPDATE,byte=i,selector=i%62,behavior=i%8,aux28=[0,1,2,0xFFFFFFFF][i%4],keys=[0,8,0xFF7,0xFFFF][i%4])for i in range(256)]
    rows.extend(dict(seed=301000+i*8+b,entry=UPDATE,byte=0,selector=i,behavior=b,aux28=0,keys=0)for i in range(62)for b in range(8))
    rows.extend(dict(seed=302000+i,entry=UPDATE,byte=1,selector=0,behavior=i%8,aux28=0,keys=0)for i in range(16))
    rows.extend(dict(seed=302100+i,entry=UPDATE,byte=0,selector=0,behavior=i%8,aux28=1,keys=1<<i)for i in range(16))
    rows.extend(dict(seed=303000+i,entry=EXIT,byte=0,selector=0,behavior=i%8,aux28=[0,1,2,0xFFFFFFFF][i%4],keys=0)for i in range(128))
    return rows

def construct(recipe):
    rng=random.Random(recipe['seed'])
    state={MAP:bytearray(rng.randbytes(16)),CTX:bytearray(rng.randbytes(0x100)),AUX:bytearray(rng.randbytes(0x180)),ECB:bytearray([recipe['byte']]),SLOT:bytearray([127 if recipe['behavior']&1 else recipe['seed']%127]),OBJECT:bytearray(rng.randbytes(32)),KEYS:bytearray(rng.randbytes(32)),RECORDS:bytearray(rng.randbytes(26*64))}
    def area(a):
        return next((base for base,b in state.items()if base<=a<base+len(b)))
    def load(a,n=4):
        base=area(a)
        return int.from_bytes(state[base][a-base:a-base+n],'little')
    def store(a,v,n=4):
        base=area(a)
        state[base][a-base:a-base+n]=word(v).to_bytes(4,'little')[:n]
    def snapshot():
        return [(a,bytes(b))for a,b in state.items()]
    def view():
        return [(a,bytes(state[a]))for a in[MAP,CTX,AUX,ECB,SLOT,OBJECT]]
    for off in[0x14,0x5C]:
        store(CTX+off,[0,1,0x7FFFFFFF,0xFFFFFFFF,0x80000000,rng.getrandbits(32)][recipe['seed']%6])
    store(CTX+0x60,recipe['selector'])
    store(AUX+0x28,recipe['aux28'])
    store(AUX+0x20,recipe['aux28'])
    store(AUX+0x2C,0 if recipe['behavior']&2 else OBJECT+8)
    store(SHARED+0x11,recipe['behavior']&4,1)
    store(KEYS+2,recipe['keys'],2)
    for i in range(26):
        store(RECORDS+i*64,0 if(i+recipe['seed'])%3==0 else rng.getrandbits(32)|1)
    initial=snapshot()
    services,native=[],[]
    def visit(address,args,result):
        event=dict(address=address,arguments=[word(v)for v in args],result=word(result),before=view())
        native.append(event)
        return event
    def service(address,args,result=None,effects=None,carrier=None):
        effects=effects or[]
        result=rng.getrandbits(32)if result is None else word(result)
        services.append(dict(address=address,arguments=[word(v)for v in args],result=result,before=view(),effects=effects,expectedCarrierR0=carrier,mode='thumb'if address==0x02089B64 else'arm'))
        for a,b in effects:
            base=area(a)
            state[base][a-base:a-base+len(b)]=b
        return result
    def effect_word(address,value):
        return(address,word(value).to_bytes(4,'little'))
    def a68():
        visit(0x021E0A68,[],SHARED)
    def a74():
        visit(0x021E0A74,[],SHARED+24)
        a68()
    def check09():
        value=load(AUX+0x28)
        visit(0x021E09DC,[],1 if value==1 else value)
        if value==1:
            visit(0x021E0A84,[],KEYS)
            service(0x0202A634,[],KEYS)
            if load(KEYS+2,2)&0xFF7:
                service(0x021E0818,[])
                a74()
                service(0x0204B61C,[SHARED+24,1])
                store(AUX+0x28,0)
                service(0x02041538,[0,2,8])
                service(0x02041908,[8,10])
                service(0x020414C8,[63])
                store(AUX+0x18,0)
        return 1 if value==1 else value
    if recipe['entry']==UPDATE:
        result=load(CTX+0x5C)
        visit(0x021DECB0,[],ECB)
        if load(ECB,1)==1:
            outcome=[0,1,0x80000000,0xFFFFFFFF][recipe['seed']%4]
            service(0x0205E844,[62],outcome,[effect_word(CTX+0x5C,rng.getrandbits(32))])
            if outcome:
                visit(0x021DECB0,[],ECB)
                store(ECB,0,1)
        elif check09()!=1:
            effects=[effect_word(CTX+0x5C,rng.getrandbits(32))]
            if recipe['behavior']&1:
                effects.append(effect_word(CTX+0x14,0xFFFFFFFF))
            if recipe['selector']==61:
                result=service(0x021E4E48,[],rng.getrandbits(32),effects)
            else:
                target=struct.unpack_from('<I',table_data(),recipe['selector']*4)[0]
                if not target or target&1:
                    raise ValueError('Callbacks300 unsupported callback address/mode')
                service(target,[],effects=effects,carrier=target)
            service(0x021DFD70,[])
            effects=[]
            if recipe['behavior']&2:
                effects=[effect_word(CTX+0x14,0x7FFFFFFF),(SHARED+0x11,bytes([1]))]
            service(0x021E5DCC,[],effects=effects)
            a68()
            if load(SHARED+0x11,1):
                service(0x021E4E80,[])
            store(CTX+0x14,load(CTX+0x14)+1)
    else:
        service(0x02089B64,[])
        visit(0x021E0E6C,[],AUX)
        if load(AUX+0x20)==1:
            service(0x0205F5F4,[load(AUX+0x24)])
        store(AUX+0x20,0)
        slot_return=[0,1,2,3,0x12345601,0x80000002,0xFFFFFF03][recipe['seed']%7]
        visit(0x021E06A0,[],signed8(slot_return))
        for i in range(26):
            pointer=RECORDS+i*64
            effects=[effect_word(CTX+0x28,rng.getrandbits(32))]if i==12 else[]
            service(0x02049AD0,[i+4],pointer,effects)
            if load(pointer):
                service(0x02049898,[pointer],effects=[effect_word(pointer,0)])
        service(0x02048F6C,[1],slot_return)
        other=[3,2,1,0,0x89ABCD02][recipe['seed']%5]
        service(0x02048F6C,[1],other)
        pair=load(MAP+signed8(other)*4)
        visit(0x021DFA64,[signed8(other)],pair)
        visit(0x021DFA54,[signed8(slot_return),pair],signed8(slot_return))
        store(MAP+signed8(slot_return)*4,pair)
        service(0x0202A498,[1,load(CTX+0x28)])
        final=rng.getrandbits(32)
        visit(0x021DFEB8,[],final)
        slot=load(SLOT,1)
        visit(0x021E0B10,[],127 if slot==127 else SLOT)
        if slot!=127:
            pointer=load(AUX+0x2C)
            visit(0x020485B4,[pointer],pointer)
            if pointer:
                store(pointer,0)
                store(pointer+4,0)
            service(0x020484DC,[1,slot])
            store(AUX+0x2C,0)
            store(AUX+0x1C,0)
            store(SLOT,127,1)
        release=0x021ED33C+28
        service(0x0204983C,[signed8(load(release,1)),3],effects=[(release,bytes([recipe['seed']&255]))])
        service(0x0204983C,[signed8(load(release,1)),127])
        for kind in[0,1,12,2,5,6,7,8]:
            service(0x0204983C,[127,kind])
        for pointer in[0x021ED264,0x021ED2AC,0x021ED2F4]:
            service(0x0204B77C,[pointer],effects=[effect_word(pointer,0)])
        a74()
        service(0x0204B77C,[SHARED+24],effects=[effect_word(SHARED+24,0)])
        service(0x02049D50,[],final)
        service(0x020BEFB8,[0])
        result=service(0x020653AC,[],[0,1,0xFFFFFFFF,0x80000000,rng.getrandbits(32)][recipe['seed']%5])
    return initial,snapshot(),services,native,word(result)
