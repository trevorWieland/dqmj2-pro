import random
import struct

DATA=0x02400000
OUT=DATA+0xF000
SPECS={0x02034480:72,0x020344C8:72,0x02034558:336,0x020348AC:220,0x02034AB8:96,
 0x02034988:32,0x02034A1C:156,0x02034758:340,0x020349A8:16,0x02034510:60,
 0x020346C0:60,0x0203470C:60,0x020349B8:60}


def put16(page,address,value):
    raw=struct.pack("<H",value)
    if isinstance(page,dict):page.update({address-DATA+i:b for i,b in enumerate(raw)})
    else:page[address-DATA:address-DATA+2]=raw
def put32(page,address,value):
    raw=struct.pack("<I",value&0xFFFFFFFF)
    if isinstance(page,dict):page.update({address-DATA+i:b for i,b in enumerate(raw)})
    else:page[address-DATA:address-DATA+4]=raw
def word(page,address):return struct.unpack_from("<I",page,address-DATA)[0]


def cell_attrs(page,expected,bank,index):
    count=[0,1,2,7,31,127,255][index%7];array=bank+0x100
    put16(page,bank,count);put32(page,bank+4,array-bank);put32(expected,bank+4,array)
    for i in range(count):
        value=[0,4,0x3000+i*4][(index+i)%3]
        put32(page,array+i*4,value);put32(expected,array+i*4,bank+value)
    return dict(count=count,array=array)


