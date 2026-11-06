import random
import struct

CONTEXT = 0x02218D90
RAW = 0x020F60EC


def recipes():
    return [dict(seed=0x235000+raw*3+kind,rawByte=raw,kind=kind,argument=[0,1,2,0x7FFFFFFF,0x80000000,0xFFFFFFFF][raw%6])for raw in range(256)for kind in range(3)]


def construct(recipe):
    rng=random.Random(recipe['seed'])
    state={CONTEXT:bytearray(rng.randbytes(80)),RAW:bytearray(rng.randbytes(16))}
    argument=recipe['argument'];kind=recipe['kind']
    struct.pack_into('<I',state[CONTEXT],40,[0,1,0x80000000][kind])
    struct.pack_into('<I',state[CONTEXT],76,argument if kind==1 else argument^0xFFFFFFFF)
    initial=[(a,bytes(b))for a,b in state.items()]
    services=[];native=[]

    def snapshot():return[(a,bytes(b))for a,b in state.items()]

    def call(address,arguments,effects):
        services.append(dict(address=address,arguments=arguments,result=rng.getrandbits(32),effects=effects,before=snapshot()))
        for a,b in effects:
            base=next(base for base,data in state.items()if base<=a and a+len(b)<=base+len(data))
            state[base][a-base:a-base+len(b)]=b

    if kind==1:return initial,snapshot(),services,native,argument
    if kind==2:
        call(0x020418B0,[0],[(CONTEXT+40,rng.randbytes(4)),(CONTEXT+76,rng.randbytes(4)),(RAW+2,rng.randbytes(1))])
        struct.pack_into('<I',state[CONTEXT],40,0)
    call(0x020414C8,[0x3E if argument else 0x2E],[(RAW+2,bytes([recipe['rawByte']])),(CONTEXT+12,rng.randbytes(4))])
    for address,arguments in [(0x02041814,[]),(0x020417F8,[RAW])]:
        native.append(dict(address=address,arguments=arguments,result=recipe['rawByte'],before=snapshot()))
    call(0x02041538,[1,2,1 if recipe['rawByte']==1 else 4],[(RAW+2,bytes([recipe['rawByte']^255])),(CONTEXT+16,rng.randbytes(4))])
    call(0x0204157C,[10],[(CONTEXT+40,rng.randbytes(4)),(CONTEXT+76,rng.randbytes(4))])
    struct.pack_into('<I',state[CONTEXT],40,1);struct.pack_into('<I',state[CONTEXT],76,argument)
    return initial,snapshot(),services,native,CONTEXT
