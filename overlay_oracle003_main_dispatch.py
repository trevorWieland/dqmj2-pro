import struct
from unicorn.arm_const import UC_ARM_REG_R0

from overlay_oracle003_modes13 import seed_modes13_003,modes13_call003,assert_modes13_003

ROOT=0x021E0690
MODES=[(0x021DADC4,0x021DAE50,0x021DAF7C),(0x021DB9BC,0x021DBA20,0x021DBAE4),(0x021DCD3C,0x021DCD84,0x021DCE34),(0x021DBCA0,0x021DBD18,0x021DBDEC),(0x021DE09C,0x021DE0F0,0x021DE180),(0x021DE378,0x021DE3D4,0x021DE484),(0x021DD074,0x021DD0A4,0x021DD19C),(0x021DC214,0x021DC258,0x021DC500)]
MAIN_INDIRECT_003={target:f'func_ov003_{target:08x}' for row in MODES for target in row}
TIMERS=[-128,-1,0,1,2,5,79,80,127]
BUTTONS=[0,*[1<<i for i in range(16)],0xFF7,0xFFFF]


def signed(value):return ((value+128)&255)-128


def parameters(vector):
    state={'current':vector%8,'phase':99,'next':vector%12,'timer':TIMERS[vector%9],'busy':0,'ready':1,'first':0,'second':0,'buttons':0,'connection':0,'scene':12,'vector':vector}
    if vector<1152:
        v=vector;state['phase']=v%2;v//=2;state['current']=v%8;v//=8;state['next']=v%12;v//=12;state['busy']=v%2;v//=2;state['ready']=[0,1,0xFFFFFFFF][v%3]
    elif vector<1248:
        v=vector-1152;state.update(phase=2,current=v%8,next=v//8%12)
    elif vector<1824:
        v=vector-1248;state['phase']=3;state['current']=v%8;v//=8;state['next']=v%12;v//=12;state['busy']=v%2;v//=2;state['ready']=[0,1,0xFFFFFFFF][v%3]
    elif vector<1878:
        v=vector-1824;state.update(phase=4,timer=TIMERS[v%9],first=[0,5,1][v//9%3],second=v//27%2)
    elif vector<2049:
        v=vector-1878;state.update(phase=5,timer=TIMERS[v%9],buttons=BUTTONS[v//9%19])
    elif vector<2057:state['phase']=6
    elif vector<2089:
        v=vector-2057;state.update(phase=7,current=v%8,connection=3 if v//8%2 else 0,scene=0 if v//16%2 else 12)
    elif vector<2113:state['phase']=8+(vector-2089)//8
    return state


def word(engine,offset):return int.from_bytes(engine.mem_read(ROOT+offset,4),'little')


def seed_main_dispatch003(engine,address,vector):
    if address!=0x021DA50C:return seed_modes13_003(engine,address,vector)
    if bytes(engine.mem_read(0x021E0160,108))!=b''.join(struct.pack('<3I',*row) for row in MODES)+bytes(12):raise ValueError('Overlay003 main callback table identity differs')
    state=parameters(vector);before=bytearray(engine.mem_read(ROOT,40));before[0]=state['timer']&255;struct.pack_into('<4I',before,24,state['current'],state['phase'],state['next'],0xABC00000+vector);engine.mem_write(ROOT,bytes(before));engine.mem_write(0x03005000,struct.pack('<2H',0,state['buttons']))
    state.update(before=bytes(before),queries=0,callbacks=MAIN_INDIRECT_003)
    return state


def main_dispatch_call003(engine,address,name,value,state):
    if address!=0x021DA50C:return modes13_call003(engine,address,name,value,state)
    for row,handlers in enumerate(MODES):
        if name==MAIN_INDIRECT_003[handlers[0]]:
            if state['vector']%2:engine.mem_write(ROOT+24,struct.pack('<I',(row+1)%8))
            engine.mem_write(ROOT+28,struct.pack('<I',99));return value
        if name==MAIN_INDIRECT_003[handlers[1]]:
            if state['vector']%7==0:engine.mem_write(ROOT+24,struct.pack('<I',(row+1)%8))
            return state['next']
        if name==MAIN_INDIRECT_003[handlers[2]]:
            if state['vector']%5==0:engine.mem_write(ROOT+32,struct.pack('<I',(word(engine,32)+1)%8))
            return value
    if name=='func_02041814':return state['busy']
    if name=='func_02062520':return state['ready']
    if name=='func_020653d0':state['queries']+=1;return state['first'] if state['queries']==1 else state['second']
    if name=='func_0202a634':return 0x03005000
    if name=='func_020c39e0':return state['connection']
    if name=='func_020273c8':return state['scene']
    return value


def simulate(state):
    before=bytearray(state['before']);calls=[];arguments={};result=9;rounds=0
    def field(offset):return int.from_bytes(before[offset:offset+4],'little')
    def put(offset,value):struct.pack_into('<I',before,offset,value&0xFFFFFFFF)
    def call(name,args=None,stack=None):
        calls.append(name)
        if args is not None:arguments.setdefault(name,[]).append((args,stack))
    while True:
        rounds+=1
        if rounds>8:raise ValueError('Independent dispatcher transition bound reached')
        current=field(24);phase=field(28);again=False
        if phase==0:
            call(MAIN_INDIRECT_003[MODES[current][0]])
            if state['vector']%2:put(24,(current+1)%8)
            put(28,1);again=True
        elif phase==1:
            call(MAIN_INDIRECT_003[MODES[current][1]])
            if state['vector']%7==0:put(24,(current+1)%8)
            current=field(24)
            if state['next']!=current:put(32,state['next']);put(36,current);put(28,3);again=True
        elif phase==3:
            call('func_ov003_021dad9c');call('func_ov003_021dff60');call('func_02041814')
            if state['busy']!=1:
                call('func_02062520')
                if state['ready']:put(28,{9:6,8:10,10:8,11:9}.get(field(32),2));again=True
        elif phase==2:
            call(MAIN_INDIRECT_003[MODES[current][2]])
            if state['vector']%5==0:put(32,(field(32)+1)%8)
            call('func_02048fcc',[ROOT+40]);put(28,0);put(24,field(32));put(32,12)
        elif phase==4:
            before[0]=(before[0]-1)&255
            if before[0]==0:
                call('func_020653d0');before[0]=80 if state['first']==0 else 5;message={0:48,5:50}.get(state['first'],49)
                call('func_020653d0');call('func_ov003_021dea38',[20,1,message,1],struct.pack('<2I',1,0xFFFFFFFF if state['second']==0 else 87));call('func_020418b0',[2]);put(28,5);call('func_ov003_021dad9c');call('func_ov003_021df6ac')
        elif phase==5:
            call('func_0202a634');call('func_ov003_021dad9c');call('func_ov003_021df6ac')
            if signed(before[0])==80:call('func_ov003_021d79e4',[62])
            if before[0]==0 and state['buttons']&0xFF7:call('func_ov003_021df668',[0]);call('func_ov003_021d7fa4');call('func_ov003_021d79e4',[33]);put(28,0)
            before[0]=(before[0]-1)&255
            if signed(before[0])<0:before[0]=0
        elif phase==6:call('func_ov003_021d7878',[2]);put(28,7)
        elif phase==7:
            call('func_020c39e0')
            if state['connection']==3:call('func_ov003_021df668',[1]);call('func_02041538',[1,2,10]);call('func_020c39d0',[1])
            call('func_020273c8')
            if state['scene']!=12:result=0
        elif phase in [8,9]:
            call('func_02045738',[1]);call('func_0206258c',[0]);call('func_020c40f4',[1])
            if phase==8:call('func_020c39f0',[2])
            result=3
        elif phase==10:call('func_02041898',[2]);call('func_020414b0',[63]);call('func_ov003_021d7878',[1]);result=0
        if not again:break
    call('func_0204176c')
    return bytes(before),calls,arguments,result


def assert_main_dispatch003(engine,address,args,calls,state):
    if address!=0x021DA50C:return assert_modes13_003(engine,address,args,calls,state)
    before,names,arguments,result=simulate(state)
    if [c['name'] for c in calls]!=names or bytes(engine.mem_read(ROOT,40))!=before or engine.reg_read(UC_ARM_REG_R0)!=result:raise ValueError('Main dispatcher full transition/callback/context/return differs')
    for name,expected in arguments.items():
        actual=[c for c in calls if c['name']==name]
        for c,(args,stack) in zip(actual,expected):
            if c['args'][:len(args)]!=args or stack is not None and bytes.fromhex(c['stack'])[:len(stack)]!=stack:raise ValueError('Main dispatcher timer/message/input/exit arguments differ')
