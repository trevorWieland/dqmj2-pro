import random
import struct
from ov001_recruit364_fixture_20261031 import STATE,TEMPLATE,CONTEXT,ROWS,FOOTER
BASE,RECORDS,WINDOW,INPUT,NAME=0x02000000,0x021BD674,0x0223A7FC,0x020EDEB8,0x021C6C6C
ACTOR_BASES=[0x02236F6C,0x022355EC]
PARAMS=0x02360000
IDS=[101,103,105,200]

def read(raw,offset,size,signed=False):return int.from_bytes(raw[offset:offset+size],'little',signed=signed)

def put(raw,offset,size,value):raw[offset:offset+size]=(value&((1<<(8*size))-1)).to_bytes(size,'little')

def category(assets,species):return((read(assets['EnmyKindTbl.bin'],8+100*species+4,2)>>8)&15)//3

def recipes():
    cases=[]
    for active in[[],[101],[103],[105],[101,103],[101,103,105],[200]]:
        for child in[367,14,31]:
            cases.append(dict(phase=0,active=active,childSpecies=child,ready=1))
    cases.append(dict(phase=0,ready=0))
    for drag in[False,True]:
        for action in[0,1,2,3]:
            for key in[0,1,2,0x800]:cases.append(dict(phase=1,drag=drag,action=action,key=key))
    for selected in[0,1,2,3]:
        for confirm in[0,2]:cases.append(dict(phase=1,key=1,selection=selected,confirm=confirm))
    for group in[0,1,2,255,3]:cases.append(dict(phase=1,key=0x800,group=group))
    for flags in[0,1,2,0x800,3,0x803]:
        for response in[0,1,255]:cases.append(dict(phase=3,key=flags,response=response))
    cases.extend(dict(phase=p)for p in[-1,2,4,127])
    defaults=dict(active=[101],reserve=[105],childSpecies=367,ready=1,drag=False,action=0,key=0,alternate=0,selection=0,confirm=0,group=0,fallback=0,response=0,selectedUids=[101],selectedReserve=[105],actorEnabled=1,actorBlocked=0,parameterBlocked=0,candidate=101,previous=0,ioResult=0)
    results=[]
    for index,case in enumerate(cases):
        recipe=dict(defaults,**case,seed=364000+index)
        if recipe['phase']==1:
            recipe['selectedUids']=[[101],[200],[],[103,105]][index%4]
            recipe['actorEnabled']=[0,1,255][index%3]
            recipe['actorBlocked']=1 if index%5==0 else 0
            recipe['parameterBlocked']=1 if index%7==0 else 0
            recipe['fallback']=1 if index%6==0 else 0
            recipe['candidate']=[0,101,200,999][index%4]
            recipe['previous']=recipe['candidate']if index%2 else 0
            recipe['alternate']=1 if index%3==0 else recipe['alternate']
            recipe['ioResult']=[0,1,0xFFFFFFFF][index%3]
        results.append(recipe)
    for offset,(drag,candidate,previous)in enumerate([(True,101,0),(True,103,0),(True,105,0),(True,200,0),(True,999,0),(True,0,101),(True,101,101),(False,999,101)]):
        results.append(dict(defaults,phase=1,drag=drag,candidate=candidate,previous=previous,seed=364200+offset))
    return results

