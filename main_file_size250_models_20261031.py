import random
import struct

ERROR=0x020EDEC8
SP=0x0301FF00
FILE=SP-88


def recipes():
    pairs=[(0,0),(0,1),(1,0),(0,0xFFFFFFFF),(0xFFFFFFFF,0),(0x80000000,0x7FFFFFFF),(0x7FFFFFFF,0x80000000),(0xFFFFFFFF,0xFFFFFFFF)]
    return [dict(seed=0x250000+i,path=path,start=start,end=end,opened=opened,mutate=mutate)for i,(path,start,end,opened,mutate)in enumerate((path,start,end,opened,mutate)for path in [0,1,0x02300000,0xFFFFFFFF]for start,end in pairs for opened in [0,1,0x80000000,0xFFFFFFFF]for mutate in [0,1])]


def construct(recipe,initial_file,initial_error):
    rng=random.Random(recipe['seed']^0x800000)
    file=bytearray(initial_file);error=initial_error;services=[]
    for offset,value in [(0,0),(4,0),(8,0),(12,0),(16,14),(24,0),(28,0)]:struct.pack_into('<I',file,offset,value)
    initialized=bytes(file)
    open_file=bytearray(rng.randbytes(72));struct.pack_into('<II',open_file,36,recipe['start'],recipe['end'])
    services.append(dict(address=0x0200BFE4,arguments=[FILE,recipe['path']],result=recipe['opened'],fileBefore=bytes(file),errorBefore=error,fileAfter=bytes(open_file),errorAfter=rng.getrandbits(32)))
    file=open_file
    if recipe['opened']:
        result=(recipe['end']-recipe['start'])&0xFFFFFFFF
        error=0 if result else 3
        after=bytearray(file);struct.pack_into('<II',after,36,rng.getrandbits(32),rng.getrandbits(32))
        final_error=rng.getrandbits(32)if recipe['mutate']else error
        services.append(dict(address=0x0200C02C,arguments=[FILE],result=rng.getrandbits(32),fileBefore=bytes(file),errorBefore=error,fileAfter=bytes(after),errorAfter=final_error))
        file=after;error=final_error
    else:result=0;error=1
    return initialized,bytes(file),error,services,result
