import struct
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3

from overlay_oracle003_mode7_flow import seed_mode7_flow003,mode7_flow_call003,assert_mode7_flow003

FUNCTIONS={0x021DBE4C,0x021DBED8,0x021DBF68,0x021DC060,0x021DC138,0x021DC1C0,0x021DC1E8}
ROOT=0x021E0690
GROUP=0x021E07CC
CONTEXT=0x021E06B8
OPTIONS=[0,1,2,3,4,5,0xFFFFFFFF]


def parameters(address,vector):
    state={'vector':vector,'pressed':0,'action':0,'wait':0,'changed':0,'option':vector%5,'busy':0,'post':0}
    if address==0x021DBF68:
        v=vector;state['pressed']=v%8;v//=8;state['action']=[0,1,2,0xFFFFFFFF][v%4];v//=4;state['wait']=[0,2,0xFFFFFFFF][v%3];v//=3;state['changed']=v%2;v//=2;state['option']=v%5
    elif address==0x021DC060:
        v=vector;state['busy']=[0,1,255,256,0xFFFFFFFF][v%5];v//=5;state['action']=[0,1,2,3,0xFFFFFFFF][v%5];v//=5;state['wait']=[0,1,2,0xFFFFFFFF][v%4];v//=4;state['post']=v%8
    return state


def seed_mode3_network003(engine,address,vector):
    if address not in FUNCTIONS:return seed_mode7_flow003(engine,address,vector)
    state=parameters(address,vector);engine.mem_write(ROOT+4,struct.pack('<I',0x0300D000));engine.mem_write(0x03005000,struct.pack('<2H',0,state['pressed']))
    state.update(root=bytes(engine.mem_read(ROOT,40)),group=bytes(engine.mem_read(GROUP,20)),context=bytes(engine.mem_read(CONTEXT,240)),heap=[0,2,0xFFFFFFFF][vector%3],size=vector%65,bank=vector%4,buffer=bytes(engine.mem_read(0x0300D000,2048)),payload=bytes(engine.mem_read(0x0300C000,65)),id=[0,1,0x80000000,0xFFFFFFFF][vector%4],fallback=[0,0x76543210][vector//4%2],present=vector//8%2,arrays=[],flags=[])
    state['callbacks']={target:name for target,name in [(0x0202A250,'func_0202a250'),(0x0203CC2C,'func_0203cc2c'),(0x0204518C,'func_0204518c'),(0x02008E0C,'func_02008e0c'),(0x02045994,'func_02045994'),(0x0202A498,'func_0202a498'),(0x02008D78,'func_02008d78'),(0x020C3790,'func_020c3790'),(0x020C386C,'func_020c386c'),(0x0206BC80,'func_0206bc80'),(0x020C384C,'func_020c384c'),(0x0206BD24,'func_0206bd24'),(0x020C3928,'func_020c3928'),(0x02041538,'func_02041538'),(0x020C48BC,'func_020c48bc'),(0x020C48D0,'func_020c48d0'),(0x02048F7C,'func_02048f7c'),(0x020C484C,'func_020c484c'),(0x020C48E8,'func_020c48e8')]}
    return state


def mode3_network_arguments003(address,vector,args):
    if address==0x021DBED8:args[0]=OPTIONS[vector%7]


def mode3_network_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return mode7_flow_call003(engine,address,name,value,state)
    args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]]
    if name=='func_0202a634':return 0x03005000
    if name=='func_020698f4':return state['action']
    if name=='func_0206a04c':return state['wait']
    if name=='func_020c1540':return state['busy']
    if name=='func_0206a0fc':return state['action']
    if name=='func_0206a49c':return state['wait']
    if name in {'func_0206c0b0','func_0206c0e0','func_020c17b0'}:return 0xFFFFFFFF if state['post']>>['func_0206c0b0','func_0206c0e0','func_020c17b0'].index(name)&1 else 0
    if name=='func_020c1708':
        if address==0x021DBE4C:
            if bytes(engine.mem_read(args[0],4))!=b'\xff'*4:raise ValueError('Network selection local not initialized to sentinel')
            engine.mem_write(args[0],struct.pack('<I',state['option']))
        else:
            if args[0]!=GROUP:raise ValueError('Network selected-state storage identity differs')
            engine.mem_write(GROUP,struct.pack('<I',state['option']))
        return state['changed']
    if name in {'func_02048f8c','func_02048f7c'}:return state['bank']
    if name=='func_0202a250':return state['heap']
    if name=='func_0203cc2c':
        if args[:2]!=[0x021E032C,state['heap']]:raise ValueError('Network setup resource archive/heap differs')
        return 0x0300F000
    if name=='func_0204518c':
        if args[1:3]!=[0x0300F000,12]:raise ValueError('Network setup resource section differs')
        engine.mem_write(args[0],struct.pack('<2I',0x0300C000,state['size']))
    if name=='func_020c3828':
        if args[0]!=0:raise ValueError('Network setup initial roster selector differs')
        return 0xABC00000+state['vector']
    if name=='func_0206be2c':return state['id']
    if name=='func_0206bf34':return state['fallback']
    if name=='func_02062a10':return 0x03006000 if state['present'] else 0
    if name in {'func_020c3790','func_020c386c'}:state['arrays'].append((name,bytes(engine.mem_read(args[0],12))))
    if name in {'func_0206bc80','func_0206bd24'}:
        second=name=='func_0206bd24';ids=[0x80000000+state['vector'],0xFFFFFFFF if second else 0,0 if second else 0xFFFFFFFF];flag=[0,127,128,255][(state['vector']+int(second))%4]
        engine.mem_write(args[0],struct.pack('<3I',*ids));engine.mem_write(args[1],bytes([flag]));state['flags'].append(flag)
    return value


