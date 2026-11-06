import struct
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3
from overlay_oracle003_caption import seed_caption003,caption_arguments003,caption_call003,assert_caption003

FUNCTIONS={0x021D9BD0,0x021D9C60,0x021D9CB8,0x021D9D84,0x021D9DC0}
BASE=0x021E058C
VALUES=[-128,-1,0,1,127]


def seed_panel_callback003(engine,address,vector):
    if address not in FUNCTIONS:return seed_caption003(engine,address,vector)
    before=bytearray(engine.mem_read(BASE,228));before[209]=0xA0|vector%16
    struct.pack_into('<I',before,200,0x0300E000 if vector//16%2 else 0);before[204]=[0,127,128,255][vector//32%4]
    engine.mem_write(BASE,bytes(before));engine.mem_write(0x021E057C,bytes([(vector*53)&255,vector//16%2]))
    engine.mem_write(0x021E0580,struct.pack('<3I',0x80000000,0x80000001,0x80000002))
    return {'before':bytes(before),'base':(vector*53)&255,'selector':vector//16%2,'stopAt':vector//32%4,'row':0,'emits':0,'positions':[6,8,6],'runtime':0x03004000,'readyAfter':[0,1,3,7][vector//16%4],'queries':0,'updates':0}


def panel_callback_arguments003(address,vector,args):
    caption_arguments003(address,vector,args)
    if address==0x021D9BD0:args[:]=[[0,1,2,3,4,5,6,15,0xFFFFFFFF][vector%9],[0,1,0x80000000,0xFFFFFFFF][vector//9%4],VALUES[vector//36%5]&0xFFFFFFFF,vector//180%3]


def panel_callback_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return caption_call003(engine,address,name,value,state)
    if name=='func_02061944':return state['runtime']
    if name=='func_ov003_021d97a4':
        i=state['row'];state['row']+=1
        if engine.reg_read(UC_ARM_REG_R0)!=0x80000000+i:raise ValueError('Panel callback row identifier differs')
        if i==state['stopAt']:engine.mem_write(BASE+209,bytes([int.from_bytes(engine.mem_read(BASE+209,1),'little')|8]))
    if name=='func_ov003_021d97f8':
        args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]]
        if args[0]!=0x80000000+state['emits'] or len(set(args[1:]))!=3 or [int.from_bytes(engine.mem_read(p,1),'little',signed=True) for p in args[1:]]!=state['positions']:raise ValueError('Panel callback three mutable cursor locals differ')
        for i,p in enumerate(args[1:]):
            state['positions'][i]=((state['positions'][i]+i+1+128)&255)-128;engine.mem_write(p,bytes([state['positions'][i]&255]))
        state['emits']+=1;engine.mem_write(0x021E057C,bytes([(int.from_bytes(engine.mem_read(0x021E057C,1),'little')+7)&255]));return state['emits']
    if name=='func_0205fd28':
        result=int(state['queries']>=state['readyAfter']);state['queries']+=1;return result
    if name=='func_0205fd0c':
        state['updates']+=1;engine.mem_write(BASE+209,bytes([int.from_bytes(engine.mem_read(BASE+209,1),'little')|0xF8]))
    return value


def assert_panel_callback003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_caption003(engine,address,args,calls,state)
    after=bytearray(state['before']);expected=[]
    if address==0x021D9BD0:
        nested=3<=args[0]<=5
        expected=['func_02061944']+(['native_ov003_021d9bd0','func_02061944','func_02065818'] if nested else [])+['func_02065818']
        targets=([1 if args[3] else 2] if nested else [])+[args[0]]
        for c,i in zip((c for c in calls if c['name']=='func_02065818'),targets):
            if c['args'][:3]!=[(state['runtime']+16+i*12)&0xFFFFFFFF,args[1],args[2]]:raise ValueError('Panel recursive placement target/full-width x/signed y differs')
        calls=[c for j,c in enumerate(calls) if not(j==0 and c['name']=='native_ov003_021d9bd0')]
    elif address==0x021D9C60:
        expected=['func_020456ac']*2
        for c,layer in zip(calls,[1,2]):
            if c['args']!=[0,layer,1,2] or bytes.fromhex(c['stack'])[:8]!=struct.pack('<2I',30,21):raise ValueError('Panel background interior clear differs')
    elif address==0x021D9CB8:
        flag=after[209];emits=0;base=state['base'];stop=False
        for i in range(3):
            expected.append('func_ov003_021d97a4')
            if i==state['stopAt']:flag|=8
            if flag&8:flag&=~8;expected.append('func_ov003_021d9c60');stop=True;break
            expected.append('func_ov003_021d97f8');emits+=1;base=(base+7+emits)&255
        after[209]=(flag&~4)|2
        if state['emits']!=emits or bytes(engine.mem_read(0x021E057C,1))!=bytes([base]):raise ValueError('Panel callback cancellation/shared cursor reload differs')
        for c in (c for c in calls if c['name']=='func_ov003_021d97f8'):
            if bytes.fromhex(c['stack'])[:4]!=struct.pack('<I',state['selector']):raise ValueError('Panel callback fifth selector argument differs')
    elif address==0x021D9D84:
        after[209]&=~1;pointer=int.from_bytes(after[200:204],'little')
        if pointer:
            expected.append('func_0202a498');heap=int.from_bytes(after[204:205],'little',signed=True)&0xFFFFFFFF
            if calls[0]['args'][:2]!=[heap,pointer]:raise ValueError('Panel cleanup signed heap/allocation differs')
        expected.append('func_0205fd4c')
        if calls[-1]['args'][:2]!=[0,0]:raise ValueError('Panel cleanup reset arguments differ')
    else:
        if after[209]&1:
            after[209]&=7;expected=['func_0205fd34','func_0205fd28']+['func_0205fd0c','func_0205fd28']*state['readyAfter']
            if calls[0]['args'][:2]!=[BASE,16] or any(c['args'][0]!=BASE for c in calls) or state['queries']!=state['readyAfter']+1 or state['updates']!=state['readyAfter']:raise ValueError('Panel bounded completion wait differs')
            if state['readyAfter']:after[209]|=0xF8
    if [c['name'] for c in calls]!=expected or bytes(engine.mem_read(BASE,228))!=bytes(after):raise ValueError('Panel callback call sequence/context differs')
