import random
import struct
RECORDS,STATE,TEMPLATE=0x021BD674,0x0223DEF8,0x02239ABC

def read(raw,offset,size,signed=False):return int.from_bytes(raw[offset:offset+size],'little',signed=signed)

def put(raw,offset,size,value):raw[offset:offset+size]=(value&((1<<(8*size))-1)).to_bytes(size,'little')

def records(raw):return[raw[i*132:(i+1)*132]for i in range(100)]

def keyed(raw):return{read(r,20,4):r for r in records(raw)if read(r,20,4)}

def features(assets,species,variant,skills):
    kind=assets['EnmyKindTbl.bin'][8+species*100:8+(species+1)*100]
    flags=read(kind,4,2)
    group=(flags>>8)&15
    category=group//3
    if category not in[0,1,2]:raise ValueError('Recruit353 unsupported raw feature category')
    offset=((flags&15)-1)//3 if flags&15 else 0
    maximum=min(4,variant+offset+2)if category==0 else min(4,(variant+offset)//2+3)if category==1 else 4
    result=[v for v in kind[63:63+maximum]if v]
    feat=assets['FeatTbl.bin'][8:]
    skill=assets['SkillTbl.bin'][8:]
    for index in range(5):
        ident,allocated=skills[2*index:2*index+2]
        if not ident or ident>=len(skill)//60:continue
        row=skill[60*ident:60*(ident+1)]
        for threshold,feature in zip(row[:10],row[50:60]):
            if not feature or allocated<threshold:continue
            record=feat[8*feature:8*(feature+1)]
            if not record[0]&4 and any(v in[feature,record[1]]for v in result):continue
            child=next((i for i in range(len(feat)//8)if feat[8*i+1]==feature),0)
            if child>0 and child in result:result.remove(child)
            result.append(feature)
    if len(result)>64:raise ValueError('Recruit353 feature list overflow in model')
    return result

def recipes(assets):
    table=assets['EnmyKindTbl.bin'][8:]
    species=[367]+[next(i for i in range(1,len(table)//100)if ((read(table,100*i+4,2)>>8)&15)//3==category and not read(table,100*i+8,2))for category in[1,2]]
    results=[]
    for ident in species:
        for mode in[0,3,7,10]:
            for count in[0,1,5]:
                i=len(results)
                results.append(dict(seed=353000+i,species=ident,variant=i%3,mode=mode,skillCount=count,raw33=[0,1,127,255][i%4],flag20=i%2==0,itemBoost=i%3==0,base=[-32768,-1,100,9998,32767][i%5],existingCount=i%4,contextWord=(0xF3530000+i)&0xFFFFFFFF,callerWord=[3,0x7F,0x80,0xFF][i%4]))
    return results

def setup(obj,recipe):
    rng=random.Random(recipe['seed'])
    template=bytearray(rng.randbytes(132))
    put(template,0,2,recipe['base'])
    put(template,2,2,recipe['base']+1)
    put(template,0x64,2,recipe['species'])
    put(template,0x66,1,recipe['variant'])
    template[0x67]=1
    template[0x68]=recipe['skillCount']
    template[0x13]=recipe['raw33']
    template[0x11]=13 if recipe['itemBoost']else 0
    template[0x20:0x2A]=bytes(10)
    for index in range(recipe['skillCount']):template[0x20+2*index:0x22+2*index]=bytes([1+index,[0,1,40,100,255][index]])
    obj.u.mem_write(TEMPLATE,bytes(template))
    obj.u.mem_write(STATE,rng.randbytes(0x24))
    obj.u.mem_write(0x021B9BD0,bytes([0xA5]*3))
    obj.u.mem_write(0x020F69E8,bytes([recipe['mode']]))
    obj.word(0x020F69E4,0x20 if recipe['flag20']else 0)
    obj.u.mem_write(0x020DDD40,bytes([1 if recipe['itemBoost']else 0]))
    obj.u.mem_write(RECORDS,bytes(13200))
    for i in range(recipe['existingCount']):
        row=bytearray(rng.randbytes(132))
        put(row,20,4,101+2*i)
        obj.u.mem_write(RECORDS+132*i,bytes(row))
    obj.word(0x021BD520,1000+recipe['seed']%100)
    obj.u.mem_write(0x021BD540,struct.pack('<6I',101 if recipe['existingCount']else 0,0,0,0,0,0))
    return bytes(template)

def model(before,after,assets,recipe,template,result):
    offset=RECORDS-0x02000000
    old=keyed(before[offset:offset+13200])
    new=keyed(after[offset:offset+13200])
    expected_uid=read(before,0x021BD520-0x02000000,4)+1
    row=bytearray(132)
    put(row,20,4,expected_uid)
    row[24:27]=template[0x64:0x67]
    row[0x20:0x40]=template[:32]
    row[0x7A:0x7A+2*recipe['skillCount']]=template[0x20:0x20+2*recipe['skillCount']]
    row[0x1B]=template[0x6A]
    row[0x1E]=template[0x6B]
    if recipe['mode']in[3,7]:
        row[0x40:0x7A]=template[0x2A:0x64]
        row[0x1C]=template[0x6C]
    if recipe['flag20']:row[0x1D]=1
    present=features(assets,recipe['species'],recipe['variant'],row[0x7A:0x84])
    weights=[5,10,15,20,22,24,26,28,30,35]
    bonuses=[sum(present.count(start+i)*weight for i,weight in enumerate(weights))for start in[128,138]]
    for index,target in enumerate([0x24,0x26]):
        value=read(row,0x20+2*index,2,True)+bonuses[index]
        if recipe['itemBoost']:value+=assets['ItemTbl.bin'][8+88*template[0x11]+33+index]
        put(row,target,2,min(value,9999))
    expected=dict(old)
    expected[expected_uid]=bytes(row)
    state_start=STATE-0x02000000
    state=bytearray(before[state_start:state_start+0x24])
    put(state,0x10,4,recipe['contextWord'])
    put(state,5,1,recipe['callerWord'])
    state[6]=0
    for field,value in[(0x20,0),(0x1C,expected_uid),(0x14,0)]:put(state,field,4,value)
    if result!=STATE or new!=expected or after[state_start:state_start+0x24]!=state:raise ValueError('Recruit353 independent live-record/context/return model differs')
    if read(after,0x021BD520-0x02000000,4)!=expected_uid:raise ValueError('Recruit353 counter differs')
    for address,size in[(0x021BD540,24),(TEMPLATE,132)]:
        start=address-0x02000000
        if before[start:start+size]!=after[start:start+size]:raise ValueError('Recruit353 group/template mutation differs')
    if after[0x021B9BD0-0x02000000:0x021B9BD3-0x02000000]!=bytes([1,2,3]):raise ValueError('Recruit353 native three-byte state differs')
    if row[0x33]!=recipe['raw33']:raise ValueError('Recruit353 supplied raw33 copy differs')
    return dict(returnWord=hex(result),newUid=expected_uid,raw33=row[0x33],features=present,derivedHalfwords=[read(row,0x24,2,True),read(row,0x26,2,True)],liveRecords=len(expected),childSha256=__import__('hashlib').sha256(row).hexdigest(),independentlyModeled='every live record,context fields,counter,group/template immutability,three-byte state,feature-derived stat halfwords; other bitmap/unused-row effects only original/source paired equality')
