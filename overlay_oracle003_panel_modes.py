import struct
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2

from overlay_oracle003_panel_lifecycle import seed_panel_lifecycle003, panel_lifecycle_call003, assert_panel_lifecycle003

PANELS={0x021D8DDC:(21,35,35,36),0x021D8FF4:(22,36,35,36),0x021D91F8:(10,37,37,38),0x021D93FC:(11,38,37,38)}
BASE=0x021E058C


def seed_panel_modes003(engine,address,vector):
    if address not in PANELS:return seed_panel_lifecycle003(engine,address,vector)
    context=bytearray(engine.mem_read(BASE,228));context[209]=0xA0|vector//4%16
    runtime=bytearray(engine.mem_read(0x03004000,624))
    runtime[617]=[-128,35,36,37,38,127][vector%6]&255
    runtime[620]=[42,41,255][vector//64%3]
    runtime[623]=[-128,-1,0,1,127][vector%5]&255
    engine.mem_write(BASE,bytes(context));engine.mem_write(0x03004000,bytes(runtime))
    phase=[0,1,2,255][vector%4];engine.mem_write(0x021E057E,bytes([phase]))
    return {'context':bytes(context),'runtime':bytes(runtime),'phase':phase,'direction':[0,1,0xFFFFFFFF][vector//192%3],'choice':[-128,35,36,37,38,127][(vector//3)%6],'payload':bytes(engine.mem_read(0x03008000,208))}


def panel_modes_call003(engine,address,name,value,state):
    if address not in PANELS:return panel_lifecycle_call003(engine,address,name,value,state)
    if name=='func_02061944':return 0x03004000
    if name=='func_0205fc10':return 0x03008000
    if name=='func_0206238c':
        pointer=engine.reg_read(UC_ARM_REG_R0);panel,initial,first,second=PANELS[address]
        if bytes(engine.mem_read(pointer,1))!=bytes([initial]) or [engine.reg_read(UC_ARM_REG_R1),engine.reg_read(UC_ARM_REG_R2)]!=[first,second]:raise ValueError('Panel selection initialized byte/range differs')
        engine.mem_write(pointer,bytes([state['choice']&255]));return state['direction']
    return value


def assert_panel_modes003(engine,address,args,calls,state):
    if address not in PANELS:return assert_panel_lifecycle003(engine,address,args,calls,state)
    context=bytearray(state['context']);runtime=state['runtime'];expected=['func_02061944'];phase=state['phase'];result=0
    panel,initial,first,second=PANELS[address]
    if phase==0:
        expected+=['func_02062328','func_02062144','func_ov003_021d9e40','func_ov003_021d9634','func_ov003_021d9984']
        context[209]|=8
        if runtime[620]==42 and context[209]&1==0:
            context[208]=0;context[209]=(context[209]|1)&~10;context[:208]=state['payload']
            expected+=['func_0205fc10','func_0205fd0c']
        phase=1
        for c in calls:
            if c['name']=='func_02062144' and c['args'][:2]!=[int.from_bytes(runtime[623:624],'little',signed=True)&0xFFFFFFFF,0]:raise ValueError('Panel signed selector forwarding differs')
            if c['name']=='func_ov003_021d9634' and c['args'][0]!=0x021E0580:raise ValueError('Panel row table identity differs')
            if c['name']=='func_ov003_021d9984' and c['args'][:2]!=[panel,0x021E0580]:raise ValueError('Panel caption/table arguments differ')
            if c['name']=='func_0205fc10' and (c['args']!=[BASE,0x021D9CB8,0x021D9D84,0] or bytes.fromhex(c['stack'])!=struct.pack('<4I',18,8192,2,0)):raise ValueError('Panel payload callback identity/stack flags differ')
            if c['name']=='func_0205fd0c' and c['args'][0]!=BASE:raise ValueError('Panel payload context differs')
    elif phase==1:
        expected+=['func_0206238c']
        old=int.from_bytes(runtime[617:618],'little',signed=True)
        if state['choice']!=old:
            expected+=['func_020620b4','func_02062358'];result=1
            selected=next(c for c in calls if c['name']=='func_020620b4');direction=next(c for c in calls if c['name']=='func_02062358')
            if selected['args'][0]!=state['choice']&0xFFFFFFFF or direction['args'][0]!=int(state['direction']==1):raise ValueError('Panel changed selection/direction normalization differs')
    if runtime[620]!=42:expected+=['func_ov003_021d9dc0'];result=1
    if [c['name'] for c in calls]!=expected or engine.reg_read(UC_ARM_REG_R0)!=result:raise ValueError('Panel startup/update/exit call sequence or completion differs')
    if bytes(engine.mem_read(BASE,228))!=bytes(context) or bytes(engine.mem_read(0x021E057E,1))!=bytes([phase]) or bytes(engine.mem_read(0x03004000,624))!=runtime:raise ValueError('Panel complete context/payload/phase differs')
