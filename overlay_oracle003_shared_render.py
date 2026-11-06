import struct
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP

from overlay_oracle003_panel_callback import seed_panel_callback003,panel_callback_arguments003,panel_callback_call003,assert_panel_callback003

FUNCTIONS={0x021D95A0,0x021D9634,0x021D97A4,0x021D97F8}
VALUES=[-128,-1,0,1,127]


def parameters(vector):
    return {'count':vector%4,'present':vector//4%2,'selector':vector//8%2,'special':vector//16%2,'alias':vector//32%5,'coord':VALUES[vector//160%5],'base':[0,127,128,255][vector%4]}


def seed_shared_render003(engine,address,vector):
    if address not in FUNCTIONS:return seed_panel_callback003(engine,address,vector)
    state=parameters(vector);state['vector']=vector
    engine.mem_write(0x021E057C,bytes([state['base'],state['selector']]))
    engine.mem_write(0x0300A000,bytes([state['coord']&255,(state['coord']+1)&255,(state['coord']+2)&255]))
    engine.mem_write(0x0301FF00,struct.pack('<I',vector%3))
    state['coords']=bytes(engine.mem_read(0x0300A000,3))
    for index in range(3):
        identifier=[-32768,-1,0,1,32767][(vector+index)%5]
        engine.mem_write(0x03006018+index*256,struct.pack('<h',identifier))
        engine.mem_write(0x03006030+index*256,bytes([100 if state['special'] else 99,0,[0,127,128,255][(vector+index)%4]]))
    engine.mem_write(0x0300B000,struct.pack('<3I',0x100,0x200,0x300))
    state['records']=[bytes(engine.mem_read(0x03006000+index*256,132)) for index in range(3)]
    state['counts']=[vector//(3**index)%3 for index in range(3)]
    state['mask']=vector//27%8;state['layoutSelector']=vector//216%2
    if address==0x021D9634:engine.mem_write(0x021E057D,bytes([state['layoutSelector']]))
    state['cursor']=[0,4096,0xFFFFFFF0][vector%3];engine.mem_write(0x0300425C,struct.pack('<I',state['cursor']))
    state['runtime']=bytes(engine.mem_read(0x03004000,608));state['allocations']=0
    state['table']=bytes(engine.mem_read(0x021E014A,22))
    return state


def render_arguments003(address,vector,args):
    panel_callback_arguments003(address,vector,args)
    if address==0x021D9634:args[0]=0x0300B000
    if address==0x021D97A4:args[0]=vector%3
    if address==0x021D97F8:
        alias=parameters(vector)['alias'];a,b,c=[0x0300A000,0x0300A001,0x0300A002]
        if alias==1:b=a
        if alias==2:c=a
        if alias==3:c=b
        if alias==4:b=c=a
        args[:]=[vector%3,a,b,c]


def shared_render_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return panel_callback_call003(engine,address,name,value,state)
    first=engine.reg_read(UC_ARM_REG_R0)
    if name=='func_02061944':return 0x03004000
    if name in {'func_02062a10','func_020c3948'}:
        if address==0x021D9634:
            if first not in [0x100,0x200,0x300] or name!=('func_02062a10' if state['layoutSelector'] else 'func_020c3948'):raise ValueError('Shared layout namespaced row getter differs')
            index=first//256-1
            return 0x03006000+index*256 if state['mask']>>index&1 else 0
        return 0x03006000 if state['present'] else 0
    if name=='func_02044cdc':
        ids=[int.from_bytes(record[24:26],'little',signed=True)&0xFFFFFFFF for record in state['records']]
        if first not in ids:raise ValueError('Shared renderer signed record identifier differs')
        return state['counts'][ids.index(first)] if address==0x021D9634 else state['count']
    if name=='func_0201d444':
        template=bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_R1),32)).split(b'\0',1)[0]
        if engine.reg_read(UC_ARM_REG_R1)!=0x021E02C4:raise ValueError('Shared panel filename identity differs')
        engine.mem_write(first,template+b'\0');state['template']=template;return len(template)
    if name=='func_0205ff80' and bytes(engine.mem_read(first,len(state['template'])+1))!=state['template']+b'\0':raise ValueError('Shared panel formatted filename differs')
    if name=='func_02065730':
        i=state['allocations'];args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]]
        entry=state['table'][i*2:i*2+2];signed=int.from_bytes(entry[:1],'little',signed=True)&0xFFFFFFFF
        if args!=[0x03004010+(i+1)*12,signed,0,entry[1]] or int.from_bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_SP),4),'little')!=state['cursor']:raise ValueError('Shared panel eleven-entry catalog/cursor differs')
        state['cursor']=(state['cursor']+3)&0xFFFFFFFF;engine.mem_write(0x0300425C,struct.pack('<I',state['cursor']))
        delta=7+i;state['cursor']=(state['cursor']+delta)&0xFFFFFFFF;state['allocations']+=1;return delta
    return value


