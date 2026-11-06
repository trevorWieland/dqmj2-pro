import random

BUFFER = 0x0301FE6C


def recipes():
    rows=[]
    for index in range(192):
        rng=random.Random(0x228000+index)
        words=[rng.getrandbits(32)for unused in range(8)]
        for offset in range(4,8):
            words[offset]=[0,1,0x7FFFFFFF,0x80000000,0xFFFFFFFF][(index+offset)%5]
        rows.append(dict(seed=0x228000+index,arguments=words,result=[0,1,0xFFFFFFFF,0x80000000,0x7FFFFFFF,0xFFFF0001][index%6]))
    return rows


def construct(recipe):
    rng=random.Random(recipe['seed']^0x800000)
    buffer=rng.randbytes(128)
    words=recipe['arguments']
    return [dict(address=0x020877BC,arguments=[words[1],BUFFER,128,words[2]],result=rng.getrandbits(32),bufferBefore=b'\0'*128,bufferAfter=buffer),
        dict(address=0x021E775C,arguments=[words[0],BUFFER,words[3],*words[4:8]],result=recipe['result'],bufferBefore=buffer,bufferAfter=buffer[:-4]+b'\xFF\0\x80\x7F')]