def setup(obj,recipe):
    rng=random.Random(recipe['seed'])
    state=bytearray(rng.randbytes(0x34))
    put(state,0x14,4,recipe['phase'])
    put(state,0x1C,4,200)
    put(state,0x18,4,103)
    obj.u.mem_write(STATE,bytes(state))
    template=bytearray(rng.randbytes(132))
    put(template,0x64,2,recipe['childSpecies'])
    template[0x67]=1
    obj.u.mem_write(TEMPLATE,bytes(template))
    obj.u.mem_write(RECORDS,bytes(13200))
    for index,ident in enumerate(IDS):
        row=bytearray(rng.randbytes(132))
        put(row,20,4,ident)
        put(row,24,2,[367,14,31,recipe['childSpecies']][index])
        obj.u.mem_write(RECORDS+132*index,bytes(row))
    obj.u.mem_write(0x021BD540,struct.pack('<6I',*(recipe['active']+[0]*(3-len(recipe['active']))+recipe['reserve']+[0]*(3-len(recipe['reserve'])))))
    obj.u.mem_write(CONTEXT,bytes(0x100))
    obj.u.mem_write(CONTEXT+0x1E,bytes([14 if recipe['drag']else 255,255]))
    obj.word(CONTEXT+0x14,recipe['previous'])
    obj.word(CONTEXT+0x18,0xA5A55A5A)
    obj.u.mem_write(FOOTER,bytes([recipe['group'],0,0,0,recipe['fallback'],0,1]))
    obj.u.mem_write(ROWS,bytes(240))
    for group,key in[(0,'selectedUids'),(1,'selectedReserve')]:
        if len(recipe[key])>3:raise ValueError('Recruit364 three-word native list capacity exceeded')
        for index,ident in enumerate(recipe[key]):
            pos=ROWS+16*(3*group+index)
            obj.word(pos,ident)
            obj.u.mem_write(pos+6,bytes([0,index,group,1,1,0,1]))
    obj.word(ROWS+14*16,recipe['candidate'])
    obj.u.mem_write(INPUT,bytes(8))
    obj.u.mem_write(INPUT+2,struct.pack('<H',recipe['key']))
    obj.u.mem_write(NAME,rng.randbytes(20))
    obj.word(0x021C0EE0,(rng.getrandbits(32)&~0xC000)|[0,0x4000,0x8000,0xC000][recipe['seed']%4])
    obj.word(0x021C0EE8,rng.getrandbits(32))
    obj.word(0x021C0E28,rng.getrandbits(32))
    obj.word(WINDOW,recipe['response'])
    for index in range(6):
        actor=ACTOR_BASES[index//3]+0x440*(index%3)
        param=PARAMS+0x200*index
        obj.u.mem_write(actor,bytes(0x440))
        obj.u.mem_write(param,bytes(0x200))
        obj.word(actor+0x1E8,param)
        obj.word(param,[101,103,105,200,0,0][index])
        obj.u.mem_write(actor+0x31C,bytes([recipe['actorEnabled']if index<4 else 0]))
        obj.u.mem_write(actor+0x1FF,bytes([recipe['actorBlocked']]))
        obj.u.mem_write(param+0xAC,bytes([recipe['parameterBlocked']]))
    obj.recipe=recipe


def model(before,after,value,provided,assets,recipe):
    expected=bytearray(before)
    state=STATE-BASE
    phase=recipe['phase']
    active=list(recipe['active'])
    reserve=list(recipe['reserve'])
    rows={ident:bytearray(before[RECORDS-BASE+132*i:RECORDS-BASE+132*(i+1)])for i,ident in enumerate(IDS)}
    events=[]
    next_state=1
    rebuilds=0
    flags=recipe['key']
    actor_good=bool(recipe['actorEnabled'])and not recipe['actorBlocked']and not recipe['parameterBlocked']
    eligible=any(ident==200 or ident in IDS and actor_good for ident in recipe['selectedUids'])
    selected=(recipe['selectedUids']+recipe['selectedReserve']+[0])[0]
    def add(address,args):events.append((hex(address),args))
    def pointer(ident):return RECORDS+132*IDS.index(ident)if ident in IDS else 0
    def actor(ident):
        if ident not in IDS:return 0
        index=IDS.index(ident)
        return ACTOR_BASES[index//3]+0x440*(index%3)
    def normalize(values):
        result=[]
        for ident in values:
            if ident in IDS and ident not in result:result.append(ident)
        return result[:3]
    def rebuild():
        nonlocal active,reserve,rebuilds
        active=normalize(recipe['selectedUids'])
        reserve=normalize(recipe['selectedReserve'])
        keep=set(recipe['selectedUids']+recipe['selectedReserve'])
        for ident,row in rows.items():
            if ident not in keep:row[0x31]=0
        if reserve:
            for mask in[0x4000,0x8000]:
                primary=0x021C0EE0-BASE
                old=read(expected,primary,4)
                put(expected,primary,4,old|mask)
                if not old&mask:
                    secondary=0x021C0EE8-BASE
                    dirty=0x021C0E28-BASE
                    put(expected,secondary,4,read(expected,secondary,4)|mask)
                    put(expected,dirty,4,read(expected,dirty,4)|0x1000)
        rebuilds+=1
    def dialog():
        add(0x0220A3D8,[5,6,44])
        add(0x0220A3F0,[255,0,0])
        add(0x0220A408,[])
    if phase==0:
        add(0x0207E874,[])
        if recipe['ready']:
            rows[200][:20]=before[NAME-BASE:NAME-BASE+20]
            add(0x0206DE44,[1])
            add(0x0206DE64,[1])
            weight=sum(category(assets,read(rows[ident],24,2,True))+1 for ident in active)
            required=category(assets,recipe['childSpecies'])+1
            if 3-weight>=required:
                if 200 not in active and len(active)<3:active.append(200)
                next_state=6
            else:
                next_state=2
                add(0x02041538,[1,2,16])
    if phase==1:
        add(0x0206BE08,[0,int(eligible and not recipe['fallback']and not recipe['drag'])])
        add(0x0206A0FC,[1])
        if recipe['action']==1:
            rebuild()
            add(0x02209B4C,[])
            next_state=6
        elif recipe['action']==2:
            put(expected,state+0x18,4,selected)
            next_state=2
        else:
            add(0x0206A49C,[])
            if recipe['alternate']==1:
                dialog()
                next_state=3
        if not recipe['drag']:
            add(0x0206940C,[])
            if flags&1:
                add(0x020698F4,[1])
                if recipe['selection']==0:
                    add(0x0206A04C,[])
                    if recipe['confirm']==2:
                        dialog()
                        next_state=3
                elif recipe['selection']==1:
                    if eligible:
                        rebuild()
                        add(0x02209B4C,[])
                        next_state=6
                elif recipe['selection']==2:
                    put(expected,state+0x18,4,selected)
                    next_state=2
            elif flags&2:add(0x0206A06C,[1])
            elif flags&0x800:
                group=recipe['group']
                if group in[0,1,2,255]:
                    index=3 if group==255 else group
                    add(0x0220A3F0,[5,2,60+index])
                    add(0x0220A3D8,[5,7,57+index])
                next_state=3
                add(0x02068F60,[0])
        candidate=recipe['candidate']if recipe['drag']else 0
        changed=candidate if candidate!=recipe['previous']else 0
        put(expected,CONTEXT-BASE+0x14,4,candidate)
        put(expected,CONTEXT-BASE+0x18,4,candidate)
        add(0x0206DCD0,[pointer(candidate)])
        if changed:
            target=actor(changed)
            add(0x0206DE1C,[1,target+0x1EC]if target else[0,0])
    if phase==3:
        add(0x020491F8,[WINDOW])
        if flags&1:
            if recipe['response']:next_state=2
            else:
                add(0x02047FF0,[pointer(103),20,0])
                next_state=5
        elif flags&2:next_state=2
        elif flags&0x800:next_state=3
    if phase!=0:
        add(0x0220B21C,[WINDOW])
        add(0x0220A97C,[WINDOW])
    for index,ident in enumerate(IDS):expected[RECORDS-BASE+132*index:RECORDS-BASE+132*(index+1)]=rows[ident]
    groups=active+[0]*(3-len(active))+reserve+[0]*(3-len(reserve))
    expected[0x021BD540-BASE:0x021BD558-BASE]=struct.pack('<6I',*groups)
    if len(provided)!=len(events):raise ValueError(('Recruit364 provider event count differs',recipe,len(provided),events))
    returns={0x0207E874:recipe['ready'],0x0206A0FC:recipe['action'],0x0206A49C:recipe['alternate'],0x020698F4:recipe['selection'],0x0206A04C:recipe['confirm']}
    for actual,(address,args)in zip(provided,events):
        if actual['entry']!=address or actual['arguments']!=args:raise ValueError(('Recruit364 independent provider contract differs',address,actual,args))
        want=returns.get(int(address,0),recipe['ioResult'])
        if actual['providedReturnWord']!=want:raise ValueError('Recruit364 provider result differs')
    lo,hi=0x027E0000-BASE,0x027F1000-BASE
    if after[:lo]!=expected[:lo]or after[hi:]!=expected[hi:]or value!=next_state:
        bad=next((hex(BASE+i)for i,(a,b)in enumerate(zip(after,expected))if a!=b and not lo<=i<hi),None)
        raise ValueError(('Recruit364 independent complete nonstack RAM/return model differs',recipe,bad,value,next_state))
    return dict(nextState=value,eligibility=eligible,active=active,reserve=reserve,partyRebuilds=rebuilds,providedCalls=len(events),candidateUid=recipe['candidate']if recipe['drag']else 0,trackerExpectedWord=(recipe['candidate']if recipe['candidate']!=recipe['previous']else 0)if recipe['drag']else 0,zeroTrackerReturnDespitePreviousChange=phase==1 and not recipe['drag']and recipe['previous']!=0,rawRecord33Preserved=all(before[RECORDS-BASE+132*i+0x33]==after[RECORDS-BASE+132*i+0x33]for i in range(4)),fullIndependentNonstackRam=True)
