import itertools
import struct
SPECS = {name: {} for name in ['020d3dc0','020d3e20','020d3e80']}
SP, STOP, STATE = 0x027f0000, 0x027e0000, 0x021d71fc
WIDGETS = []


def fixtures(name):
    return [dict(mode=mode,index=index,seed=seed) for mode,index,seed in itertools.product([-1,0,1,2,3,4],[0,1,2,3,4,5,6,0xffffffff,0x80000000],range(3))]


def scenario(name,f,ordinal):
    raw = bytearray((i*31+ordinal*7)&255 for i in range(86))
    ids = [-32768,-1,0,1,32767,0x1234,-2,2,256]
    variants = [0,1,127,128,255,254,129,2,64]
    categories = [255,128,127,1,0,129,254,2,64]
    for i in range(9):
        j = (i+f['seed']*3)%9
        struct.pack_into('<h',raw,16+i*6,ids[j])
        raw[16+i*6+2] = variants[j]
        raw[16+i*6+4] = categories[j]
    result = -1 if name=='020d3dc0' else 0
    count = 3 if f['mode']==1 else 6 if f['mode'] in [2,3] else 0
    if f['index'] < count:
        offset = 16+(f['index']+(0 if f['mode']==1 else 3))*6
        if name=='020d3dc0':result=struct.unpack_from('<h',raw,offset)[0]
        else:result=raw[offset+(2 if name=='020d3e20' else 4)]
    return dict(initial={STATE-16:bytes(raw)},regions={STATE-16:bytes(raw)},actions=[],result=result&0xffffffff)
