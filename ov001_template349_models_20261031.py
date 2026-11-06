import struct
import random
ACTOR,PARAM,TEMPLATE=0x02360000,0x02361000,0x02239ABC
ASTAT=[0x1EC,0x1EE,0x1F4,0x1F6,0x1F8,0x1FA]
PSTAT=[0x32,0x34,0x36,0x38,0x3A,0x3C]
TSTAT=[0,2,8,10,12,14]

def put(raw,offset,size,value):raw[offset:offset+size]=(value&((1<<(8*size))-1)).to_bytes(size,'little')
def read(raw,offset,size,signed=False):return int.from_bytes(raw[offset:offset+size],'little',signed=signed)

def recipes(assets):
    table=assets['EnmyKindTbl.bin'][8:]
    alternative=next(i for i in range(1,len(table)//100)if 0<read(table,100*i+8,2)<len(table)//100)
    results=[]
    for species in[367,alternative]:
        for mode in[3,7]:
            for old in[False,True]:
                for stat in[-32768,-100,-1,0,1,100,32767]:
                    i=len(results)
                    results.append(dict(seed=349000+i,
                            mode=mode,
                            oldEventBit10=old,
                            species=species,
                            variant=[0,
                                1,
                                255][i%3],
                            stat=stat,
                            add=[-32768,
                                -1,
                                0,
                                1,
                                32767][(i//3)%5],
                            skillPrefix=i%6,
                            skillGap=i%4==0,
                            null=False))
    for mode in[3,7]:
        for old in[False,
            True]:results.append(dict(seed=349000+len(results),
                mode=mode,
                oldEventBit10=old,
                species=367,
                variant=0,
                stat=0,
                add=0,
                skillPrefix=0,
                skillGap=False,
                null=True))
    return results

def setup(obj,recipe):
    rng=random.Random(recipe['seed'])
    obj.u.mem_write(0x020F69E8,bytes([recipe['mode']]))
    obj.u.mem_write(TEMPLATE,rng.randbytes(132))
    actor=bytearray(rng.randbytes(0x440))
    parameter=bytearray(rng.randbytes(0x200))
    put(actor,0x1E8,4,PARAM)
    for a,p in zip(ASTAT,PSTAT):
        put(actor,a,2,recipe['stat'])
        put(parameter,p,2,recipe['add'])
    put(parameter,0x2A,2,recipe['species'])
    put(parameter,0x2C,1,recipe['variant'])
    pairs=bytearray(10)
    for index in range(recipe['skillPrefix']):
        pairs[2*index]=1+index
        pairs[2*index+1]=rng.randrange(256)
    if recipe['skillGap']and recipe['skillPrefix']>=2:pairs[2]=0
    parameter[0xD2:0xDC]=pairs
    obj.u.mem_write(ACTOR,bytes(actor))
    obj.u.mem_write(PARAM,bytes(parameter))
    first=(rng.getrandbits(32)&~0x400)|(0x400 if recipe['oldEventBit10']else 0)
    obj.word(0x021C0EE0,first)
    obj.word(0x021C0EE8,rng.getrandbits(32))
    obj.word(0x021C0E28,rng.getrandbits(32))
    return bytes(actor),bytes(parameter)

def model(before,recipe,actor,parameter,assets):
    expected=bytearray(before)
    output=bytearray(132)
    if not recipe['null']:
        table=assets['EnmyKindTbl.bin'][8:]
        alternate=read(table,100*recipe['species']+8,2)
        species=alternate if alternate else recipe['species']
        put(output,0x64,2,species)
        put(output,0x66,1,recipe['variant'])
        output[0x67]=1
        output[0x69]=actor[0x31F]
        for a,p,t in zip(ASTAT,PSTAT,TSTAT):
            value=read(actor,a,2,True)+read(parameter,p,2,True)
            put(output,t,2,value)
        output[4:8]=output[:4]
        output[0x6D:0x81]=parameter[0xB2:0xC6]
        output[0x10]=actor[0x1FC]
        output[0x14:0x1C]=actor[0x200:0x208]
        output[0x20:0x2A]=parameter[0xD2:0xDC]
        output[0x1C:0x1E]=actor[0x208:0x20A]
        count=0
        for index in range(5):
            if output[0x20+2*index]==0:break
            count+=1
        output[0x68]=count
        output[0x6A]=parameter[0xAD]
        output[0x2A:0x64]=parameter[0xDC:0x116]
        output[0x6B]=parameter[0xAE]
        output[0x6C]=parameter[0xAB]
        offset=0x021C0EE0-0x02000000
        word=read(expected,offset,4)
        put(expected,offset,4,word|0x400)
        if not word&0x400:
            off=0x021C0EE8-0x02000000
            put(expected,off,4,read(expected,off,4)|0x400)
            off=0x021C0E28-0x02000000
            put(expected,off,4,read(expected,off,4)|0x1000)
    start=TEMPLATE-0x02000000
    expected[start:start+132]=output
    return bytes(expected),bytes(output)
