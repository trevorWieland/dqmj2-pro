import struct
from overlay_oracle003_mode2 import seed_mode2_003,mode2_call003,assert_mode2_003
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP

FUNCTIONS={0x021DCAEC,0x021DCBC4,0x021DCC8C,0x021DCCC4,0x021DCCD4}
DISPLAY=0x021E07F4
MODE=0x021E07E0
VALUES=[0,1,127,128,247,248,255,256,0xFFFFFFFF]


def s8(value):return ((value+128)%256-128)&0xFFFFFFFF


def seed_mode7_helpers003(engine,address,vector):
    if address not in FUNCTIONS:return seed_mode2_003(engine,address,vector)
    state={'vector':vector,'selected':VALUES[vector%9],'index':VALUES[vector//9%9],'first':[0,1,127,128,255][vector//81%5],'species':[-32768,-1,0,1,32767][vector%5],'marker':[0,127,128,255][vector//5%4],'frame':VALUES[vector//9%9],'present':vector//81%2,'changed':vector//162%2,'pressed':[0,1,2,4,8,0x800,0x1000,0xFFFF][vector%8],'mode':vector%256}
    engine.mem_write(DISPLAY+493,bytes([state['first']]));engine.mem_write(DISPLAY+248,struct.pack('<I',state['selected']^0xFF));engine.mem_write(0x03006000+24,struct.pack('<h',state['species']));engine.mem_write(0x03006000+50,bytes([state['marker']]))
    engine.mem_write(0x03008000,struct.pack('<2I',0x03009000,0x0300E000));engine.mem_write(0x03009000+4,struct.pack('<I',0x0300A000));engine.mem_write(0x0300A000+94,bytes([state['marker']]));engine.mem_write(0x0300A000+104,struct.pack('<I',state['selected']))
    engine.mem_write(0x0300B000,struct.pack('<2I',0x0300C000 if state['present'] else 0,0x0300D000));engine.mem_write(0x03005000,struct.pack('<2H',0,state['pressed']))
    state.update(display=bytes(engine.mem_read(DISPLAY,532)),modeBefore=bytes(engine.mem_read(MODE,20)),record=bytes(engine.mem_read(0x03006000,132)),current=bytes(engine.mem_read(0x0300B000,8)),cursor=bytes(engine.mem_read(0x03007000,32)),positions=[])
    return state


def mode7_helpers_arguments003(address,vector,args):
    if address==0x021DCAEC:args[:2]=[0x03006000,VALUES[vector//9%9]]
    if address==0x021DCCC4:args[0]=VALUES[vector%9]
    if address==0x021DCCD4:args[0]=0x03007000


def mode7_helpers_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return mode2_call003(engine,address,name,value,state)
    args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]];sp=engine.reg_read(UC_ARM_REG_SP)
    if name=='func_ov003_021de854':return 0x0300F000+args[0]*16
    if name=='func_02049ad0':return 0x03008000
    if name=='func_02049ae4':return 0x0300B000
    if name=='func_02049f24':return state['frame']
    if name=='func_02049f30':engine.mem_write(DISPLAY+248,struct.pack('<I',state['selected']))
    if name=='func_02049f14':engine.mem_write(0x0300B000,struct.pack('<I',0x0300C000 if state['changed'] else 0))
    if name=='func_02049ffc':engine.mem_write(0x03006000+24,struct.pack('<h',-state['species'] if state['species']!=-32768 else 32767))
    if name=='func_020602ec':engine.mem_write(0x03006000+50,bytes([state['marker']^0xFF]))
    if name=='func_0204a724':
        state['positions'].append(bytes(engine.mem_read(args[1],4)));engine.mem_write(args[1],struct.pack('<2h',-32768,32767))
    if name=='func_0202a634':return 0x03005000
    if name=='func_ov003_021df6ac':
        if args[0]!=0x03007000 or bytes(engine.mem_read(args[0]+16,1))!=b'\x07':raise ValueError('Mode7 cursor mode byte not set before reset')
        engine.mem_write(MODE,bytes([state['mode']]));engine.mem_write(args[0]+20,struct.pack('<I',state['selected']))
    if name=='func_ov003_021df830':
        if bytes(engine.mem_read(sp,8))!=struct.pack('<2I',28,28):raise ValueError('Mode7 cursor signed geometry stack arguments differ')
        engine.mem_write(args[0]+24,struct.pack('<I',state['index']))
    return value


def assert_mode7_helpers003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_mode2_003(engine,address,args,calls,state)
    display=bytearray(state['display']);mode=bytearray(state['modeBefore']);record=bytearray(state['record']);current=bytearray(state['current']);cursor=bytearray(state['cursor']);expected=[];checks={}
    if address==0x021DCAEC:
        expected=['func_ov003_021de854','func_02049ad0','func_02049ffc','func_02049f4c','func_020602ec','func_0204a724','func_02065818'];label=7 if state['index']<state['first'] else 8;species=-state['species'] if state['species']!=-32768 else 32767
        struct.pack_into('<h',record,24,species);record[50]=state['marker']^0xFF
        checks={'func_ov003_021de854':[label],'func_02049ad0':[5],'func_02049ffc':[0x0300A000],'func_02049f4c':[0x03008000],'func_020602ec':[0x03009000,species&0xFFFFFFFF,0x03006000,24],'func_0204a724':[5],'func_02065818':[0x0300F000+label*16,3,3]}
        c=next(c for c in calls if c['name']=='func_020602ec')
        if bytes.fromhex(c['stack'])[:8]!=struct.pack('<2I',0,1):raise ValueError('Mode7 row record renderer flags differ')
        c=next(c for c in calls if c['name']=='func_0204a724')
        if c['args'][2:]!=[24,0] or bytes.fromhex(c['stack'])!=struct.pack('<4I',1,state['marker']^0xFF,1,0) or state['positions']!=[bytes(4)]:raise ValueError('Mode7 row marker reload/position/stack forwarding differs')
    elif address==0x021DCBC4:
        expected=['func_02049ae4','func_02049f24','func_02049f30','func_02049ad0','func_02046af4','func_02049f14','func_ov003_021dea38','func_ov003_021dfd18']+(['func_020853c8'] if state['changed'] else []);struct.pack_into('<I',display,248,state['selected']);struct.pack_into('<I',display,0,5);struct.pack_into('<I',current,0,0x0300C000 if state['changed'] else 0)
        checks={'func_02049ad0':[s8(state['selected']+8)],'func_02046af4':[0x021C9698,state['selected'],state['marker'],0],'func_02049f14':[state['frame']],'func_ov003_021dea38':[0,1,(state['selected']%256+8),1],'func_ov003_021dfd18':[0],'func_020853c8':[0x0300D000,0x0300C000]}
        for name,stack in [('func_02046af4',[state['frame'],255]),('func_ov003_021dea38',[1,87])]:
            c=next(c for c in calls if c['name']==name)
            if bytes.fromhex(c['stack'])[:8]!=struct.pack('<2I',*stack):raise ValueError('Mode7 popup captured frame/message stack arguments differ')
    elif address==0x021DCC8C:
        expected=['func_0202a634']
        if state['pressed']&0xFF7:expected.append('func_ov003_021df668');struct.pack_into('<I',display,0,4)
        checks={'func_ov003_021df668':[1]}
    elif address==0x021DCCC4:mode[1]=args[0]%256
    else:
        expected=['func_ov003_021df6ac','func_ov003_021df830','func_ov003_021dff60'];cursor[16]=7;struct.pack_into('<I',cursor,20,state['selected']);struct.pack_into('<I',cursor,24,state['index']);mode[0]=state['mode']
        checks={'func_ov003_021df6ac':[0x03007000],'func_ov003_021df830':[0x03007000,s8(state['mode']),s8(state['mode']+8),s8(state['mode']+15)],'func_ov003_021dff60':[0x03007000]}
    if [c['name'] for c in calls]!=expected:raise ValueError('Mode7 helper callback order differs')
    for c in calls:
        if c['name'] in checks and c['args'][:len(checks[c['name']])]!=checks[c['name']]:raise ValueError('Mode7 helper independent forwarding differs: '+c['name'])
    for pointer,data in [(DISPLAY,display),(MODE,mode),(0x03006000,record),(0x0300B000,current),(0x03007000,cursor)]:
        if bytes(engine.mem_read(pointer,len(data)))!=bytes(data):raise ValueError('Mode7 helper complete state preservation/effects differ')
