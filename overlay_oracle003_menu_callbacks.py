import struct
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2

from overlay_oracle003_panel_modes import seed_panel_modes003, panel_modes_call003, assert_panel_modes003

FUNCTIONS={0x021D89D8,0x021D8CAC,0x021D8CE8}
BASE=0x021E0498
FLAG=BASE+209


def seed_menu_callbacks003(engine,address,vector):
    if address not in FUNCTIONS:return seed_panel_modes003(engine,address,vector)
    flag=vector%16
    ui=(vector*53)&255
    before=bytearray(engine.mem_read(BASE,228))
    before[209]=flag|0xA0
    struct.pack_into('<I',before,200,0x0300E000 if vector//16%2 else 0)
    before[204]=[0,127,128,255][vector//32%4]
    engine.mem_write(BASE,bytes(before))
    engine.mem_write(0x021E0465,bytes([ui]))
    for g,base in enumerate([0x021E0468,0x021E048C,0x021E0474,0x021E0480]):engine.mem_write(base,struct.pack('<3I',*[0x80000000+g*256+i for i in range(3)]))
    return {'before':bytes(before),'flag':flag|0xA0,'ui':ui,'row':0,'emits':0,'stopAt':vector//16%13,'action':vector//208%3,'readyAfter':[0,1,3,7][vector//16%4],'queries':0,'updates':0}


def menu_callbacks_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return panel_modes_call003(engine,address,name,value,state)
    if name=='func_ov003_021d82f4':
        row=state['row'];state['row']+=1
        if row==state['stopAt'] and state['action']==1:engine.mem_write(FLAG,bytes([int.from_bytes(engine.mem_read(FLAG,1),'little')&15]))
    if name=='func_0205fd18':
        if state['row']-1==state['stopAt'] and state['action']==2:engine.mem_write(FLAG,bytes([int.from_bytes(engine.mem_read(FLAG,1),'little')|8]))
    if name=='func_ov003_021d85e4':
        state['emits']+=1
        p=engine.reg_read(UC_ARM_REG_R2)
        engine.mem_write(p,bytes([(int.from_bytes(engine.mem_read(p,1),'little')+state['emits'])&255]))
        engine.mem_write(0x021E0465,bytes([(int.from_bytes(engine.mem_read(0x021E0465,1),'little')+7)&255]))
        return state['emits']%3+1
    if name=='func_0205fd28':
        result=int(state['queries']>=state['readyAfter']);state['queries']+=1
        return result
    if name=='func_0205fd0c':
        state['updates']+=1
        engine.mem_write(FLAG,bytes([int.from_bytes(engine.mem_read(FLAG,1),'little')|0xF8]))
    return value


def assert_menu_callbacks003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_panel_modes003(engine,address,args,calls,state)
    after=bytearray(state['before']);expected=[]
    if address==0x021D89D8:
        flag=(after[209]&15)|16;stop=False;row=0;emits=0;ui=state['ui'];cursor=0
        for group,(x,y) in enumerate([(9,4),(18,4),(3,6),(24,6)]):
            if stop:continue
            for i in range(3):
                expected.append('func_ov003_021d82f4')
                c=calls[cursor];cursor+=1
                if c['args'][0]!=0x80000000+group*256+i:raise ValueError('Menu callback identifier group differs')
                if row==state['stopAt'] and state['action']==1:flag&=15
                row+=1
                if flag&0xF0==0:break
                flag|=4;expected.append('func_0205fd18');cursor+=1
                if row-1==state['stopAt'] and state['action']==2:flag|=8
                if flag&8:stop=True;break
                expected.append('func_ov003_021d85e4');c=calls[cursor];cursor+=1
                def signed(v):return ((v+128)&255)-128
                if c['args'][0]!=0x80000000+group*256+i or c['args'][3]!=(1 if group in [0,2] else 0):raise ValueError('Menu callback emitted cell selector/flag differs')
                emits+=1
                y=signed(y+emits)
                if bytes(engine.mem_read(c['args'][1],1))!=bytes([x]) or c['args'][1]==c['args'][2]:raise ValueError('Menu callback distinct coordinate locals differ')
                ui=(ui+7+emits%3+1)&255
            if group in [0,1,2,3]:
                groupcalls=[c for c in calls[:cursor] if c['name']=='func_ov003_021d85e4' and (c['args'][0]>>8)&3==group]
                if groupcalls and int.from_bytes(engine.mem_read(groupcalls[-1]['args'][2],1),'little')!=y&255:raise ValueError('Menu callback mutated coordinate cursor differs')
        if stop:flag&=~8;expected.append('func_ov003_021d8890')
        after[209]=(flag&~4)|2
        if state['row']!=row or state['emits']!=emits or bytes(engine.mem_read(0x021E0465,1))!=bytes([ui]):raise ValueError('Menu callback early stop/cell counter differs')
    elif address==0x021D8CAC:
        after[209]&=~1
        pointer=int.from_bytes(after[200:204],'little')
        if pointer:
            expected.append('func_0202a498');heap=int.from_bytes(after[204:205],'little',signed=True)&0xFFFFFFFF
            if calls[0]['args'][:2]!=[heap,pointer]:raise ValueError('Menu callback signed heap or allocation differs')
        expected.append('func_0205fd4c')
        if calls[-1]['args'][:2]!=[0,0]:raise ValueError('Menu callback cleanup arguments differ')
    else:
        if after[209]&1:
            after[209]&=7
            expected=['func_0205fd34','func_0205fd28']+['func_0205fd0c','func_0205fd28']*state['readyAfter']
            if calls[0]['args'][:2]!=[BASE,16] or any(c['args'][0]!=BASE for c in calls):raise ValueError('Menu completion wait context differs')
            if state['updates']!=state['readyAfter'] or state['queries']!=state['readyAfter']+1:raise ValueError('Menu completion wait iteration bound differs')
            if state['readyAfter']:after[209]|=0xF8
        elif calls:raise ValueError('Inactive menu completion wait called external helpers')
    if [c['name'] for c in calls]!=expected or bytes(engine.mem_read(BASE,228))!=bytes(after):raise ValueError('Menu callback flags/context or call sequence differs')
