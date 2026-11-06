import random
import struct
from ov001_query265_models_20261031 import action_table
ENTRY, ACTION, LOOKUP, ELIGIBLE = 0x0222BF54,0x0207AFEC,0x021DB438,0x021DB8D0
MAP, BYTE, FIND, COPY = 0x0205D790,0x0205D764,0x0205CA0C,0x021D8B4C
TARGET, FALLBACK = 0x021EEC7C,0x021EEDBC
ACT_PTR, ACT_TABLE, ROWS, COPY_TABLE = 0x021C6748,0x02300000,0x02102E2C,0x0223161C
BASES=[0x02236F6C,0x022362AC,0x022355EC,0x02237C2C]
NATIVE={ACTION:20,LOOKUP:124,ELIGIBLE:72,MAP:60,BYTE:44,FIND:56,COPY:44}

def s32(v):
    return (v&0xFFFFFFFF)-0x100000000 if v&0x80000000 else v&0xFFFFFFFF

def recipes():
    rows=[dict(seed=280000+action*8+mode,action=action,mode=mode,side=action%4,mask=action//4%8)for action in range(256)for mode in range(8)]
    rows.extend(dict(seed=285000+action*8+i,action=action,mode=5,side=side,mask=0)for action in range(8)for i,side in enumerate([4,255,256,0x80000000,0xFFFFFFFF]))
    return rows

def construct(recipe):
    rng=random.Random(recipe['seed'])
    action,mode,side=recipe['action'],recipe['mode'],recipe['side']
    field=struct.unpack_from('<h',action_table(),8+action*40+12)[0]
    fieldword=field&0xFFFFFFFF
    records=bytearray(rng.randbytes(32*0xAC))
    ids=[0x40000000+i*0x10001 for i in range(32)]
    kind=[1,2,3,0,4,127,128,255][mode]
    if mode!=7:
        index=[0,15,31][(action+mode)%3]
        ids[index]=fieldword
        if index==0:
            ids[23]=fieldword
    for i,key in enumerate(ids):
        struct.pack_into('<I',records,i*0xAC+4,key)
        records[i*0xAC+0x7A]=kind
    index=ids.index(fieldword)if fieldword in ids else -1
    raw=(kind if kind<128 else kind-256)if index>=0 else -1
    selector=raw-1 if raw in[1,2,3]else -1
    group=side if side<4 else 0
    actors=BASES[group]
    descriptors=0x02310000+group*0x1000
    actorbytes=bytearray(rng.randbytes(3*0x440))
    descriptorbytes=bytearray(rng.randbytes(3*0x100))
    for i in range(3):
        enabled=bool(recipe['mask']&(1<<i))
        struct.pack_into('<I',actorbytes,i*0x440+0x1E8,descriptors+i*0x100)
        actorbytes[i*0x440+0x31C]=[1,2,255][i]if enabled or i!=0 else 0
        actorbytes[i*0x440+0x1FF]=0 if enabled or i!=1 else 255
        descriptorbytes[i*0x100+0xAC]=0 if enabled or i!=2 else 127
    copyindex=3 if side==0 else 11
    copyaddress=COPY_TABLE+copyindex*16
    words=[rng.getrandbits(32),rng.getrandbits(32),[0,1,0xFFFFFFFF,0x80000000,0x7FFFFFFF,0x10000000,0xF0000000,0x1234ABCD][(action+mode)%8],0xA17C00DE]
    state={ACT_PTR:bytearray(struct.pack('<I',ACT_TABLE)),ACT_TABLE:bytearray(action_table()[8:]),ROWS:records,actors:actorbytes,descriptors:descriptorbytes,copyaddress:bytearray(struct.pack('<IIII',*words))}
    def snapshot():
        return [(a,bytes(b))for a,b in state.items()]
    initial=snapshot()
    native=[]
    services=[]
    def visit(address,args,result):
        native.append(dict(address=address,arguments=[v&0xFFFFFFFF for v in args],result=result&0xFFFFFFFF,before=snapshot()))
    def provider(address,args,slot=None):
        result=[0,127,128,255,0x1234ABCD,0x80000000,0xFFFFFFFF][(action+mode+len(services))%7]
        changed=bytearray(state[ACT_TABLE])
        struct.pack_into('<h',changed,action*40+12,[-32768,-1,0,32767][mode%4])
        effects=[(ACT_TABLE,bytes(changed))]
        if slot is not None and slot<2 and action&1:
            new=bytearray(state[descriptors])
            new[(slot+1)*0x100+0xAC]=0 if new[(slot+1)*0x100+0xAC]else 1
            effects.append((descriptors,bytes(new)))
        services.append(dict(address=address,arguments=[v&0xFFFFFFFF for v in args],result=result,effects=effects,before=snapshot()))
        for a,b in effects:
            state[a][:]=b
        return result
    visit(ACTION,[action],ACT_TABLE+action*40)
    visit(MAP,[fieldword],selector)
    visit(BYTE,[fieldword],raw)
    visit(FIND,[fieldword],index)
    result=0xFFFFFFFF
    if selector>=0:
        visit(LOOKUP,[side,0],actors)
        for i in range(3):
            allowed=state[actors][i*0x440+0x31C]!=0 and state[actors][i*0x440+0x1FF]==0 and state[descriptors][i*0x100+0xAC]==0
            visit(ELIGIBLE,[actors+i*0x440],int(allowed))
            if allowed:
                value=provider(TARGET,[fieldword,actors+i*0x440,selector],i)&255
                result=(value if value<128 else value-256)&0xFFFFFFFF
    else:
        visit(COPY,[copyindex,0x0301FF00-36],copyaddress)
        scaled=s32(words[2]<<3)
        quotient=abs(scaled)//10*(-1 if scaled<0 else 1)
        value=provider(FALLBACK,[fieldword,words[0],words[1],quotient,side])&255
        result=(value if value<128 else value-256)&0xFFFFFFFF
    return initial,snapshot(),services,native,result
