import struct
from unicorn.arm_const import UC_ARM_REG_R0

from overlay_oracle003_compatibility import seed_compatibility003,compatibility_arguments003,compatibility_call003,assert_compatibility003

FUNCTIONS={0x021DB034,0x021DB20C,0x021DB248}
GROUP=0x021E07A8
CONTEXT=0x021E06B8
SELECTIONS=[-2147483648,-1,0,1,2,3,4,5,2147483647]
PRESSES=[0,1,2,3,0x8000]
ACK=[0,*[1<<i for i in range(16)],0xFF7,0xFFFF]


def seed_first_input003(engine,address,vector):
    if address not in FUNCTIONS:return seed_compatibility003(engine,address,vector)
    selected=SELECTIONS[vector%9];pressed=PRESSES[vector//9%5];repeat=[0,64,128,192][vector//45%4]
    if address==0x021DB248:
        pressed=ACK[vector%19];engine.mem_write(GROUP,bytes([[0,1,2,3,127,255][vector//19%6]]))
    engine.mem_write(CONTEXT,struct.pack('<i',selected));engine.mem_write(0x03005000,struct.pack('<4H',0,pressed,0,repeat))
    return {'selected':selected,'pressed':pressed,'repeat':repeat,'mode':vector//180%3,'success':vector//540%2,'group':bytes(engine.mem_read(GROUP,20)),'context':bytes(engine.mem_read(CONTEXT,240)),'callbacks':{0x021DEA38:'func_ov003_021dea38',0x021DFD18:'func_ov003_021dfd18'}}


def first_input_arguments003(address,vector,args):
    compatibility_arguments003(address,vector,args)
    if address==0x021DB20C:args[:2]=[[0,1,2,0xFFFFFFFF][vector%4],[0,1,0xFFFFFFFF][vector//4%3]]


def first_input_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return compatibility_call003(engine,address,name,value,state)
    if name=='func_0202a634':return 0x03005000
    if name=='func_020c367c':return state['mode']
    if name=='func_ov003_021db57c':
        if engine.reg_read(UC_ARM_REG_R0)!=(1 if state['mode']==1 else 0):raise ValueError('First input confirmation capability selector differs')
        return state['success']
    return value


def assert_first_input003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_compatibility003(engine,address,args,calls,state)
    context=bytearray(state['context']);group=bytearray(state['group']);expected=[];sounds=[];message=None;failure=None
    if address==0x021DB034:
        expected=['func_0202a634','func_ov003_021dad9c'];selected=state['selected']
        if state['repeat']&64:selected=selected-1 if selected>0 else 4;expected.append('func_0205e7a8');sounds.append([0xFFFFFFFF,85])
        elif state['repeat']&128:selected=selected+1 if selected<4 else 0;expected.append('func_0205e7a8');sounds.append([0xFFFFFFFF,85])
        struct.pack_into('<i',context,0,selected)
        if state['pressed']&1:
            if selected==0:
                expected.append('func_020c367c');success=state['success'] if state['mode'] in [1,2] else 0
                if state['mode'] in [1,2]:expected.append('func_ov003_021db57c')
                if success:
                    message=2 if state['mode']==1 else 1;failure=0;group[0]=1
                    expected+=['func_ov003_021db20c','func_ov003_021dea38','func_ov003_021dfd18','func_0205e7a8'];sounds.append([0xFFFFFFFF,83])
                else:
                    message=0;failure=1;group[0]=2;expected+=['func_ov003_021db290','func_ov003_021db20c','func_ov003_021dea38','func_ov003_021dfd18']
                struct.pack_into('<I',group,8,6)
            elif selected in [1,2,3,4]:
                struct.pack_into('<I',group,8,{1:3,2:4,3:5,4:7}[selected]);expected.append('func_0205e7a8');sounds.append([0xFFFFFFFF,83 if selected==4 else 82])
        elif state['pressed']&2:struct.pack_into('<I',group,8,7);expected.append('func_0205e7a8');sounds.append([0xFFFFFFFF,83])
        if [c['args'][:2] for c in calls if c['name']=='func_0205e7a8']!=sounds:raise ValueError('First input direction/confirm/cancel sound precedence differs')
        for c in calls:
            if c['name']=='func_ov003_021db20c' and c['args'][:2]!=[message,failure]:raise ValueError('First input confirmation result/message forwarding differs')
    elif address==0x021DB20C:expected=['func_ov003_021dea38','func_ov003_021dfd18'];message=args[0];failure=args[1]
    else:
        expected=['func_0202a634']
        if state['pressed']&0xFF7:
            if group[0]!=2:expected.append('func_ov003_021df668')
            struct.pack_into('<I',group,8,group[0])
        for c in calls:
            if c['name']=='func_ov003_021df668' and c['args'][0]!=1:raise ValueError('First input acknowledgement close flag differs')
    if message is not None:
        for c in calls:
            if c['name']=='func_ov003_021dea38' and (c['args']!=[20,1,message,1] or bytes.fromhex(c['stack'])[:8]!=struct.pack('<2I',1,87 if failure else 0xFFFFFFFF)):raise ValueError('First input actual message helper stack arguments differ')
            if c['name']=='func_ov003_021dfd18' and c['args'][0]!=0:raise ValueError('First input message state reset differs')
    if [c['name'] for c in calls]!=expected or bytes(engine.mem_read(GROUP,20))!=bytes(group) or bytes(engine.mem_read(CONTEXT,240))!=bytes(context):raise ValueError('First input full state/context/call effects differ')
