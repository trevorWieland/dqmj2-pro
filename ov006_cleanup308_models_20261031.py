import random
import struct

ENTRY,RECORDS,BANK,MAP,HEADER=0x021DEC9C,0x02102A18,0x021029D0,0x0220F500,0x023F0000
SPECS={ENTRY:104}
NATIVE={0x02049AD0:20,0x02048F6C:16,0x02049898:168,0x021DDF08:16,0x021DDF18:16}

def word(v):
    return v&0xFFFFFFFF

def recipes():
    return[dict(entry=ENTRY,seed=308000+bank*28+pattern,bank=bank,pattern=pattern)for bank in range(4)for pattern in range(28)]

def construct(recipe):
    rng=random.Random(recipe['seed'])
    state={RECORDS:bytearray(rng.randbytes(29*12)),BANK:bytearray(rng.randbytes(4)),MAP:bytearray(rng.randbytes(16)),HEADER:bytearray(rng.randbytes(16))}
    state[BANK][1]=recipe['bank']
    struct.pack_into('<I',state[HEADER],4,0)
    for i in range(25):
        p=recipe['pattern']
        nonzero=p==1 or p==2 and i%2==0 or p>=3 and i==p-3
        struct.pack_into('<I',state[RECORDS],(i+4)*12,HEADER if nonzero else 0)
    def snapshot():
        return[(a,bytes(b))for a,b in state.items()]
    initial=snapshot()
    native=[]
    def visit(address,args,result):
        native.append(dict(address=address,arguments=[word(v)for v in args],result=word(result),before=snapshot()))
    for i in range(4,29):
        pointer=RECORDS+i*12
        visit(0x02049AD0,[i],pointer)
        if struct.unpack_from('<I',state[RECORDS],i*12)[0]:
            visit(0x02049898,[pointer],HEADER)
    visit(0x02048F6C,[1],recipe['bank'])
    visit(0x02048F6C,[1],recipe['bank'])
    value=struct.unpack_from('<I',state[MAP],recipe['bank']*4)[0]
    visit(0x021DDF18,[recipe['bank']],value)
    visit(0x021DDF08,[recipe['bank'],value],recipe['bank'])
    return initial,snapshot(),[],native,recipe['bank']
