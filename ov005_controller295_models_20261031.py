import functools
import random
import struct
from project import ROOT
ENTRY,CTX,TABLE=0x021DF630,0x021ED1B0,0x021E6EA4
GETTER,GATE,BYTE,ZERO=0x021DFAB0,0x02041814,0x020417F8,0x0204176C
POST1,POST2,SLOT=0x020851D4,0x02085200,0x0208522C
GATE_OBJECT,GLOBAL,RECORDS=0x020F60EC,0x0210276C,0x021CAEC0
NATIVE={ENTRY:348,GETTER:12,GATE:20,BYTE:8,ZERO:8,POST1:44,POST2:44,SLOT:56}

def word(v):
    return v&0xFFFFFFFF

@functools.lru_cache(maxsize=1)
def table_data():
    data=(ROOT/'extract/arm9_overlays/ov005.bin').read_bytes()
    raw=data[TABLE-0x021D7240:TABLE-0x021D7240+24]
    if struct.unpack('<IIIIII',raw)!=(0x021E1600,0x021E19B8,0x021E1A6C,0,0,0):
        raise ValueError('Controller295 original table differs')
    return raw

def recipes():
    nexts=[0,1,3,4,0xFFFFFFFF,0x80000000,0x12345678]
    rows=[dict(seed=295000+i,kind=0,phase=3,next=nexts[i%7],gate=i,behavior=0)for i in range(256)]
    pairs=[(0,0),(0,1),(0,2),(0,255),(1,0),(1,2),(1,3),(1,255),(3,3),(4,3)]
    rows.extend(dict(seed=296000+i*32+b,kind=k,phase=p,next=nexts[b%7],gate=[0,1,2,255][b%4],behavior=b)for i,(k,p)in enumerate(pairs)for b in range(12))
    return rows

def construct(recipe):
    rng=random.Random(recipe['seed'])
    records=bytearray(rng.randbytes(2*0x1810))
    for i in range(70):
        value=struct.unpack_from('<I',records,i*0xB0+24)[0]&~2
        struct.pack_into('<I',records,i*0xB0+24,value)
    state={CTX:bytearray(struct.pack('<IIII',recipe['kind'],recipe['phase'],word(recipe['next']),rng.getrandbits(32))),GATE_OBJECT:bytearray(rng.randbytes(16)),GLOBAL:bytearray(struct.pack('<I',rng.getrandbits(32))),RECORDS:records,TABLE:bytearray(table_data())}
    state[GATE_OBJECT][2]=recipe['gate']
    def snapshot():
        return [(a,bytes(b))for a,b in state.items()]
    def view():
        return [(CTX,bytes(state[CTX])),(GATE_OBJECT,bytes(state[GATE_OBJECT])),(GLOBAL,bytes(state[GLOBAL]))]
    def get(offset):
        return struct.unpack_from('<I',state[CTX],offset)[0]
    def put(offset,value):
        struct.pack_into('<I',state[CTX],offset,word(value))
    initial=snapshot()
    native=[]
    services=[]
    def visit(address,args,result,kind='native',depth=None,before=None):
        event=dict(address=address,arguments=[word(v)for v in args],result=word(result),before=view()if before is None else before,eventKind=kind,depth=depth)
        native.append(event)
        return event
    def callback(address,role):
        result=word(recipe['next'])if role==1 else rng.getrandbits(32)
        changed=bytearray(state[CTX])
        behavior=recipe['behavior']
        if behavior&1:
            struct.pack_into('<I',changed,0,1)
        if behavior&2:
            struct.pack_into('<I',changed,4,255)
        struct.pack_into('<I',changed,12,recipe['seed']^role)
        effects=[(CTX,bytes(changed))]
        if behavior&4:
            gate=bytearray(state[GATE_OBJECT])
            gate[2]=[0,1,255][role]
            effects.append((GATE_OBJECT,bytes(gate)))
        services.append(dict(address=address,arguments=[],result=result,effects=effects,before=view(),expectedCarrierR0=address,callbackRole=role))
        for a,b in effects:
            state[a][:]=b
        return result
    def bookkeeping():
        for address,group in[(POST1,1),(POST2,2)]:
            visit(address,[],35)
            for slot in range(35):
                pointer=0x021C96B0+group*0x1810+slot*0xB0
                index=pointer-RECORDS
                visit(SLOT,[group,slot],pointer,before=[(pointer+24,bytes(state[RECORDS][index+24:index+28]))])
        state[GLOBAL][:]=struct.pack('<I',1)
    def activation(depth):
        if depth>3:
            raise ValueError('Controller295 model recursion escaped bound')
        frame=visit(ENTRY,[],0,kind='caller',depth=depth)
        visit(GETTER,[],CTX)
        oldkind=get(0)
        oldphase=get(4)
        result=8
        transition=0
        if oldphase in[0,1,2]:
            if oldkind not in[0,1]:
                raise ValueError('Controller295 unsupported callback table index')
            callbacks=struct.unpack_from('<III',table_data(),oldkind*12)
            if oldphase==0:
                if callbacks[0]:
                    callback(callbacks[0],0)
                put(4,1)
            elif oldphase==1:
                if not callbacks[1]:
                    raise ValueError('Controller295 null update unsupported')
                nextkind=callback(callbacks[1],1)
                if nextkind!=oldkind:
                    put(12,get(0))
                    put(4,2)
                    put(8,nextkind)
                    transition=1
            else:
                if callbacks[2]:
                    callback(callbacks[2],2)
                put(4,3)
                transition=1
        elif oldphase==3:
            gate=state[GATE_OBJECT][2]
            visit(GATE,[],gate)
            visit(BYTE,[GATE_OBJECT],gate)
            if gate!=1:
                put(0,get(8))
                put(4,0)
                if get(0)in[1,3,4]:
                    result=0
        if transition and oldphase!=get(4):
            result=activation(depth+1)
        if get(0)==1:
            result=0
        else:
            bookkeeping()
        visit(ZERO,[],0)
        frame['result']=word(result)
        return result
    result=activation(0)
    return initial,snapshot(),services,native,result