def animation(page,expected,bank,index):
    sequences=[0,1,2,7][index%4];seq=bank+0x100;frames=bank+0x1000;contents=bank+0x3000
    put16(page,bank,sequences);cursor=0
    for offset,target in[(4,seq),(8,frames),(12,contents)]:put32(page,bank+offset,target-bank);put32(expected,bank+offset,target)
    for i in range(sequences):
        count=[0,1,2,7][(index//4+i)%4];record=seq+i*16
        put16(page,record,count);put32(page,record+12,cursor*8);put32(expected,record+12,frames+cursor*8)
        for j in range(count):
            target=frames+cursor*8;value=(cursor*12+(index%3)*4)
            put32(page,target,value);put32(expected,target,contents+value);cursor+=1
    put16(page,bank+2,cursor)
    extended=index%2!=0;extra=bank+0x5000;attrs=extra+8;attribute_seq=attrs+0x100
    put32(page,bank+20,extra-bank if extended else 0)
    if extended:
        put32(expected,bank+20,extra);count=[0,1,2,7][(index//8)%4]
        put16(page,attrs,count);put32(page,attrs+4,attribute_seq-attrs);put32(expected,attrs+4,attribute_seq)
        for i in range(count):
            record=attribute_seq+i*12;num=[0,1,2,7][(index+i)%4];frame_attrs=attrs+0x1000+i*0x100
            put16(page,record,num);put32(page,record+4,0x3000+i*32);put32(expected,record+4,attrs+0x3000+i*32)
            put32(page,record+8,frame_attrs-attrs);put32(expected,record+8,frame_attrs)
            for j in range(num):put32(page,frame_attrs+j*4,0x4000+i*128+j*4);put32(expected,frame_attrs+j*4,attrs+0x4000+i*128+j*4)
    return dict(sequences=sequences,frames=cursor,extended=extended)


def cells(page,expected,bank,index,absolute=False):
    count=[0,1,2,7,31,127,255][index%7];stride=16 if index%2 else 8;array=bank+0x100;oam=array+count*stride
    put16(page,bank,count);put16(page,bank+2,0xA500|(index%2))
    put32(page,bank+4,array if absolute else array-bank)
    if absolute:return dict(count=count,stride=stride,oam=oam)
    put32(expected,bank+4,array)
    for i in range(count):put32(page,array+i*stride+4,i*6);put32(expected,array+i*stride+4,oam+i*6)
    transfer=bank+0x3000;extended=bank+0x5000
    put32(page,bank+12,transfer-bank if(index//2)%2 else 0)
    if(index//2)%2:
        put32(page,transfer+4,0x100);put32(expected,bank+12,transfer);put32(expected,transfer+4,transfer+0x100)
    put32(page,bank+20,extended-bank if(index//4)%2 else 0)
    if(index//4)%2:put32(expected,bank+20,extended);cell_attrs(page,expected,extended+8,index//8)
    return dict(count=count,stride=stride,oam=oam,transfer=bool((index//2)%2),extended=bool((index//4)%2))


def font(page,expected,file,index,parent=False):
    header=[16,32,64][index%3];count=[0,1,2,4,7,12][(index//3)%6]
    put16(page,file+12,header);put16(page,file+14,count);put16(page,file+6,0x100+(index%3));put32(page,file,0x4E465452)
    first=None
    for i in range(count):
        block=file+header+i*0x80;kind=[0x46494E46,0x43474C50,0x43574448,0x434D4150,0xDEADBEAF][(index//18+i)%5]
        put32(page,block,kind);put32(page,block+4,0x80);payload=block+8
        if kind==0x46494E46:
            if first is None:first=payload
            put32(page,payload+8,0x3000);put32(expected,payload+8,file+0x3000)
            for off,relative in[(12,0x4000 if index%2 else 0),(16,0x5000 if(index//2)%2 else 0)]:
                put32(page,payload+off,relative)
                if relative:put32(expected,payload+off,file+relative)
        if kind in[0x43574448,0x434D4150]:
            offset=4 if kind==0x43574448 else 8;relative=0x6000 if(index+i)%2 else 0
            put32(page,payload+offset,relative)
            if relative:put32(expected,payload+offset,file+relative)
    if parent:
        put32(expected,OUT,first or 0)
        if first and index%3==0:expected[file-DATA+0x3000+7]=0
    return dict(blocks=count,headerSize=header,firstInfo=first,version=0x100+(index%3)),1 if first else 0


def build(entry,index):
    rng=random.Random(0x98400000+index);page=bytearray(rng.randbytes(65536));expected={}
    bank=DATA+0x1000;file=DATA+0x100;result=None;context={};arguments=[bank]
    if entry==0x02034AB8:
        reader=bank;source=DATA+0x4000;available=index%9;bits=(index//9)%9;current=rng.randrange(256)
        put32(page,reader,source);page[reader-DATA+4]=available;page[reader-DATA+5]=current
        value=0;left=available;position=source;byte=current
        for i in range(bits):
            if left==0:byte=page[position-DATA];position+=1;left=8
            value=(value<<1)|((byte>>(left-1))&1);left-=1
        put32(expected,reader,position);expected[reader-DATA+4]=left;expected[reader-DATA+5]=byte
        arguments=[reader,bits];result=value;context=dict(bits=bits,available=available)
    elif entry==0x02034480:
        header=[16,32,64][index%3];count=[0,1,2,7,31,64][(index//3)%6];query=[0x41424E4B,0x46494E46,0xDEAD0000][(index//18)%3]
        put16(page,file+12,header);put16(page,file+14,count);cursor=file+header;found=0
        for i in range(count):
            kind=query if i==[0,count//2,count-1,-1][(index//54)%4]else 0xABCD0000+i
            size=[8,12,16,32][(index+i)%4];put32(page,cursor,kind);put32(page,cursor+4,size)
            if kind==query and not found:found=cursor
            cursor+=size
        arguments=[file,query];result=found;context=dict(blocks=count,headerSize=header,found=found)
    elif entry in[0x020348AC,0x02034758]:
        context,result=font(page,expected,file,index,parent=entry==0x02034758)
        arguments=[file,OUT]if entry==0x02034758 else[file]
        if entry==0x020348AC:result=None
    elif entry in[0x020344C8,0x020349A8]:
        actual=bank+8 if entry==0x020349A8 else bank
        context=cell_attrs(page,expected,actual,index)
    elif entry==0x02034558:context=animation(page,expected,bank,index)
    elif entry in[0x02034A1C,0x02034988]:
        context=cells(page,expected,bank,index,absolute=entry==0x02034988)
        if entry==0x02034988:result=context["oam"]
    else:
        kind={0x02034510:0x41424E4B,0x020346C0:0x43484152,0x0203470C:0x504C5454,0x020349B8:0x4345424B}[entry]
        header=[16,32,64][index%3];present=index%4!=0;put16(page,file+12,header);put16(page,file+14,1 if present else 0)
        block=file+header;bank=block+8;put32(page,block,kind);put32(page,block+4,0xC000)
        if present:
            if entry==0x02034510:context=animation(page,expected,bank,index)
            elif entry==0x020349B8:context=cells(page,expected,bank,index)
            else:
                offset=20 if entry==0x020346C0 else 12
                put32(page,bank+offset,0x1000);put32(expected,bank+offset,bank+0x1000)
        put32(expected,OUT,bank if present else 0);arguments=[file,OUT];result=int(present);context.update(present=present)
    modeled=bytearray(page)
    for offset,value in expected.items():modeled[offset]=value
    return page,modeled,arguments,result,context
