import struct
from overlay_oracle003_mode6_fields import seed_mode6_fields003,mode6_fields_call003,assert_mode6_fields003
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3

FUNCTIONS={0x021DD074,0x021DD19C,0x021DD1B0,0x021DD22C,0x021DD28C,0x021DD5F4}
ROOT=0x021E0690
CONTEXT=0x021E06B8
PANEL=0x021E0A18
SELECT=[-2147483648,-1,0,1,2,255,2147483647]
LIMIT=[0,1,3,127,128,255]


def seed_mode6_003(engine,address,vector):
    if address not in FUNCTIONS:return seed_mode6_fields003(engine,address,vector)
    state={'vector':vector,'selected':SELECT[vector%7],'limit':LIMIT[vector//7%6],'repeat':[0,64,128,192][vector//42%4],'enabled':[0,127,128,255][vector%4],'afterEnabled':[0,1,128,255][vector//4%4],'saved':[0,1,0x80000000,0xFFFFFFFF][vector%4],'afterSaved':[0,1,0x80000000,0xFFFFFFFF][vector//4%4],'tailSaved':0xDEAD0000+vector}
    engine.mem_write(PANEL,bytes([state['enabled'],vector%7,state['limit'],vector%256])+struct.pack('<I',state['saved']));engine.mem_write(CONTEXT,struct.pack('<i',state['selected']));engine.mem_write(0x03005000,struct.pack('<4H',0,0xFFFF,0,state['repeat']))
    state.update(root=bytes(engine.mem_read(ROOT,40)),panel=bytes(engine.mem_read(PANEL,24)),context=bytes(engine.mem_read(CONTEXT,240)),input=bytes(engine.mem_read(0x03005000,8)))
    return state


def mode6_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return mode6_fields_call003(engine,address,name,value,state)
    args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]]
    if name=='func_0202a634':return 0x03005000
    if name=='func_02048e74':
        if args[:2]!=[PANEL+8,6]:raise ValueError('Mode6 SDK initialization identity differs')
        engine.mem_write(PANEL+8,struct.pack('<4I',6,0,12,12))
    if name=='func_02048fcc':
        if args[0]!=CONTEXT:raise ValueError('Mode6 cleared context identity differs')
        engine.mem_write(CONTEXT,bytes(240))
    if name=='func_ov003_021df4b4' and address in {0x021DD28C,0x021DD5F4}:
        if address==0x021DD5F4 and bytes(engine.mem_read(PANEL+2,1))!=b'\x05':raise ValueError('Mode6 customization limit not stored before resource call')
        engine.mem_write(PANEL,bytes([state['afterEnabled']]));engine.mem_write(PANEL+4,struct.pack('<I',state['afterSaved']))
    if name=='func_ov003_021ded08':engine.mem_write(CONTEXT+4,struct.pack('<I',state['vector']));engine.mem_write(PANEL,bytes([state['enabled']^0xFF]))
    if name=='func_ov003_021dec40':
        if args[:2]!=[CONTEXT,1]:raise ValueError('Mode6 formatter cursor/reset identity differs')
        engine.mem_write(CONTEXT+16,bytes([state['afterEnabled']]))
    if name=='func_ov003_021deda4':engine.mem_write(CONTEXT+8,struct.pack('<I',state['vector']^0x1234))
    if name=='func_ov003_021dfd18' and address==0x021DD28C:engine.mem_write(PANEL+4,struct.pack('<I',state['tailSaved']))
    return value


def assert_mode6_003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_mode6_fields003(engine,address,args,calls,state)
    panel=bytearray(state['panel']);context=bytearray(state['context']);expected=[];checks={};selected=state['selected']
    if address==0x021DD074:
        expected=['func_02048e74','func_ov003_021dad9c','func_02048fcc'];panel[8:24]=struct.pack('<4I',6,0,12,12);context[:]=bytes(240)
    elif address==0x021DD19C:expected=['func_ov003_021df4b4','func_ov003_021dfccc'];checks={'func_ov003_021df4b4':[1]}
    elif address==0x021DD1B0:
        expected=['func_0202a634','func_ov003_021dad9c']
        if state['repeat']&64:selected=selected-1 if selected>0 else state['limit']
        elif state['repeat']&128:selected=selected+1 if selected<state['limit'] else 0
        if state['repeat']&192:expected.append('func_0205e7a8')
        struct.pack_into('<i',context,0,selected);checks={'func_0205e7a8':[0xFFFFFFFF,85]}
    elif address==0x021DD22C:
        expected=['func_ov003_021dad9c','func_ov003_021ded08','func_ov003_021dad9c','func_ov003_021dec40','func_020620b4','func_02062358'];struct.pack_into('<I',context,4,state['vector']);context[16]=state['afterEnabled'];panel[0]=state['enabled']^0xFF
        c=next(c for c in calls if c['name']=='func_ov003_021ded08')
        if c['args']!=[CONTEXT,4,16,1] or bytes.fromhex(c['stack'])!=struct.pack('<4I',3,30,2,0):raise ValueError('Mode6 initial formatter geometry/stack flags differ')
        checks={'func_020620b4':[39],'func_02062358':[1]}
    else:
        expected=['func_ov003_021dad9c','func_ov003_021df4b4'];panel[0]=state['afterEnabled'];struct.pack_into('<I',panel,4,state['afterSaved']);panel[2]=3 if address==0x021DD28C else 5
        checks['func_ov003_021df4b4']=[3 if address==0x021DD28C or state['saved'] else 4]
        enabled=state['afterEnabled']
        if address==0x021DD5F4 and state['afterSaved']:
            expected.append('func_ov003_021ded08');struct.pack_into('<I',context,4,state['vector']);enabled=state['enabled']^0xFF;panel[0]=enabled;struct.pack_into('<I',panel,4,0)
            c=next(c for c in calls if c['name']=='func_ov003_021ded08')
            if c['args']!=[CONTEXT,45,16,2] or bytes.fromhex(c['stack'])!=struct.pack('<4I',5,29,2,1):raise ValueError('Mode6 saved customization cursor conditional geometry differs')
        expected+=['func_ov003_021deda4','func_ov003_021dfd18'];struct.pack_into('<I',context,8,state['vector']^0x1234)
        if address==0x021DD28C:struct.pack_into('<I',panel,4,0)
        c=next(c for c in calls if c['name']=='func_ov003_021deda4')
        if c['args']!=[CONTEXT,4 if address==0x021DD28C else 6,0x021E0394 if address==0x021DD28C else 0x021E03A8,2] or bytes.fromhex(c['stack'])[:12]!=struct.pack('<3I',6 if address==0x021DD28C else 8,28,enabled):raise ValueError('Mode6 formatter captured cursor/fresh enabled-byte arguments differ')
        checks['func_ov003_021dfd18']=[1]
    if [c['name'] for c in calls]!=expected:raise ValueError('Mode6 independent callback order differs')
    for c in calls:
        if c['name'] in checks and c['args'][:len(checks[c['name']])]!=checks[c['name']]:raise ValueError('Mode6 independent callback arguments differ')
    for pointer,data in [(PANEL,panel),(CONTEXT,context),(ROOT,state['root']),(0x03005000,state['input'])]:
        if bytes(engine.mem_read(pointer,len(data)))!=bytes(data):raise ValueError('Mode6 complete panel/cursor/input effects differ')
