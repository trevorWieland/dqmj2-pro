import struct
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1

from overlay_oracle003_mode7_setup import seed_mode7_setup003,mode7_setup_arguments003,mode7_setup_call003,assert_mode7_setup003

FUNCTIONS={0x021DC214,0x021DC258,0x021DC500}
MODE=0x021E07E0
DISPLAY=0x021E07F4
PRIMARY=0x021E07FC
SECONDARY=0x021E08EC
CONTEXT=0x021E06B8
POSITIONS=[(count,index) for count in [1,2,4,7] for index in range(count)]
CHOICES=[0,1,255,256,0xFFFFFFFF]
PRESS=[0,1,2,3,0x800,0x801,0x802]


def parameters(vector):
    state={'phase':0,'protocol':[0,1,2,255][vector%4],'changed':0,'pressed':0,'count':7,'index':vector%7,'choice':CHOICES[vector%5],'move':CHOICES[(vector+1)%5],'fade':vector//3%2,'mode':[0,7,0xFFFFFFFF][vector%3]}
    if 12<=vector<908:
        v=vector-12;state['protocol']=[0,1,2,255][v%4];v//=4;state['changed']=v%2;v//=2;state['pressed']=v%4;v//=4;state['count'],state['index']=POSITIONS[v%14];v//=14;state['phase']=1+v%2
    elif 908<=vector<1608:
        v=vector-908;state['changed']=v%2;v//=2;state['pressed']=PRESS[v%7];v//=7;state['move']=CHOICES[v%5];v//=5;state['choice']=CHOICES[v%5];v//=5;state['phase']=3+v%2
    elif vector>=1608:state['phase']=5
    return state


def seed_mode7_flow003(engine,address,vector):
    if address not in FUNCTIONS:return seed_mode7_setup003(engine,address,vector)
    state=parameters(vector);state['vector']=vector
    engine.mem_write(MODE+1,bytes([state['protocol']]))
    before=bytearray(engine.mem_read(DISPLAY,532));struct.pack_into('<I',before,0,state['phase']);struct.pack_into('<I',before,8,state['index']);struct.pack_into('<H',before,20,state['count']);struct.pack_into('<I',before,248,state['choice']);struct.pack_into('<I',before,488,0x03006000+(vector%6)*256)
    recordPointers=[0x03006000+i*256 if i<state['count']-1 else 0 for i in range(8)];struct.pack_into('<8I',before,500,*recordPointers);engine.mem_write(DISPLAY,bytes(before));engine.mem_write(0x03005000,struct.pack('<2H',0,state['pressed']))
    state.update(display=bytes(before),modeBefore=bytes(engine.mem_read(MODE,20)),context=bytes(engine.mem_read(CONTEXT,240)),records={p:bytes(engine.mem_read(p,132)) for p in [0x03006000+i*256 for i in range(6)]},recordPointers=recordPointers)
    return state


def word(engine,address):return int.from_bytes(engine.mem_read(address,4),'little')


def mode7_flow_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return mode7_setup_call003(engine,address,name,value,state)
    first=engine.reg_read(UC_ARM_REG_R0)
    if name=='func_02048e74':
        if [first,engine.reg_read(UC_ARM_REG_R1)]!=[MODE+4,7]:raise ValueError('Mode7 SDK state initialization identity differs')
        engine.mem_write(MODE+4,struct.pack('<4I',7,0,12,12))
    if name=='func_02048fcc':
        if first!=CONTEXT:raise ValueError('Mode7 reset context getter differs')
        engine.mem_write(CONTEXT,bytes(240))
    if name=='func_0202a634':return 0x03005000
    if name=='func_02049f24':engine.mem_write(MODE+4,struct.pack('<I',state['mode']))
    if name=='func_ov003_021dc52c':engine.mem_write(DISPLAY,struct.pack('<I',1));engine.mem_write(MODE+4,struct.pack('<I',state['mode']^0x100))
    if name=='func_ov003_021dc6c0':
        if first==2:engine.mem_write(PRIMARY,struct.pack('<I',(word(engine,PRIMARY)+1)%state['count']))
        elif first==4:engine.mem_write(SECONDARY,struct.pack('<I',(word(engine,SECONDARY)+1)&0xFFFFFFFF))
        else:raise ValueError('Mode7 layout rebuild type differs')
        engine.mem_write(MODE+4,struct.pack('<I',state['mode']^0x200))
    if name=='func_02041944':return state['fade']
    if name=='func_020491f8':
        if first not in [PRIMARY,SECONDARY]:raise ValueError('Mode7 primary/secondary cursor identity differs')
        if state['changed']:engine.mem_write(first,struct.pack('<I',(word(engine,first)+1)%state['count'] if first==PRIMARY else state['move']))
        return state['changed']
    if name=='func_ov003_021dcbc4':engine.mem_write(DISPLAY,struct.pack('<I',5))
    if name=='func_ov003_021dcc8c':engine.mem_write(DISPLAY,struct.pack('<I',4))
    return value


def simulate(state):
    display=bytearray(state['display']);mode=bytearray(state['modeBefore']);context=bytearray(state['context']);records={p:bytearray(data) for p,data in state['records'].items()};calls=['func_0202a634','func_02049f24'];arguments={};result=state['mode'];render=True;active=0
    struct.pack_into('<I',mode,4,result)
    def get(offset):return int.from_bytes(display[offset:offset+4],'little')
    def put(offset,value):struct.pack_into('<I',display,offset,value&0xFFFFFFFF)
    def call(name,args=None):
        calls.append(name)
        if args is not None:arguments.setdefault(name,[]).append(args)
    for iteration in range(3):
        again=False;phase=get(0)
        if phase==0:call('func_ov003_021dc52c');put(0,1);struct.pack_into('<I',mode,4,result^0x100);call('func_ov003_021dad9c');call('func_ov003_021debd8',[CONTEXT,5,0,5]);render=False
        elif phase==1:
            active=PRIMARY;call('func_ov003_021df4b4',[1]);call('func_ov003_021dc6c0',[2]);put(8,(get(8)+1)%state['count']);struct.pack_into('<I',mode,4,result^0x200);call('func_0206dcd0',[state['recordPointers'][get(8)]]);call('func_02041944')
            if state['fade']:call('func_02041538',[0,2,10])
            put(0,2);again=True
        elif phase==2:
            active=PRIMARY;call('func_020491f8',[PRIMARY])
            if state['changed']:put(8,(get(8)+1)%state['count']);call('func_0206dcd0',[state['recordPointers'][get(8)]]);call('func_ov003_021dccd4',[PRIMARY]);call('func_0205e7a8',[0xFFFFFFFF,85])
            if state['pressed']&1:
                selected=get(8)
                if selected!=state['count']-1:put(0,3);put(488,state['recordPointers'][selected]);call('func_0205e7a8',[0xFFFFFFFF,82])
                else:
                    result={0:4,1:1}.get(state['protocol'],result);call('func_02041538',[1,2,10]);call('func_0205e7a8',[0xFFFFFFFF,83])
            elif state['pressed']&2:result={0:4,1:1}.get(state['protocol'],result);call('func_0205e7a8',[0xFFFFFFFF,83]);call('func_02041538',[1,2,10])
        elif phase==3:active=SECONDARY;call('func_ov003_021df4b4',[1]);call('func_ov003_021dc6c0',[4]);put(248,get(248)+1);struct.pack_into('<I',mode,4,result^0x200);put(0,4);again=True
        elif phase==4:
            active=SECONDARY;call('func_020491f8',[SECONDARY])
            if state['changed']:put(248,state['move']);call('func_0205e7a8',[0xFFFFFFFF,85])
            if state['pressed']&1:records[get(488)][50]=get(248)&255;put(0,1);call('func_0205e7a8',[0xFFFFFFFF,82])
            elif state['pressed']&2:put(0,1);call('func_0205e7a8',[0xFFFFFFFF,83])
            elif state['pressed']&0x800:call('func_ov003_021dcbc4');put(0,5)
        elif phase==5:active=SECONDARY;call('func_ov003_021dcc8c');put(0,4)
        if render:call('func_ov003_021dccd4',[active])
        if not again:break
    else:raise ValueError('Independent Mode7 loop bound reached')
    return bytes(display),bytes(mode),bytes(context),records,calls,arguments,result


def assert_mode7_flow003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_mode7_setup003(engine,address,args,calls,state)
    display=bytearray(state['display']);mode=bytearray(state['modeBefore']);context=bytearray(state['context']);records={p:bytearray(data) for p,data in state['records'].items()}
    if address==0x021DC214:
        expected=['func_02048e74','func_ov003_021dad9c','func_02048fcc','func_ov003_021df518','func_0206258c'];mode[4:20]=struct.pack('<4I',7,0,12,12);display[:8]=struct.pack('<2I',0,7);context[:]=bytes(240);arguments={'func_0206258c':[[0]]};result=None
    elif address==0x021DC500:expected=['func_020625ac','func_0206258c','func_ov003_021df518','func_ov003_021dfccc','func_ov003_021dad9c','func_ov003_021deb78'];arguments={'func_020625ac':[[0]],'func_0206258c':[[1]],'func_ov003_021deb78':[[CONTEXT,0]]};result=None
    else:display,mode,context,records,expected,arguments,result=simulate(state)
    if [c['name'] for c in calls]!=expected or bytes(engine.mem_read(DISPLAY,532))!=bytes(display) or bytes(engine.mem_read(MODE,20))!=bytes(mode) or bytes(engine.mem_read(CONTEXT,240))!=bytes(context):raise ValueError('Mode7 complete phase/cursor/callback/context effects differ')
    if any(bytes(engine.mem_read(p,132))!=bytes(data) for p,data in records.items()):raise ValueError('Mode7 selected-record byte mutation/preservation differs')
    if result is not None and engine.reg_read(UC_ARM_REG_R0)!=result:raise ValueError('Mode7 captured/exit protocol result differs')
    for name,values in arguments.items():
        actual=[c for c in calls if c['name']==name]
        if [c['args'][:len(value)] for c,value in zip(actual,values)]!=values:raise ValueError('Mode7 cursor/record/fade/sound forwarding differs')
