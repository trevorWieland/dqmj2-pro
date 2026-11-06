import struct
OFFSETS=[0x20,0x22,0x28,0x2A,0x2C,0x2E]
CHILD=0x022474C8
PARENTS=0x02247480

def word(raw,offset,size,signed=False):
    return int.from_bytes(raw[offset:offset+size],'little',signed=signed)

def put(raw,offset,size,value):
    raw[offset:offset+size]=(value&((1<<(size*8))-1)).to_bytes(size,'little')

def recipes():
    recipes=[]
    for i in range(128):
        recipes.append(dict(seed=33000+i,
                alias=i%11==0,
                case=i,
                stats=[-32768,
                    -1,
                    0,
                    1,
                    5000,
                    32767][i%6],
                levels=[(0,
                        0),
                    (10,
                        10),
                    (10,
                        11),
                    (20,
                        20),
                    (20,
                        21),
                    (99,
                        99)][(i//6)%6],
                limitA=[0,
                    5,
                    98,
                    99,
                    255][(i//3)%5],
                limitB=[0,
                    1,
                    90,
                    99,
                    254][(i//7)%5],
                generationA=[0,
                    98,
                    99,
                    254,
                    255][i%5],
                generationB=[0,
                    97,
                    100,
                    254,
                    255][(i//5)%5],
                flagsA=i%8,
                flagsB=(i//8)%8,
                pointsA=[-32768,
                    -1,
                    0,
                    1000,
                    32767][i%5],
                pointsB=[-32768,
                    -1,
                    0,
                    1000,
                    32767][(i//5)%5],
                bonus=[-1000,
                    0,
                    999,
                    32767][(i//9)%4],
                scratch33=[0,
                    1,
                    127,
                    255][i%4]))
    return recipes

def setup(obj,rows,recipe):
    chosen=[r for r in rows if word(r,20,4)][:2]
    uids=[word(r,20,4)for r in chosen]
    pointers=[0x021BD674+rows.index(r)*132 for r in chosen]
    for side,pointer in enumerate(pointers):
        data=bytearray(obj.u.mem_read(pointer,132))
        for j,offset in enumerate(OFFSETS):
            put(data,offset,2,recipe['stats']if j%2==0 else -recipe['stats']-1)
        data[0x30]=recipe['levels'][side]
        data[0x1C]=recipe['limitA'if side==0 else'limitB']
        data[0x1E]=recipe['generationA'if side==0 else'generationB']
        data[0x1D]=recipe['flagsA'if side==0 else'flagsB']
        put(data,0x3C,2,recipe['pointsA'if side==0 else'pointsB'])
        obj.u.mem_write(pointer,bytes(data))
    if recipe['alias']:
        pointers[1],uids[1]=pointers[0],uids[0]
    parents=[bytes(obj.u.mem_read(p,132))for p in pointers]
    obj.u.mem_write(CHILD+0x33,bytes([recipe['scratch33']]))
    return [uids[0],uids[1],word(parents[0],0x18,2,True),0,recipe['bonus']],pointers,parents

def model(before,args,pointers,parents,assets,seed):
    result=bytearray(before)
    raw=bytearray(result[CHILD-0x02000000:CHILD-0x02000000+132])
    put(result,PARENTS+4-0x02000000,4,pointers[0])
    put(result,PARENTS+8-0x02000000,4,pointers[1])
    put(raw,0x18,2,args[2])
    put(raw,0x1A,1,args[3])
    caps=struct.unpack_from('<6H',assets['EnmyKindTbl.bin'],8+100*args[2]+0x10)
    for offset,cap in zip(OFFSETS,caps):
        average=(word(parents[0],offset,2,True)+word(parents[1],offset,2,True))>>2
        put(raw,offset,2,min(average,cap))
    raw[0x24:0x28]=raw[0x20:0x24]
    put(raw,0x38,4,0xABC000+seed)
    summed=parents[0][0x30]+parents[1][0x30]
    a,b=parents[0][0x1C],parents[1][0x1C]
    value=max(a,b)+1 if summed<=20 else max(a,b)+(min(a,b)//2)+1 if summed<=40 else a+b+1
    raw[0x1C]=min(value,99)
    if word(raw,0x20,2,True)<=0:
        put(raw,0x20,2,1)
        put(raw,0x24,2,1)
    for side,p in enumerate(parents):
        raw[0x40+2*side:0x42+2*side]=p[0x18:0x1A]
        raw[0x4C+side]=p[0x1A]
        raw[0x52+20*side:0x66+20*side]=p[:20]
        for old,new,oldv,newv in[(0x40,0x44+2*side,0x4C,0x4E+side),(0x42,0x48+2*side,0x4D,0x50+side)]:
            raw[new:new+2]=p[old:old+2]
            raw[newv]=p[oldv]
    raw[0x1E]=min((max(p[0x1E]for p in parents)+1)&255,99)
    a,b=(p[0x1D]for p in parents)
    raw[0x1D]=((a&1)<<1)|((b&1)<<2)|((a&2)<<2)|((a&4)<<2)|((b&2)<<4)|((b&4)<<4)
    raw[0x30]=1
    summed=sum(word(p,0x3C,2,True)for p in parents)
    half=summed//2 if summed>=0 else -((-summed)//2)
    put(raw,0x3C,2,min(args[4]+half,999))
    result[CHILD-0x02000000:CHILD-0x02000000+132]=raw
    return bytes(result),caps
