import random
import struct
from ov001_query265_models_20261031 import action_table
A,B=0x0222C54C,0x0222C728
STATE,ACT_PTR,ACT_TABLE=0x022497E8,0x021C6748,0x02300000
ACTORS,DESC,UI_GLOBAL,UI_OBJECT=0x022355EC,0x02310000,0x02238F58,0x02305000
RULE,RNG_STATE=0x020F69E4,0x020F6044
BASES=[0x02236F6C,0x022362AC,0x022355EC,0x02237C2C]
ACTION,LOOKUP,ELIGIBLE=0x0207AFEC,0x021DB438,0x021DB8D0
SIDE_MAP,UI_APPLY,UI_CLEAR=0x021F1414,0x021F1438,0x021F14A4
QUANTITY,CURRENT_HP,CURRENT_MP,CHANGE_HP,CHANGE_MP=0x0222C51C,0x021DBD24,0x021DBD30,0x021DB718,0x021DB7CC
MAX_HP,MAX_MP,C700,RNG,DIVIDE,FLAG=0x021DBCBC,0x021DBCF0,0x0222C700,0x0203D294,0x02026350,0x02044424
NATIVE={ACTION:20,LOOKUP:124,ELIGIBLE:72,SIDE_MAP:36,UI_APPLY:108,UI_CLEAR:28,QUANTITY:48,CURRENT_HP:12,CURRENT_MP:12,CHANGE_HP:112,CHANGE_MP:104,C700:40,RNG:72,FLAG:48}
SPECS={A:dict(bytes=436,instructions=432,counter=4,phase=5,phases=[0,5,10,20,100,255]),B:dict(bytes=312,instructions=308,counter=2,phase=3,phases=[0,10,50,100,255])}

def s32(v):
    return (v&0xFFFFFFFF)-0x100000000 if v&0x80000000 else v&0xFFFFFFFF

