import struct
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP

from overlay_oracle003_menu_callbacks import seed_menu_callbacks003, menu_callbacks_call003, assert_menu_callbacks003

FUNCTIONS={0x021D85E4,0x021D867C,0x021D87C8,0x021D8890,0x021D88E8}
VALUES=[-128,-1,0,1,127]


def word(engine,address):
    return int.from_bytes(engine.mem_read(address,4),'little')


def seed_cells003(engine,address,vector):
    if address not in FUNCTIONS:
        return seed_menu_callbacks003(engine,address,vector)
    state={'vector':vector,'mask':vector%64,'phase':vector%16,'count':vector//2%5,'present':vector%2,'base':[0,127,128,255][vector//10%4], 'x':VALUES[vector//40%5],'y':VALUES[vector//200%5], 'alias':vector//1000%2,'runtime':0x03004000}
    engine.mem_write(0x021E0465,bytes([state['base']]))
    engine.mem_write(0x0300A000,bytes([state['x']&255,state['y']&255]))
    engine.mem_write(0x03006018,struct.pack('<h',[-32768,-1,0,1,32767][vector%5]))
    state['id']=int.from_bytes(engine.mem_read(0x03006018,2),'little',signed=True)
    for i in range(6):
        p=0x03007000+i*256
        engine.mem_write(p+20,struct.pack('<I',0xFFFFFFFF if vector//64%3==0 else i*1729+vector))
    for i in range(4):
        engine.mem_write(0x03008000+i*256,struct.pack('<I',0x03009000+i*256))
        engine.mem_write(0x03009004+i*256,struct.pack('<I',0x0300A400+i*32))
    state['arraysBefore']=bytes(engine.mem_read(0x021E0468,48))
    state['beforeXY']=bytes(engine.mem_read(0x0300A000,2))
    return state


def cell_arguments003(address,vector,args):
    if address==0x021D85E4:
        args[:]=[vector%6,0x0300A000,0x0300A000 if vector//1000%2 else 0x0300A001,vector%3]
    if address==0x021D87C8:
        args[:]=[[0,1,2,3,8,14,15,49,0xFFFFFFFF][vector%9],VALUES[vector//9%5]&0xFFFFFFFF,VALUES[vector//45%5]&0xFFFFFFFF,vector//225%3]


def cells_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:
        return menu_callbacks_call003(engine,address,name,value,state)
    if not state:return value
    index=engine.reg_read(UC_ARM_REG_R0)
    if name=='func_02061944':return state['runtime']
    if name=='func_02062a10':return 0x03006000 if state['present'] else 0
    if name=='func_02044cdc':
        if index!=state['id']&0xFFFFFFFF:raise ValueError('Cell size signed record identifier differs')
        return state['count']
    if name=='func_02061dcc':return 0x03008000+(index-6)*256
    if name in {'func_02062aa0','func_02062ad0','func_020c385c','func_020c3938'}:
        return state['phase']>>['func_02062aa0','func_02062ad0','func_020c385c','func_020c3938'].index(name)&1
    if name in {'func_02062a50','func_02062a88'}:
        if not state.get('checked'):
            if bytes(engine.mem_read(0x021E0468,48))!=b'\xff'*48:raise ValueError('Four cell tables not initialized before record traversal')
            state['checked']=True
        slot=index+(3 if name=='func_02062a88' else 0)
        return 0x03007000+slot*256 if state['mask']>>slot&1 else 0
    if name in {'func_020c3828','func_020c3904'}:
        return (0xFEDCBA98 if name=='func_020c3828' else 0xFFFFFFFF)^index*0x1020304^state['vector']
    return value


def signedbyte(value):
    return ((value+128)&255)-128


def assert_cells003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_menu_callbacks003(engine,address,args,calls,state)
    if not state:return
    expected=[]
    if address==0x021D85E4:
        expected=['func_02061944','func_02062a10']
        xy=bytearray(state['beforeXY'])
        if state['present']:
            expected+=['func_02044cdc']+['func_ov003_021d87c8']*(state['count']+1)
            cells=[c for c in calls if c['name']=='func_ov003_021d87c8']
            for i,c in enumerate(cells):
                x=signedbyte(xy[0]);y=signedbyte(xy[0 if state['alias'] else 1])
                if c['args']!=[signedbyte(state['base']+3+i)&0xFFFFFFFF,x&0xFFFFFFFF,y&0xFFFFFFFF,args[3]]:raise ValueError('Per-cell signed coordinates/index/flag differ')
                xy[0 if state['alias'] else 1]=(y+5)&255
            xy[0 if state['alias'] else 1]=(xy[0 if state['alias'] else 1]+1)&255
        if bytes(engine.mem_read(0x0300A000,2))!=bytes(xy) or engine.reg_read(UC_ARM_REG_R0)!=(state['count']+1 if state['present'] else 0):raise ValueError('Cell count or coordinate progression differs')
    elif address==0x021D867C:
        expected=['func_02061dcc','func_02049f4c']*4+['func_02061dcc','func_02049ffc']*4
        for bit,getter,cell in [(0,'func_02062aa0',6),(1,'func_02062ad0',7),(2,'func_020c385c',8),(3,'func_020c3938',9)]:
            expected.append(getter)
            if not state['phase']>>bit&1:expected.append('func_0204aaf0')
        rows=[c for c in calls if c['name']=='func_02061dcc']
        if [c['args'][0] for c in rows]!=list(range(6,10))*2:raise ValueError('Four-cell traversal differs')
        for i,c in enumerate(c for c in calls if c['name']=='func_02049f4c'):
            if c['args'][0]!=0x03008000+i*256:raise ValueError('Cell reset handle differs')
        for i,c in enumerate(c for c in calls if c['name']=='func_02049ffc'):
            if c['args'][0]!=0x0300A400+i*32:raise ValueError('Nested cell release handle differs')
        rows=[c for c in calls if c['name']=='func_0204aaf0']
        for c,cell in zip(rows,[6+i for i in range(4) if not state['phase']>>i&1]):
            if c['args'][0]!=cell or c['args'][2:]!=[20,0] or bytes(engine.mem_read(c['args'][1],4))!=bytes(4) or bytes.fromhex(c['stack'])[:12]!=struct.pack('<3I',7,1,1):raise ValueError('Unavailable cell position/flags differ')
    elif address==0x021D87C8:
        nested=3<=args[0]<=14
        expected=['func_02061944']+(['native_ov003_021d87c8','func_02061944','func_02065818'] if nested else [])+['func_02065818']
        actual=[c for c in calls if c['name']=='func_02065818']
        indices=([1 if args[3] else 2] if nested else [])+[args[0]]
        for c,i in zip(actual,indices):
            if c['args'][:3]!=[(state['runtime']+16+i*12)&0xFFFFFFFF,args[1],args[2]]:raise ValueError('Recursive cell placement target/coordinates differ')
        calls=[c for j,c in enumerate(calls) if not(j==0 and c['name']=='native_ov003_021d87c8')]
    elif address==0x021D8890:
        expected=['func_020456ac']*2
        for c,layer in zip(calls,[1,2]):
            if c['args']!=[0,layer,0,0] or bytes.fromhex(c['stack'])[:8]!=struct.pack('<2I',32,24):raise ValueError('Both cell background clears differ')
    else:
        expected=['func_02062a50']*3+['func_02062a88']*3+['func_020c3828']*3+['func_020c3904']*3
        rows=[0xFFFFFFFF]*12
        for i in range(6):
            if state['mask']>>i&1:rows[i]=word(engine,0x03007014+i*256)
        for i in range(3):
            rows[9+i]=(0xFEDCBA98^i*0x1020304^state['vector'])&0xFFFFFFFF
            rows[6+i]=(0xFFFFFFFF^i*0x1020304^state['vector'])&0xFFFFFFFF
        if bytes(engine.mem_read(0x021E0468,48))!=struct.pack('<12I',*rows):raise ValueError('Four cell identifier tables differ')
        for getter in ['func_02062a50','func_02062a88','func_020c3828','func_020c3904']:
            if [c['args'][0] for c in calls if c['name']==getter]!=[0,1,2]:raise ValueError('Three-entry record traversal differs')
    if [c['name'] for c in calls]!=expected:raise ValueError('Cell management call sequence differs')
