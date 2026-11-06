import struct
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3

from overlay_oracle003_mode3_network import seed_mode3_network003,mode3_network_arguments003,mode3_network_call003,assert_mode3_network003

FUNCTIONS={0x021DB9BC,0x021DBA20,0x021DBAE4,0x021DBB18,0x021DBBC4,0x021DBCA0,0x021DBD18,0x021DBDEC}
ROOT=0x021E0690
CONTEXT=0x021E06B8
ONE=0x021E07BC
THREE=0x021E07CC
SELECT=[-2147483648,-1,0,1,2,3,4,5,2147483647]


def seed_modes13_003(engine,address,vector):
    if address not in FUNCTIONS:return seed_mode3_network003(engine,address,vector)
    previous=[2,7,1,4,6,12,0xFFFFFFFF][vector%7];engine.mem_write(ROOT+36,struct.pack('<I',previous));engine.mem_write(ROOT+4,struct.pack('<I',0x0300D000))
    phase=[0,1,2,3,4,99][vector%6];current=[0,1,7,0xFFFFFFFF][vector//6%4]
    engine.mem_write(ONE,struct.pack('<2I',current,phase));engine.mem_write(THREE+4,struct.pack('<2I',current,phase))
    selected=SELECT[vector%9];engine.mem_write(CONTEXT,struct.pack('<i',selected));pressed=[0,1,2,3,0x8000][vector//9%5];repeat=[0,64,128,192][vector//45%4];engine.mem_write(0x03005000,struct.pack('<4H',0,pressed,0,repeat))
    state={'vector':vector,'root':bytes(engine.mem_read(ROOT,40)),'one':bytes(engine.mem_read(ONE,16)),'three':bytes(engine.mem_read(THREE,20)),'context':bytes(engine.mem_read(CONTEXT,240)),'phase':phase,'current':current,'selected':selected,'pressed':pressed,'repeat':repeat,'previous':previous,'afterPrevious':[2,7,0xFFFFFFFF][vector//7%3],'fade':vector//24%2,'gate':vector//24%2,'ready':[0,1,0xFFFFFFFF][vector//48%3],'heap':[0,2,0xFFFFFFFF][vector%3],'oldHeap':0x1000+vector,'heapCalls':0,'size':vector%65,'bank':vector%4,'payload':bytes(engine.mem_read(0x0300C000,65)),'buffer':bytes(engine.mem_read(0x0300D000,2048))}
    if address==0x021DBDEC:state['callbacks']={0x0202A250:'func_0202a250',0x0203CC2C:'func_0203cc2c',0x0204518C:'func_0204518c',0x02008E0C:'func_02008e0c',0x02045994:'func_02045994',0x0202A498:'func_0202a498'}
    return state


def modes13_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return mode3_network_call003(engine,address,name,value,state)
    args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]]
    if name=='func_02048e74':
        if args[:2]!=([ONE,1] if address==0x021DB9BC else [THREE+4,3]):raise ValueError('Mode SDK state initialization identity differs')
        engine.mem_write(args[0],struct.pack('<4I',args[1],0,12,12))
    if name=='func_02048fcc':
        if args[0]!=CONTEXT:raise ValueError('Mode initialized context getter differs')
        engine.mem_write(CONTEXT,bytes(240))
    if name=='func_02041944':return state['fade']
    if name=='func_0202a634':return 0x03005000
    if name=='func_0202a1e0':
        if args[0]!=(1 if state['heapCalls']==0 else state['oldHeap']):raise ValueError('Mode heap switch/restoration differs')
        state['heapCalls']+=1;return state['oldHeap']
    if name in {'func_ov003_021dbb18','func_ov003_021dbbc4'} and address==0x021DBA20:engine.mem_write(ONE,struct.pack('<I',state['current']^0x100))
    if name in {'func_ov003_021dbf68','func_ov003_021dc1e8'} and address==0x021DBD18:engine.mem_write(THREE+4,struct.pack('<I',state['current']^0x200))
    if name=='func_ov003_021dc060':return state['gate']
    if name=='func_020c4318':return state['ready']
    if name=='func_ov003_021deda4' and address==0x021DBB18:engine.mem_write(ROOT+36,struct.pack('<I',state['afterPrevious']))
    if name=='func_02048f8c':return state['bank']
    if name=='func_0202a250':return state['heap']
    if name=='func_0203cc2c':
        if args[:2]!=[0x021E032C,state['heap']]:raise ValueError('Mode cleanup resource archive/heap differs')
        return 0x0300F000
    if name=='func_0204518c':
        if args[1:3]!=[0x0300F000,2]:raise ValueError('Mode cleanup replacement section differs')
        engine.mem_write(args[0],struct.pack('<2I',0x0300C000,state['size']))
    return value


def assert_modes13_003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_mode3_network003(engine,address,args,calls,state)
    root=bytearray(state['root']);one=bytearray(state['one']);three=bytearray(state['three']);context=bytearray(state['context']);expected=[];phase=state['phase'];result=state['current']
    ui=['func_ov003_021dad9c','func_ov003_021dff60','func_ov003_021dad9c','func_ov003_021df6ac']
    if address==0x021DB9BC:
        expected=['func_02048e74','func_ov003_021dad9c','func_02048fcc','func_ov003_021dada8'];one[:]=struct.pack('<4I',1,0,12,12);context[:]=bytes(240)
        if state['previous'] in [2,7]:expected.append('func_ov003_021dad9c');struct.pack_into('<I',context,0,int(state['previous']==7))
    elif address==0x021DBA20:
        if phase==0:expected=['func_ov003_021dbb18','func_02041944']+(['func_02041538'] if state['fade'] else [])+ui;struct.pack_into('<2I',one,0,state['current']^0x100,1)
        elif phase==1:expected=['func_ov003_021dbbc4']+ui;struct.pack_into('<I',one,0,state['current']^0x100)
        elif phase==2:result=2
        elif phase==3:expected=['func_02041538','func_ov003_021dccc4'];result=7
        elif phase==4:result=0
        if engine.reg_read(UC_ARM_REG_R0)!=result:raise ValueError('Mode1 captured/changed callback result differs')
    elif address==0x021DBAE4:
        expected=['func_ov003_021df4b4','func_ov003_021dfccc']
        if calls[0]['args'][0]!=(2 if phase==2 else 1):raise ValueError('Mode1 selected teardown type differs')
    elif address==0x021DBB18:
        expected=['func_ov003_021dada8']
        if state['previous']!=2:expected+=['func_ov003_021dad9c','func_ov003_021ded08']
        expected+=['func_ov003_021dad9c','func_ov003_021dad9c','func_ov003_021deda4','func_ov003_021dfd18','func_ov003_021dada8']
        if state['afterPrevious']!=2:expected.append('func_020620e8')
        struct.pack_into('<I',root,36,state['afterPrevious'])
        for c in calls:
            if c['name']=='func_ov003_021ded08' and (c['args']!=[CONTEXT,2,16,1] or bytes.fromhex(c['stack'])!=struct.pack('<4I',3,30,2,0)):raise ValueError('Mode1 conditional caption geometry differs')
            if c['name']=='func_ov003_021deda4' and (c['args']!=[CONTEXT,2,0x021E034C,2] or bytes.fromhex(c['stack'])[:12]!=struct.pack('<3I',6,28,state['selected']&0xFFFFFFFF)):raise ValueError('Mode1 selected caption/text/geometry differs')
            if c['name']=='func_020620e8' and c['args'][:2]!=[37,1]:raise ValueError('Mode1 fresh previous-mode selection sync differs')
    elif address==0x021DBBC4:
        expected=['func_0202a634','func_ov003_021dad9c'];selected=state['selected'];sounds=[]
        if state['repeat']&64:selected=selected-1 if selected>0 else 1;expected.append('func_0205e7a8');sounds.append([0xFFFFFFFF,85])
        elif state['repeat']&128:selected=selected+1 if selected<1 else 0;expected.append('func_0205e7a8');sounds.append([0xFFFFFFFF,85])
        struct.pack_into('<i',context,0,selected)
        if state['pressed']&1:
            if selected in [0,1]:struct.pack_into('<I',one,4,selected+2)
            expected.append('func_0205e7a8');sounds.append([0xFFFFFFFF,82])
        elif state['pressed']&2:struct.pack_into('<I',one,4,4);expected.append('func_0205e7a8');sounds.append([0xFFFFFFFF,83])
        if [c['args'][:2] for c in calls if c['name']=='func_0205e7a8']!=sounds:raise ValueError('Mode1 signed direction/button/sound precedence differs')
    elif address==0x021DBCA0:
        expected=['func_02048e74','func_ov003_021dad9c','func_02048fcc','func_0202a1e0','func_ov003_021df518','func_02068ae8','func_0207ca14','func_020bf518','func_0202a1e0','func_ov003_021dad9c','func_0206258c']
        three[4:20]=struct.pack('<4I',3,0,12,12);struct.pack_into('<I',three,0,1);context[:]=bytes(240);context[16]=3
        if state['heapCalls']!=2:raise ValueError('Mode3 complete heap restoration differs')
    elif address==0x021DBD18:
        redraw=phase in [1,3,4]
        if phase==0:expected=['func_ov003_021dbe4c','func_02041538'];struct.pack_into('<I',three,8,1)
        elif phase==1:expected=['func_ov003_021dc060']+([] if state['gate'] else ['func_ov003_021dbf68'])+['func_ov003_021dc1e8'];struct.pack_into('<I',three,4,state['current']^0x200)
        elif phase==2:
            expected=['func_020c4318']+(['func_02068f60'] if state['ready'] else [])+['func_ov003_021dad9c','func_ov003_021df6ac']
            if state['ready']:struct.pack_into('<I',three,8,1)
        elif phase==3:result=0
        elif phase==4:result=2
        if redraw:expected+=ui
        if engine.reg_read(UC_ARM_REG_R0)!=result:raise ValueError('Mode3 captured/changed callback result differs')
    else:
        expected=['func_0206258c','func_020625ac','func_020693e0','func_02068d54','func_020c0210','func_020c013c','func_0207cdb8','func_020bf5c0','func_ov003_021df518','func_ov003_021dfccc','func_ov003_021dad9c','func_ov003_021deb78','func_02048f8c','func_ov003_021dad1c','func_0202a250','func_0203cc2c','func_0204518c','func_02008e0c','func_02045994','func_0202a498']
        buffer=state['payload'][:state['size']]+state['buffer'][state['size']:]
        if bytes(engine.mem_read(0x0300D000,2048))!=buffer:raise ValueError('Mode3 cleanup connected native replacement copy boundary differs')
        values={'func_02008e0c':[0x0300C000,0x0300D000,state['size']],'func_02045994':[state['bank'],0x0300D000,0,2048],'func_0202a498':[state['heap'],0x0300F000],'func_ov003_021dad1c':[2,state['bank']],'func_ov003_021deb78':[CONTEXT,0]}
        for c in calls:
            if c['name'] in values and c['args'][:len(values[c['name']])]!=values[c['name']]:raise ValueError('Mode3 cleanup resource/heap/context arguments differ')
    for c in calls:
        if c['name']=='func_02041538' and c['args'][:3]!=[1 if address==0x021DBA20 and phase==3 else 0,2,10]:raise ValueError('Mode callback fade arguments differ')
        if c['name']=='func_ov003_021dccc4' and c['args'][0]!=1:raise ValueError('Mode1 secondary selection forwarding differs')
        if c['name'] in {'func_ov003_021dff60','func_ov003_021df6ac'} and c['args'][0]!=CONTEXT:raise ValueError('Mode actual context getter identity differs')
    if [c['name'] for c in calls]!=expected or bytes(engine.mem_read(ROOT,40))!=bytes(root) or bytes(engine.mem_read(ONE,16))!=bytes(one) or bytes(engine.mem_read(THREE,20))!=bytes(three) or bytes(engine.mem_read(CONTEXT,240))!=bytes(context):raise ValueError('Mode1/3 complete state/context/call effects differ')
