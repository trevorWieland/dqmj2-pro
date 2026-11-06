import struct
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3

from overlay_oracle003_first_mode_input import seed_first_input003,first_input_arguments003,first_input_call003,assert_first_input003

FUNCTIONS={0x021DACEC,0x021DAD1C,0x021DADC4,0x021DAE50,0x021DAF7C,0x021DAF90}
ROOT=0x021E0690
GROUP=0x021E07A8
CONTEXT=0x021E06B8


def seed_first_mode003(engine,address,vector):
    if address not in FUNCTIONS:return seed_first_input003(engine,address,vector)
    engine.mem_write(ROOT+4,struct.pack('<I',0x0300D000 if address!=0x021DACEC or vector%2 else 0))
    engine.mem_write(ROOT+36,struct.pack('<I',[1,4,6,12,0,0xFFFFFFFF][vector%6]))
    phase=[0,1,2,3,4,5,6,7,99][vector%9];current=[0,4,12,0xFFFFFFFF][vector//36%4]
    engine.mem_write(GROUP+4,struct.pack('<2I',current,phase));engine.mem_write(CONTEXT,struct.pack('<I',[0,1,2,0xFFFFFFFF][vector%4]))
    return {'root':bytes(engine.mem_read(ROOT,40)),'group':bytes(engine.mem_read(GROUP,20)),'context':bytes(engine.mem_read(CONTEXT,240)),'phase':phase,'current':current,'fade':vector//9%2,'busy':vector//18%2,'heap':[0,2,0xFFFFFFFF][vector%3],'size':vector%65,'payload':bytes(engine.mem_read(0x0300C000,65)),'buffer':bytes(engine.mem_read(0x0300D000,2048)),'kind':vector%3,'updates':0,'choice':[34,33,0xFFFFFFFF,0][vector//4%4],'value':[0,1,0x80000000,0xFFFFFFFF][vector//16%4]}


def first_mode_arguments003(address,vector,args):
    first_input_arguments003(address,vector,args)
    if address==0x021DAD1C:args[:2]=[vector%3,vector//3%4]


def first_mode_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return first_input_call003(engine,address,name,value,state)
    args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]]
    if name=='func_0202a250':return state['heap']
    if name=='func_0203cc2c':
        if args[:2]!=[0x021E032C,state['heap']]:raise ValueError('First mode resource archive/heap differs')
        return 0x0300F000
    if name=='func_0204518c':
        if args[1:3]!=[0x0300F000,state['kind']]:raise ValueError('First mode replacement section identity differs')
        engine.mem_write(args[0],struct.pack('<2I',0x0300C000,state['size']))
    if name=='func_02048e74':
        if args[:2]!=[GROUP+4,0]:raise ValueError('First mode SDK state initializer differs')
        engine.mem_write(GROUP+4,bytes(16))
    if name=='func_02048fcc':
        if args[0]!=CONTEXT:raise ValueError('First mode original context getter forwarding differs')
        engine.mem_write(CONTEXT,bytes(240))
    if name=='func_02041944':return state['fade']
    if name=='func_02041814':return state['busy']
    if name in {'func_ov003_021db034','func_ov003_021db248'}:
        state['updates']^=0x100 if name=='func_ov003_021db034' else 0x200
        engine.mem_write(GROUP+4,struct.pack('<I',state['current']^state['updates']))
    if name=='func_020c35fc':return state['value']
    if name=='func_02062378':return state['choice']
    return value


def assert_first_mode003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_first_input003(engine,address,args,calls,state)
    root=bytearray(state['root']);group=bytearray(state['group']);context=bytearray(state['context']);expected=[]
    if address==0x021DACEC:
        pointer=int.from_bytes(root[4:8],'little')
        if pointer:
            expected=['func_0202a498'];root[4:8]=bytes(4)
            if calls[0]['args'][:2]!=[2,pointer]:raise ValueError('First mode cleanup allocation ownership differs')
    elif address==0x021DAD1C:
        expected=['func_0202a250','func_0203cc2c','func_0204518c','func_02008e0c','func_02045994','func_0202a498']
        for c in calls:
            values={'func_02008e0c':[0x0300C000,0x0300D000,state['size']],'func_02045994':[args[1],0x0300D000,0,2048],'func_0202a498':[state['heap'],0x0300F000]}
            if c['name'] in values and c['args'][:len(values[c['name']])]!=values[c['name']]:raise ValueError('First mode replacement native copy/upload/free differs')
        buffer=state['payload'][:state['size']]+state['buffer'][state['size']:]
        if bytes(engine.mem_read(0x0300D000,2048))!=buffer:raise ValueError('First mode replacement copy extent/preserved allocation differs')
    elif address==0x021DADC4:
        expected=['func_02048e74','func_ov003_021dad9c','func_02048fcc','func_ov003_021dada8','func_ov003_021dad9c'];group[4:20]=bytes(16);context[:]=bytes(240)
        previous=int.from_bytes(root[36:40],'little');struct.pack_into('<I',context,0,{1:1,4:2,6:3}.get(previous,0))
    elif address==0x021DAE50:
        phase=state['phase'];result=state['current'];redraw=phase in [0,1,3,4,5,6]
        if phase==0:
            expected=['func_ov003_021daf90','func_02041944']+(['func_02041538'] if state['fade'] else []);struct.pack_into('<I',group,8,1)
        elif phase==1:expected=['func_02041814']+(['func_ov003_021db034'] if state['busy']!=1 else [])
        elif phase==2:expected=['func_02041510'];result=9
        elif phase in [3,4,5]:result={3:1,4:4,5:6}[phase]
        elif phase==6:expected=['func_ov003_021db248']
        elif phase==7:expected=['func_02041510','func_02041538','func_0205e814'];result=8
        if redraw:expected+=['func_ov003_021dad9c','func_ov003_021dff60','func_ov003_021dad9c','func_ov003_021df6ac']
        if state['updates']:struct.pack_into('<I',group,4,state['current']^state['updates'])
        if engine.reg_read(UC_ARM_REG_R0)!=result:raise ValueError('First mode callback captured/selected return differs')
        for c in calls:
            if c['name'] in {'func_02041510','func_02041538'} and c['args'][:3]!=[0 if phase==0 else 1,2,10]:raise ValueError('First mode callback fade arguments differ')
            if c['name']=='func_0205e814' and c['args'][:3]!=[0,0,10]:raise ValueError('First mode exit transition arguments differ')
            if c['name'] in {'func_ov003_021dff60','func_ov003_021df6ac'} and c['args'][0]!=CONTEXT:raise ValueError('First mode actual context getter identity differs')
    elif address==0x021DAF7C:
        expected=['func_ov003_021df4b4','func_ov003_021dfccc']
        if calls[0]['args'][0]!=1:raise ValueError('First mode teardown flag differs')
    else:
        expected=['func_ov003_021dad9c','func_ov003_021dad9c','func_ov003_021deda4','func_ov003_021dad9c','func_020c35fc','func_ov003_021df3b4','func_ov003_021dfd18','func_02062378']
        if state['choice']!=34:expected+=['func_020620b4','func_02062358']
        for c in calls:
            if c['name']=='func_ov003_021deda4' and (c['args']!=[CONTEXT,5,0x021E0340,2] or bytes.fromhex(c['stack'])[:12]!=struct.pack('<3I',5,28,int.from_bytes(context[:4],'little'))):raise ValueError('First mode caption selection/text/geometry differs')
            if c['name']=='func_ov003_021df3b4' and (c['args']!=[CONTEXT,state['value'],16,2] or bytes.fromhex(c['stack'])[:12]!=struct.pack('<3I',21,28,2)):raise ValueError('First mode dynamic value/geometry differs')
            constants={'func_ov003_021dfd18':1,'func_020620b4':34,'func_02062358':1}
            if c['name'] in constants and c['args'][0]!=constants[c['name']]:raise ValueError('First mode initial selection sync differs')
    if [c['name'] for c in calls]!=expected or bytes(engine.mem_read(ROOT,40))!=bytes(root) or bytes(engine.mem_read(GROUP,20))!=bytes(group) or bytes(engine.mem_read(CONTEXT,240))!=bytes(context):raise ValueError('First mode complete call/context/state effects differ')