def recipes(address):
    return [dict(seed=293000+address+phase*257+counter,phase=phase,counter=counter,side=[0,1,2,3,4,255][counter%6],mask=counter//6%8)for phase in SPECS[address]['phases']for counter in range(256)]

def construct(address,recipe):
    rng=random.Random(recipe['seed'])
    spec=SPECS[address]
    actors=bytearray(rng.randbytes(0x3300))
    descriptors=bytearray(rng.randbytes(0x4000))
    state={STATE:bytearray(rng.randbytes(16)),ACT_PTR:bytearray(struct.pack('<I',ACT_TABLE)),ACT_TABLE:bytearray(action_table()[8:]),ACTORS:actors,DESC:descriptors,UI_GLOBAL:bytearray(struct.pack('<IIII',0,UI_OBJECT,0,0)),UI_OBJECT:bytearray(rng.randbytes(64)),RULE:bytearray(struct.pack('<I',rng.getrandbits(32)&~0x40000000|((recipe['counter']&1)<<30))),RNG_STATE:bytearray(struct.pack('<I',rng.getrandbits(32)))}
    state[STATE][0]=recipe['side']
    state[STATE][spec['phase']]=recipe['phase']
    state[STATE][spec['counter']]=recipe['counter']
    hpmax={}
    mpmax={}
    for side,base in enumerate(BASES):
        for slot in range(3):
            actor=base+slot*0x440
            offset=actor-ACTORS
            descriptor=DESC+side*0x1000+slot*0x100
            enabled=bool(recipe['mask']&(1<<slot))
            struct.pack_into('<I',actors,offset+0x1E8,descriptor)
            actors[offset+0x31C]=[1,2,255][slot]if enabled or slot!=0 else 0
            actors[offset+0x1FF]=0 if enabled or slot!=1 else 255
            descriptors[descriptor-DESC+0xAC]=0 if enabled or slot!=2 else 127
            actors[offset+0x31E]=(recipe['counter']+side+slot)%2
            struct.pack_into('<h',actors,offset+0x1F0,[-32768,0,1,7,500,9999,32767][(recipe['counter']+side+slot)%7])
            struct.pack_into('<h',actors,offset+0x1F2,[-32768,0,1,7,500,9999,10000,32767][(recipe['counter']+side+slot)%8])
            hpmax[actor]=[0,1,15,16,31,128,9999][(recipe['counter']+side+slot)%7]
            mpmax[actor]=[0,1,9,10,11,100,9999][(recipe['counter']+side+slot)%7]
    def snapshot():
        return [(a,bytes(b))for a,b in state.items()]
    def read(a,n):
        for base,b in state.items():
            if base<=a and a+n<=base+len(b):
                return bytes(b[a-base:a-base+n])
        raise ValueError('Family293 model read outside state')
    def write(a,b):
        for base,data in state.items():
            if base<=a and a+len(b)<=base+len(data):
                data[a-base:a-base+len(b)]=b
                return
        raise ValueError('Family293 model write outside state')
    def half(a):
        return struct.unpack('<h',read(a,2))[0]
    def word(a):
        return struct.unpack('<I',read(a,4))[0]
    initial=snapshot()
    native=[]
    services=[]
    def visit(entry,args,result,remainder=None):
        event=dict(address=entry,arguments=[v&0xFFFFFFFF for v in args],result=result&0xFFFFFFFF,before=snapshot())
        if remainder is not None:
            event['remainder']=remainder
        native.append(event)
    def provider(entry,args,result=None,actor=None):
        effects=[]
        if result is None:
            result=rng.getrandbits(32)
        if entry not in[MAX_HP,MAX_MP]:
            view=bytearray(state[STATE])
            view[0]=[0,1,2,3,4,255][(recipe['counter']+len(services))%6]
            view[15]=rng.getrandbits(8)
            if entry==0x0222C024:
                view[3]=[0,10,50,100,255][recipe['counter']%5]
            effects.append((STATE,bytes(view)))
            if actor is not None and entry==0x021D9494:
                current=[0,1,100,32767][recipe['counter']%4]
                effects.append((actor+(0x1F0 if address==A else 0x1F2),struct.pack('<h',current)))
        event=dict(address=entry,arguments=[v&0xFFFFFFFF for v in args],result=result&0xFFFFFFFF,effects=effects,before=snapshot())
        services.append(event)
        for a,b in effects:
            write(a,b)
        return result&0xFFFFFFFF
    def stat(entry,actor):
        return provider(entry,[actor],hpmax[actor]if entry==MAX_HP else mpmax[actor])
    def lookup(slot):
        side=state[STATE][0]
        actor=BASES[side]+slot*0x440 if side<4 else 0
        visit(LOOKUP,[side,slot],actor)
        valid=bool(actor and read(actor+0x31C,1)[0]and not read(actor+0x1FF,1)[0]and not read(word(actor+0x1E8)+0xAC,1)[0])
        visit(ELIGIBLE,[actor],int(valid))
        return actor if valid else 0
    def quantity(actor):
        maximum=hpmax[actor]
        current=half(actor+0x1F0)
        amount=maximum>>4 if current-(maximum>>4)>0 else current-1
        visit(QUANTITY,[actor],amount)
        stat(MAX_HP,actor)
        visit(CURRENT_HP,[actor],current)
        return amount
    def hp_change(actor,amount):
        old=half(actor+0x1F0)
        blocked=bool(word(RULE)&0x40000000 and read(actor+0x31E,1)[0]==1)
        value=max(0,old+amount)
        if value>hpmax[actor]:
            value=hpmax[actor]
        result=0 if blocked else value-old
        visit(CHANGE_HP,[actor,amount],result)
        visit(FLAG,[0x40000000],int(bool(word(RULE)&0x40000000)))
        if not blocked:
            if old+amount>=0:
                stat(MAX_HP,actor)
                if old+amount>hpmax[actor]:
                    stat(MAX_HP,actor)
            write(actor+0x1F0,struct.pack('<h',value))
        return result
    def random_amount(actor):
        maximum=mpmax[actor]
        bound=maximum//10
        after=(word(RNG_STATE)*0x41C64E6D+0x3039)&0xFFFFFFFF
        drawn=(after>>16)%bound if bound>0 else 0
        visit(C700,[actor],drawn+1)
        stat(MAX_MP,actor)
        visit(RNG,[bound],drawn)
        write(RNG_STATE,struct.pack('<I',after))
        if bound>0:
            visit(DIVIDE,[after>>16,bound],(after>>16)//bound,drawn)
        return drawn+1
    def mp_change(actor,amount):
        old=half(actor+0x1F2)
        value=min(max(0,old+amount),mpmax[actor])
        result=amount if old>=10000 else value-old
        visit(CHANGE_MP,[actor,amount],result)
        visit(CURRENT_MP,[actor],old)
        if old<10000:
            if old+amount>=0:
                stat(MAX_MP,actor)
                if old+amount>mpmax[actor]:
                    stat(MAX_MP,actor)
            write(actor+0x1F2,struct.pack('<h',value))
        return result
    if address==A:
        visit(ACTION,[215],ACT_TABLE+215*40)
        if state[STATE][5]==0:
            provider(0x021D7F54,[state[STATE][0]])
            provider(0x021F1354,[1,0,50,1])
            side=state[STATE][0]
            mapped=side if side<2 else 2
            visit(SIDE_MAP,[side],mapped)
            result=rng.getrandbits(32)
            visit(UI_APPLY,[mapped],result)
            provider(0x02085320,[UI_OBJECT,0,4+mapped],result)
            state[STATE][4]=0
            state[STATE][5]=5
        if state[STATE][5]==5:
            state[STATE][4]=(state[STATE][4]+1)&255
            if state[STATE][4]>30:
                state[STATE][5]=10
        if state[STATE][5]==10:
            flags=word(UI_OBJECT+24)&~4
            visit(UI_CLEAR,[],flags)
            write(UI_OBJECT+24,struct.pack('<I',flags))
            positive=False
            for slot in range(3):
                actor=lookup(slot)
                if actor:
                    amount=quantity(actor)
                    if amount>0:
                        provider(0x021D9494,[actor,4,1],actor=actor)
                        hp_change(actor,-amount)
                        provider(0x022024D4,[state[STATE][0],slot,amount])
                        positive=True
                    provider(0x021EE78C,[actor,amount,-1,1,0])
            provider(0x021F949C,[238 if positive else 242,1])
            state[STATE][4]=0
            state[STATE][5]=20
        elif state[STATE][5]==20:
            state[STATE][4]=(state[STATE][4]+1)&255
            if state[STATE][4]>30:
                state[STATE][5]=100
        if state[STATE][5]==100:
            state[STATE][5]=0
            state[STATE][1]=7
    else:
        if state[STATE][3]==0:
            result=provider(0x0222C024,[247,state[STATE][0],51],[0,1,0x80000000,0xFFFFFFFF][recipe['counter']%4])
            if result:
                state[STATE][3]=10
        if state[STATE][3]==10:
            for slot in range(3):
                actor=lookup(slot)
                if actor:
                    amount=random_amount(actor)
                    if amount>0:
                        provider(0x021D9494,[actor,0,0],actor=actor)
                        amount=mp_change(actor,amount)
                        provider(0x022024D4,[state[STATE][0],slot,-amount])
                    provider(0x021EE7D4,[actor,amount,2])
            state[STATE][2]=0
            state[STATE][3]=50
        if state[STATE][3]==50:
            state[STATE][2]=(state[STATE][2]+1)&255
            if state[STATE][2]>45:
                state[STATE][3]=100
        if state[STATE][3]==100:
            state[STATE][3]=0
            state[STATE][1]=7
    return initial,snapshot(),services,native,0