def signed(value):return ((value+128)&255)-128


def assert_shared_render003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_panel_callback003(engine,address,args,calls,state)
    expected=[]
    if address==0x021D95A0:
        expected=['func_02061944','func_0201d444','func_0205ff80']+['func_02065730']*11+['func_0205ff9c']
        runtime=bytearray(state['runtime']);struct.pack_into('<I',runtime,604,state['cursor'])
        if state['allocations']!=11 or bytes(engine.mem_read(0x03004000,608))!=bytes(runtime):raise ValueError('Shared panel complete runtime/cursor differs')
    elif address==0x021D9634:
        expected=['func_02061c1c'];panels=[[6,3,3,26]];y=6
        for i in range(3):
            expected.append('func_02062a10' if state['layoutSelector'] else 'func_020c3948')
            count=state['counts'][i] if state['mask']>>i&1 else 0
            if state['mask']>>i&1:expected.append('func_02044cdc')
            y=(y+{1:3,2:5}.get(count,0))&255
            expected+=['func_02061c1c']*3;panels.extend([[i+7,7,y,11],[i+10,19,y,5],[i+13,10,(y+2)&255,17]])
            y=(y+(3 if count==1 else 6))&255
        expected.append('func_02045ed0')
        rows=[c for c in calls if c['name']=='func_02061c1c']
        if [c['args'] for c in rows]!=panels or any(bytes.fromhex(c['stack'])[:12]!=struct.pack('<3I',2,0,0) for c in rows) or calls[-1]['args'][0]!=1:raise ValueError('Shared three-record layout geometry/stack flags differs')
    elif address==0x021D97A4:
        expected=['func_02061944','func_02062a10']
        if state['present']:
            expected.append('func_02061de4');c=calls[-1];identifier=int.from_bytes(state['records'][0][24:26],'little',signed=True)&0xFFFFFFFF
            if c['args']!=[0x03004010+(state['base']+3)*12,identifier,state['base'],1] or bytes.fromhex(c['stack'])[:4]!=bytes(4):raise ValueError('Shared fallback icon target/identifier differs')
    else:
        expected=['func_02061944','func_02062a10' if state['selector'] else 'func_020c3948'];coords=bytearray(state['coords']);placements=[]
        a,b,c=[p-0x0300A000 for p in args[1:]];count=state['count']
        if state['present']:
            expected+=['func_02044cdc']
            for i in range(count+1):
                placements.append([signed(state['base']+3+i)&0xFFFFFFFF,1,signed(coords[a])&0xFFFFFFFF,state['vector']%3]);coords[a]=(coords[a]+5)&255
            coords[a]=(coords[a]+(2 if count else 1))&255
            if count in [1,2]:
                delta=3 if count==1 else 5;coords[b]=(coords[b]+delta)&255;coords[c]=(coords[c]+delta)&255
            placements.append([signed(state['records'][0][50]+6)&0xFFFFFFFF,7,signed(coords[b])&0xFFFFFFFF,0])
            if state['special']:placements.append([11,22,signed(coords[c])&0xFFFFFFFF,0])
            delta=9 if count else 6;coords[b]=(coords[b]+delta)&255;coords[c]=(coords[c]+delta)&255
            expected+=['func_ov003_021d9bd0']*len(placements)
        if [call['args'] for call in calls if call['name']=='func_ov003_021d9bd0']!=placements or bytes(engine.mem_read(0x0300A000,3))!=bytes(coords) or engine.reg_read(UC_ARM_REG_R0)!=(count+1 if state['present'] else 0):raise ValueError('Shared renderer signed coordinate progression/aliasing/optional marker differs')
    if [c['name'] for c in calls]!=expected:raise ValueError('Shared rendering call sequence differs')