def selection_success_calls():return ['func_ov003_021dc138','func_02008d78','func_020c3790','func_020c386c','func_0206bc80','func_020c3790','func_020c384c','func_0206bd24','func_020c3928','func_020c386c','func_02041538']


def assert_mode3_network003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_mode7_flow003(engine,address,args,calls,state)
    group=bytearray(state['group']);expected=[];sounds=[];phase=None;success=False;result=None
    if address==0x021DBE4C:
        expected=['func_ov003_021dad9c','func_ov003_021deb78','func_ov003_021dad9c','func_ov003_021dec40','func_ov003_021dad9c','func_ov003_021df190','func_ov003_021dfe30','func_020c17e8','func_020c1708','func_02048f8c','func_ov003_021dad1c','func_0202a250','func_0203cc2c','func_0204518c','func_02008e0c','func_02045994','func_0202a498','func_ov003_021dfda8','func_020625ac','func_020620b4','func_020c3828','func_02062a10','func_0206dcd0','func_02062358']
        buffer=state['payload'][:state['size']]+state['buffer'][state['size']:]
        if bytes(engine.mem_read(0x0300D000,2048))!=buffer:raise ValueError('Network setup connected native copy/allocation extent differs')
    elif address==0x021DBED8:
        expected=['func_020c48bc']+(['func_020c48d0'] if args[0] in range(1,5) else [])+['func_02048f7c','func_020c484c','func_020c48e8']
    elif address==0x021DBF68:
        expected=['func_0202a634','func_0206940c']
        if state['pressed']&1:
            expected.append('func_020698f4')
            if state['action']==1:expected+=selection_success_calls()+['func_0205e7a8'];phase=3;success=True;sounds.append([0xFFFFFFFF,82])
            elif state['action']==2:expected+=['func_ov003_021dc1c0','func_02041538','func_0205e7a8'];phase=4;sounds.append([0xFFFFFFFF,83])
            else:
                expected.append('func_0206a04c')
                if state['wait']==2:expected+=['func_ov003_021df150','func_020c485c','func_02068f60'];phase=2
        elif state['pressed']&2:expected.append('func_0206a06c')
        if state['pressed']&4:
            expected.append('func_020c1708');struct.pack_into('<I',group,0,state['option'])
            if state['changed']:
                expected+=['func_ov003_021dbed8','func_020c48bc']+(['func_020c48d0'] if state['option'] in range(1,5) else [])+['func_02048f7c','func_020c484c','func_020c48e8','func_0206be2c','func_02062a10','func_0206dcd0','func_02068f60'];phase=2
    elif address==0x021DC060:
        expected=['func_020c1540'];busy=state['busy']&255
        if not busy:
            expected.append('func_0206a0fc')
            if state['action']==1:expected+=selection_success_calls()+['func_0205e7a8'];phase=3;success=True;sounds.append([0xFFFFFFFF,82])
            elif state['action']==2:expected+=['func_ov003_021dc1c0','func_02041538','func_0205e7a8'];phase=4;sounds.append([0xFFFFFFFF,83])
            else:
                expected.append('func_0206a49c')
                if state['wait']==1:expected+=['func_ov003_021df150','func_020c485c','func_02068f60'];phase=2
                elif state['wait']==2:expected.append('func_0205e7a8');sounds.append([0xFFFFFFFF,84])
        for bit,name in enumerate(['func_0206c0b0','func_0206c0e0','func_020c17b0']):
            expected.append(name)
            if state['post']>>bit&1:break
        result=int(bool(state['post'] or busy))
    elif address==0x021DC138:expected=selection_success_calls()[1:];phase=3;success=True
    elif address==0x021DC1C0:expected=['func_02041538'];phase=4
    else:
        expected=['func_0206be2c']+([] if state['id'] else ['func_0206bf34'])+['func_02062a10','func_0206dcd0']
    if phase is not None:struct.pack_into('<I',group,8,phase)
    if success:
        first=struct.pack('<3I',0x80000000+state['vector'],0,0xFFFFFFFF);second=struct.pack('<3I',0x80000000+state['vector'],0xFFFFFFFF,0)
        if state['arrays']!=[('func_020c3790',bytes(12)),('func_020c386c',bytes(12)),('func_020c3790',first),('func_020c386c',second)]:raise ValueError('Network accepted roster zero/update/capture sequence differs')
        if [c['args'][0] for c in calls if c['name']=='func_020c384c']!=state['flags'][:1] or [c['args'][0] for c in calls if c['name']=='func_020c3928']!=state['flags'][1:]:raise ValueError('Network accepted roster byte selector propagation differs')
    if [c['args'][:2] for c in calls if c['name']=='func_0205e7a8']!=sounds:raise ValueError('Network decision sound precedence differs')
    if result is not None and engine.reg_read(UC_ARM_REG_R0)!=result:raise ValueError('Network truncated busy/short-circuit status result differs')
    for c in calls:
        values={'func_ov003_021deb78':[CONTEXT,14],'func_ov003_021dec40':[CONTEXT,0],'func_ov003_021df190':[CONTEXT],'func_020c17e8':[0,0],'func_ov003_021dad1c':[12,state['bank']],'func_02008e0c':[0x0300C000,0x0300D000,state['size']],'func_02045994':[state['bank'],0x0300D000,0,2048],'func_0202a498':[state['heap'],0x0300F000],'func_ov003_021dfda8':[1],'func_020625ac':[1],'func_020620b4':[1],'func_02062358':[1],'func_02041538':[1,2,10],'func_ov003_021df150':[3,0xFFFFFFFF],'func_02068f60':[0],'func_0206a06c':[1],'func_020c484c':[state['bank']],'func_020c48e8':[87]}
        if c['name'] in values and c['args'][:len(values[c['name']])]!=values[c['name']]:raise ValueError('Network setup/transition/resource arguments differ')
        if c['name']=='func_020c48d0':
            option=args[0] if address==0x021DBED8 else state['option']
            if c['args'][:3]!=[5,6,{1:27,2:28,3:29,4:48}[option]]:raise ValueError('Network popup option mapping differs')
        if c['name']=='func_0206dcd0' and c['args'][0]!=(0x03006000 if state['present'] else 0):raise ValueError('Network selected record pointer forwarding differs')
        if c['name']=='func_02062a10':
            identifier=0xABC00000+state['vector'] if address==0x021DBE4C else state['id'] or state['fallback'] if address==0x021DC1E8 else state['id']
            if c['args'][0]!=identifier:raise ValueError('Network current/fallback record identifier differs')
    if [c['name'] for c in calls]!=expected or bytes(engine.mem_read(GROUP,20))!=bytes(group) or bytes(engine.mem_read(ROOT,40))!=state['root'] or bytes(engine.mem_read(CONTEXT,240))!=state['context']:raise ValueError('Mode3 network complete state/context/call order differs')
