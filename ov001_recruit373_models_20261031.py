import random
import struct
import ov001_recruit364_models_20261031 as OLD
from ov001_recruit364_models_20261031 import BASE,RECORDS,WINDOW,INPUT,NAME,ACTOR_BASES,PARAMS,IDS,STATE,TEMPLATE,CONTEXT,ROWS,FOOTER,read,put,category


def setup(obj,recipe):
    OLD.setup(obj,recipe)
    obj.u.mem_write(0x020DDD40,bytes([0]))
    for index in range(6):
        actor=ACTOR_BASES[index//3]+0x440*(index%3)
        param=PARAMS+0x200*index
        for offset,value in[(0x1EC,[-32768,-1,0,100,9998,32767][index]),(0x1EE,[100,-1,32767,0,9998,-32768][index]),(0x1F0,[-32768,-1,1,100,9999,32767][index]),(0x1F2,[100,-1,9999,32767,9998,-32768][index]),(0x21C,[-20,0,1,30,32767,-32768][index]),(0x21E,[30,0,-1,-20,-32768,32767][index])]:obj.u.mem_write(actor+offset,(value&65535).to_bytes(2,'little'))
        if recipe.get('mpValues'):obj.u.mem_write(actor+0x1F2,(recipe['mpValues'][index]&65535).to_bytes(2,'little'))
        obj.u.mem_write(actor+0x1FD,bytes([1+index]))
        obj.u.mem_write(param+0x46,bytes([128,129,139,0])+bytes(60))
        if recipe.get('standalone'):
            obj.u.mem_write(actor+0x31C,bytes([recipe['enabled'][index]]))
            obj.u.mem_write(actor+0x1FF,bytes([recipe['blocked'][index]]))
            obj.word(param,recipe['actorUids'][index])


def refresh_image(image):
    valid={read(image,RECORDS-BASE+132*i+20,4)for i in range(100)}-{0}
    groups={read(image,0x021BD540-BASE+4*i,4)for i in range(6)}&valid
    refreshed=[]
    for index in range(6):
        actor=ACTOR_BASES[index//3]+0x440*(index%3)-BASE
        if not image[actor+0x31C]:continue
        parameter=read(image,actor+0x1E8,4)-BASE
        ident=read(image,parameter,4)
        if ident in groups:continue
        image[actor+0x1FD]=0
        image[actor+0x1FF]=0
        values=list(image[parameter+0x46:parameter+0x86])
        if 0 in values:values=values[:values.index(0)]
        weights=[5,10,15,20,22,24,26,28,30,35]
        bonus=[sum(values.count(start+i)*weight for i,weight in enumerate(weights))for start in[128,138]]
        maximum=[min(min(read(image,actor+base_offset,2,True)+bonus[i],9999)+read(image,actor+extra_offset,2,True),9999)for i,(base_offset,extra_offset)in enumerate([(0x1EC,0x21C),(0x1EE,0x21E)])]
        put(image,actor+0x1F0,2,max(0,maximum[0]))
        old_mp=read(image,actor+0x1F2,2,True)
        if old_mp<10000:
            candidate=old_mp+maximum[1]
            value=0 if candidate<0 else min(candidate,maximum[1])
            put(image,actor+0x1F2,2,value)
        refreshed.append(dict(index=index,actorUid=ident,maximumHalfwords=maximum,oldMp=old_mp,newMp=read(image,actor+0x1F2,2,True)))
    return refreshed


def standalone_recipes():
    source=OLD.recipes()[0]
    results=[]
    for index,(enabled,active,reserve)in enumerate([([0]*6,[],[]),([1]*6,[],[]),([255]*6,[101],[200]),([1,0,1,0,1,0],[101,103],[105]),([1]*6,[101,103,105],[200]),([1]*6,[999],[0])]):
        results.append(dict(source,seed=373000+index,standalone=True,enabled=enabled,blocked=[0,1,255,1,255,0],actorUids=[101,103,105,200,0,999],active=active,reserve=reserve))
    for value in[9998,9999,10000,10001]:results.append(dict(results[1],seed=373100+value,mpValues=[value]*6))
    return results


def compare_nonstack(before,after,expected):
    lo,hi=0x027E0000-BASE,0x027F1000-BASE
    if after[:lo]!=expected[:lo]or after[hi:]!=expected[hi:]:
        address=next(hex(BASE+i)for i,(a,b)in enumerate(zip(after,expected))if a!=b and not lo<=i<hi)
        raise ValueError(('Recruit373 independent nonstack RAM differs',address))


def connected_model(before,after,value,provided,assets,recipe):
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
        for row_index,ident in enumerate(IDS):expected[RECORDS-BASE+132*row_index:RECORDS-BASE+132*(row_index+1)]=rows[ident]
        raw_groups=active+[0]*(3-len(active))+reserve+[0]*(3-len(reserve))
        expected[0x021BD540-BASE:0x021BD558-BASE]=struct.pack('<6I',*raw_groups)
        refresh_image(expected)
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


def eligibility_model(image):
    selected=[]
    for y in range(3):
        for index in range(15):
            row=ROWS-BASE+16*index
            if image[row+9]and image[row+11]==0 and image[row+8]==0 and image[row+7]==y:selected.append(read(image,row,4))
    if len(selected)>3:raise ValueError('Recruit373 original caller list capacity3 exceeded')
    required=read(image,STATE-BASE+0x1C,4)
    for ident in selected:
        for index in range(6):
            actor=ACTOR_BASES[index//3]+0x440*(index%3)-BASE
            parameter=read(image,actor+0x1E8,4)-BASE
            if read(image,parameter,4)==ident:
                if image[actor+0x31C]and image[actor+0x1FF]==0 and image[parameter+0xAC]==0:return 1
                break
        if ident==required:return 1
    return 0


def eligibility_recipes():
    results=[]
    original=OLD.recipes()[22]
    for ids in[[],[0],[999],[101],[200],[0,101,0],[103,105],[999,999,999]]:
        for enabled,blocked,parameter in[(0,0,0),(1,0,0),(255,1,0),(1,0,255)]:
            results.append(dict(original,seed=374000+len(results),selectedUids=ids,actorEnabled=enabled,actorBlocked=blocked,parameterBlocked=parameter))
    return results
