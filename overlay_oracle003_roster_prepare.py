import struct
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3
from overlay_oracle003_record_copy import generated


from overlay_oracle003_main_dispatch import seed_main_dispatch003,main_dispatch_call003,assert_main_dispatch003


def seed_roster_prepare003(engine,address,vector):
    if address!=0x021DB290:return seed_main_dispatch003(engine,address,vector)
    state={'vector':vector,'primary':vector%64,'alternate':vector*17%64,'sources':{},'targets':{},'computed':{},'arrays':[],'queries':0,'a':vector%3,'b':vector//3%2,'c':vector//6%3,'d':vector//18%3,'e':vector//54%3}
    for i in range(12):
        p=0x03006000+i*256;record=bytearray(engine.mem_read(p,132));identifier=0x80000000+i if i<6 or state['alternate']>>(i-6)&1 else 0
        struct.pack_into('<IhB',record,20,identifier,[-32768,-1,0,1,32767][(vector+i)%5],(vector*17+i)&255);engine.mem_write(p,bytes(record));state['sources'][p]=bytes(record)
        target=0x03008000+i*512;state['targets'][target]=bytes(engine.mem_read(target,512))
    state['callbacks']={0x02008E0C:'func_02008e0c',0x0207B460:'func_0207b460',0x0207B1C4:'func_0207b1c4',0x0207C078:'func_0207c078'}
    return state


def roster_prepare_call003(engine,address,name,value,state):
    if address!=0x021DB290:return main_dispatch_call003(engine,address,name,value,state)
    args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]];index=args[0]
    if name=='func_020c361c':return state['a']
    if name=='func_020c363c':return state['b']
    if name=='func_020c365c':state['queries']+=1;return state['c'] if state['queries']==1 else state['d']
    if name=='func_020c369c':return state['e']
    getters={'func_02062a50':0,'func_02062a88':3,'func_020c3838':6,'func_020c3914':9}
    targets={'func_020649ac':0,'func_020649d4':3,'func_020649c0':6,'func_020649e8':9}
    if name in getters:
        if index not in range(3):raise ValueError('Roster preparation record index differs')
        slot=getters[name]+index
        return 0x03006000+slot*256 if slot>=6 or state['primary']>>slot&1 else 0
    if name in targets:
        if index not in range(3):raise ValueError('Roster preparation destination index differs')
        return 0x03008000+(targets[name]+index)*512
    if name in {'func_020c36b8','func_020c3724'}:state['arrays'].append((name,bytes(engine.mem_read(index,12))))
    if name=='func_0207b460':
        source=args[2]-122;target=args[3]-74
        if source not in state['sources'] or target not in state['targets']:raise ValueError('Roster derived-field source/destination ownership differs')
        record=state['sources'][source];species,variant,family,stats,extra=generated(record)
        if args[:2]!=[species&0xFFFFFFFF,variant]:raise ValueError('Roster derived-field signed identifier/variant differs')
        state['computed'][target]=source;engine.mem_write(target+74,family)
    if name=='func_0207b1c4':
        source=args[0]-122;target=args[1]-74
        if state['computed'].get(target)!=source or args[2]!=target+12:raise ValueError('Roster derived-stat pointer propagation differs')
        species,variant,family,stats,extra=generated(state['sources'][source])
        if bytes(engine.mem_read(target+74,64))!=family:raise ValueError('Roster derived-family intermediate differs')
        engine.mem_write(target+12,stats)
    if name=='func_0207c078':
        target=args[2]-74;source=state['computed'].get(target)
        if source is None or args[3]!=target+138:raise ValueError('Roster derived-attribute pointers differ')
        species,variant,family,stats,extra=generated(state['sources'][source])
        if args[:2]!=[species&0xFFFFFFFF,variant] or bytes(engine.mem_read(target+74,64))!=family:raise ValueError('Roster derived-attribute intermediate/identifier differs')
        engine.mem_write(target+138,extra)
    return value


def converted(record,before):
    result=bytearray(before)
    if record is None:struct.pack_into('<h',result,46,-1);struct.pack_into('<I',result,0,0xFFFFFFFF);return bytes(result)
    species,variant,family,stats,extra=generated(record)
    result[182:202]=record[:20];struct.pack_into('<i',result,0,species);result[46:48]=record[24:26];result[48]=variant;result[4:8]=record[20:24];result[177]=record[27];result[178]=record[30];result[175]=record[28]
    result[214:224]=record[122:132];result[224:282]=record[64:122];result[284:316]=record[32:64];result[74:138]=family;result[12:44]=stats;result[138:170]=extra
    return bytes(result)


def assert_roster_prepare003(engine,address,args,calls,state):
    if address!=0x021DB290:return assert_main_dispatch003(engine,address,args,calls,state)
    flags={1:0x800000,2:0x1000000}.get(state['a'],0)|(0x2000000 if state['b']==1 else 0)|(0x4000000 if state['c']==2 else 1 if state['d']==1 else 0)|{1:0x8000000,2:0x10000000}.get(state['e'],0)|0x46
    parameters={'func_020443d4':[5],'func_020652dc':[104],'func_02065304':[0],'func_02065630':[0],'func_02065648':[45],'func_0206532c':[3],'func_020445c4':[1],'func_0206534c':[0xFFFFFFFF],'func_020652c4':[0],'func_020656d0':[1],'func_020443c4':[12]}
    if [c['args'][0] for c in calls if c['name']=='func_02044454']!=[0,flags] or state['queries']!=(1 if state['c']==2 else 2):raise ValueError('Roster rule flags or repeated mode query differs')
    for c in calls:
        if c['name'] in parameters and c['args'][:len(parameters[c['name']])]!=parameters[c['name']]:raise ValueError('Roster battle/setup parameters differ')
    expectedArrays=[];pairs=[]
    for group,setter in [(0,'func_020c36b8'),(1,'func_020c3724')]:
        expectedArrays.append((setter,bytes(12)));ids=[]
        for i in range(3):
            slot=group*3+i;source=0x03006000+slot*256;ids.append(int.from_bytes(state['sources'][source][20:24],'little') if state['primary']>>slot&1 else 0)
        expectedArrays.append((setter,struct.pack('<3I',*ids)))
    if state['arrays']!=expectedArrays:raise ValueError('Roster original identifier list initialization/capture differs')
    for i in range(12):
        target=0x03008000+i*512;source=0x03006000+i*256;present=bool(state['primary']>>i&1) if i<6 else bool(state['alternate']>>(i-6)&1)
        record=state['sources'][source] if present else None;pairs.append([target,source if present else 0])
        if bytes(engine.mem_read(target,512))!=converted(record,state['targets'][target]):raise ValueError('Roster complete converted record/destination padding differs')
    if [c['args'][:2] for c in calls if c['name']=='func_ov003_021db4a8']!=pairs:raise ValueError('Roster primary/secondary/alternate conversion order differs')
    if any(bytes(engine.mem_read(p,132))!=record for p,record in state['sources'].items()):raise ValueError('Roster preparation changed an original fixture record')
    clearCalls=[c for c in calls if c['name']=='func_02008d78']
    if len(clearCalls)!=2 or any(c['args'][1:3]!=[0,12] for c in clearCalls):raise ValueError('Roster complete identifier-array native clear differs')
