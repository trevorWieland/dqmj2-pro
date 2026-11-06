import struct
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3

FUNCTIONS={0x021DE064,0x021DE09C,0x021DE0F0,0x021DE180,0x021DE1B4,0x021DE27C,0x021DE378,0x021DE3D4,0x021DE484,0x021DE4B8,0x021DE5B0}
ROOT=0x021E0690
CONTEXT=0x021E06B8
MODE4=0x021E0A48
MODE5=0x021E0A58
PROTOCOL=0x021E07E0
INPUT=0x03005000
SELECT=[-2147483648,-1,0,1,2,255,2147483647]
REPEAT=[0,1,2,3,64,65,66,67,128,129,130,131,192,193,194,195]


def seed_modes45_003(engine,address,vector):
    if address not in FUNCTIONS:return {}
    own=MODE5 if address>=0x021DE378 else MODE4;state={'vector':vector,'own':own,'phase':[0,1,2,3,4,5,6,99][vector%8],'result':[0,1,0x80000000,0xFFFFFFFF][vector//8%4],'previous':[4,5,7,0xFFFFFFFF][vector%4],'afterPrevious':[4,5,7,0xFFFFFFFF][vector//4%4],'selected':SELECT[vector%7],'repeat':REPEAT[vector//7%16],'changed':vector//112%2,'actualMode':[0,1,4,0xFFFFFFFF][vector%4],'ready':[0,1,2,0xFFFFFFFF][vector//32%4],'fade':vector//16%2,'formats':0}
    pressed=[0,1,2,4,8,0x800,0x1000,0xFFFF][vector%8] if address==0x021DE064 else (state['repeat']^3)&3
    engine.mem_write(ROOT+36,struct.pack('<I',state['previous']));engine.mem_write(own,struct.pack('<2I',state['result'],state['phase']));engine.mem_write(CONTEXT,struct.pack('<i',state['selected']));engine.mem_write(INPUT,struct.pack('<4H',0,pressed,0,state['repeat']))
    state.update(root=bytes(engine.mem_read(ROOT,40)),modes={a:bytes(engine.mem_read(a,16)) for a in [MODE4,MODE5]},context=bytes(engine.mem_read(CONTEXT,240)),input=bytes(engine.mem_read(INPUT,8)),protocol=bytes(engine.mem_read(PROTOCOL,20)),pressed=pressed)
    return state


def modes45_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return value
    args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]];own=state['own']
    if name=='func_0202a634':return INPUT
    if name=='func_02048e74':
        kind=4 if own==MODE4 else 5
        if args[:2]!=[own,kind]:raise ValueError('Mode4/5 SDK initialization identity differs')
        engine.mem_write(own,struct.pack('<4I',kind,0,12,12))
    if name=='func_02048fcc':
        if args[0]!=CONTEXT:raise ValueError('Mode4/5 clear context identity differs')
        engine.mem_write(CONTEXT,bytes(240));engine.mem_write(ROOT+36,struct.pack('<I',state['afterPrevious']))
    if name=='func_020c3a00':return state['actualMode']
    if name=='func_020c39f0':
        if address==0x021DE378:engine.mem_write(own,struct.pack('<2I',state['vector']^0x800,99))
        elif address==0x021DE5B0:engine.mem_write(CONTEXT+12,struct.pack('<I',state['vector']^0x800))
    if name=='func_02041814':return state['ready']
    if name=='func_02041944':return state['fade']
    if address in {0x021DE0F0,0x021DE3D4}:
        if name in {'func_ov003_021de1b4','func_ov003_021de27c','func_ov003_021de4b8','func_ov003_021de5b0'}:engine.mem_write(own,struct.pack('<2I',state['result']^0x100,99));engine.mem_write(CONTEXT,struct.pack('<I',state['vector']))
        if name=='func_ov003_021dff60':engine.mem_write(CONTEXT+4,struct.pack('<I',state['vector']^0x100))
        if name=='func_ov003_021df6ac':engine.mem_write(CONTEXT+8,struct.pack('<I',state['vector']^0x200))
    if address in {0x021DE27C,0x021DE5B0} and name=='func_0205e7a8' and args[1]==85 and state['changed']:
        engine.mem_write(CONTEXT,struct.pack('<i',SELECT[(state['vector']+1)%7]));engine.mem_write(INPUT+6,struct.pack('<H',state['repeat']^3))
    if address in {0x021DE1B4,0x021DE4B8}:
        if name=='func_ov003_021ded08':state['formats']+=1;engine.mem_write(CONTEXT,struct.pack('<I',0x12340000+state['formats']))
        if name=='func_ov003_021deda4':engine.mem_write(CONTEXT+4,struct.pack('<I',state['vector']));engine.mem_write(ROOT+36,struct.pack('<I',state['afterPrevious']))
    return value


def assert_modes45_003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return
    modes={a:bytearray(data) for a,data in state['modes'].items()};own=state['own'];mode=modes[own];root=bytearray(state['root']);context=bytearray(state['context']);inputBefore=bytearray(state['input']);protocol=bytearray(state['protocol']);expected=[];checks={};phase=state['phase'];selected=state['selected'];repeat=state['repeat'];result=state['result']
    ui=['func_ov003_021dad9c','func_ov003_021dff60','func_ov003_021dad9c','func_ov003_021df6ac']
    if address==0x021DE064:
        expected=['func_0202a634'];result=int(bool(state['pressed']&0xFF7))
        if result:expected+=['func_ov003_021df668','func_ov003_021dfd18']
        checks={'func_ov003_021df668':[1],'func_ov003_021dfd18':[1]}
        if engine.reg_read(UC_ARM_REG_R0)!=result:raise ValueError('Mode6 help acknowledgment return differs')
    elif address in {0x021DE09C,0x021DE378}:
        kind=4 if own==MODE4 else 5;expected=['func_02048e74','func_ov003_021dad9c','func_02048fcc'];mode[:]=struct.pack('<4I',kind,0,12,12);context[:]=bytes(240);struct.pack_into('<I',root,36,state['afterPrevious'])
        if own==MODE4:expected+=['func_ov003_021dada8','func_ov003_021dad9c'];selected=int(state['afterPrevious']==7)
        else:expected+=['func_020c3a00','func_ov003_021dad9c','func_020c39f0'];selected=int(state['actualMode']==4);struct.pack_into('<I',mode,0,state['vector']^0x800);checks['func_020c39f0']=[1]
        struct.pack_into('<I',context,0,selected)
    elif address in {0x021DE0F0,0x021DE3D4}:
        active=1;wait=2;newPhase=2 if own==MODE5 else 1
        if phase in [0,active]:
            expected=[('func_ov003_021de4b8' if phase==0 else 'func_ov003_021de5b0') if own==MODE5 else ('func_ov003_021de1b4' if phase==0 else 'func_ov003_021de27c')]+ui;struct.pack_into('<2I',mode,0,result^0x100,newPhase if phase==0 else 99);struct.pack_into('<3I',context,0,state['vector'],state['vector']^0x100,state['vector']^0x200)
        elif own==MODE5 and phase==wait:
            expected=['func_ov003_021dad9c','func_ov003_021dff60','func_02041814'];struct.pack_into('<I',context,4,state['vector']^0x100)
            if state['ready']!=1:struct.pack_into('<I',mode,4,1)
        elif own==MODE4 and phase in [2,3,4]:result={2:0,3:5,4:7}[phase]
        elif own==MODE5 and phase in [3,4,5]:result={3:4,4:10,5:11}[phase]
        if engine.reg_read(UC_ARM_REG_R0)!=result:raise ValueError('Mode4/5 dispatcher captured result differs')
        checks={'func_ov003_021dff60':[CONTEXT],'func_ov003_021df6ac':[CONTEXT]}
    elif address in {0x021DE180,0x021DE484}:expected=['func_ov003_021df4b4','func_ov003_021dfccc'];checks={'func_ov003_021df4b4':[2 if phase==3 else 1]}
    elif address in {0x021DE27C,0x021DE5B0}:
        expected=['func_0202a634','func_ov003_021dad9c'];sounds=[]
        if repeat&64:selected=selected-1 if selected>0 else 1
        elif repeat&128:selected=selected+1 if selected<1 else 0
        if repeat&192:
            expected.append('func_0205e7a8');sounds.append([0xFFFFFFFF,85])
            if state['changed']:selected=SELECT[(state['vector']+1)%7];repeat^=3;struct.pack_into('<H',inputBefore,6,repeat)
        struct.pack_into('<i',context,0,selected)
        if repeat&1:
            if selected==0:struct.pack_into('<I',mode,4,3 if own==MODE4 else 4)
            elif selected==1:
                if own==MODE4:expected+=['func_02041538','func_ov003_021dccc4'];protocol[1]=0;checks['func_ov003_021dccc4']=[0]
                else:expected.append('func_020c39f0');checks['func_020c39f0']=[4];struct.pack_into('<I',context,12,state['vector']^0x800)
                struct.pack_into('<I',mode,4,4 if own==MODE4 else 5)
            if own==MODE5:expected+=['func_02041538','func_02061260'];checks['func_02061260']=[1]
            expected.append('func_0205e7a8');sounds.append([0xFFFFFFFF,82]);checks['func_02041538']=[1,2,10]
        elif repeat&2:struct.pack_into('<I',mode,4,2 if own==MODE4 else 3);expected.append('func_0205e7a8');sounds.append([0xFFFFFFFF,83])
        if [c['args'][:2] for c in calls if c['name']=='func_0205e7a8']!=sounds:raise ValueError('Mode4/5 repeat navigation/confirm/cancel sound priority differs')
    else:
        previous=5 if own==MODE4 else 4;expected=['func_ov003_021dada8'];formats=[]
        if state['previous']!=previous:expected+=['func_ov003_021dad9c','func_ov003_021ded08'];formats.append(([CONTEXT,3,16,1],[3,30,2,0]))
        if own==MODE5:expected+=['func_ov003_021dad9c','func_ov003_021ded08'];formats.append(([CONTEXT,23,16,2],[5,29,2,1]))
        expected+=['func_ov003_021dad9c','func_ov003_021dad9c','func_ov003_021deda4','func_ov003_021dfd18','func_ov003_021dada8'];selected=0x12340000+len(formats) if formats else state['selected']&0xFFFFFFFF
        struct.pack_into('<2I',context,0,selected,state['vector']);struct.pack_into('<I',root,36,state['afterPrevious'])
        if state['afterPrevious']!=previous:expected.append('func_020620e8')
        expected.append('func_02041944')
        if state['fade']:expected.append('func_02041538')
        for c,(values,stack) in zip([c for c in calls if c['name']=='func_ov003_021ded08'],formats):
            if c['args']!=values or bytes.fromhex(c['stack'])!=struct.pack('<4I',*stack):raise ValueError('Mode4/5 conditional header formatter geometry differs')
        c=next(c for c in calls if c['name']=='func_ov003_021deda4')
        if c['args']!=[CONTEXT,2,0x021E03B4 if own==MODE4 else 0x021E03B8,2] or bytes.fromhex(c['stack'])[:12]!=struct.pack('<3I',6 if own==MODE4 else 8,28,selected):raise ValueError('Mode4/5 fresh formatted cursor selection differs')
        checks={'func_ov003_021dfd18':[1],'func_020620e8':[35,1],'func_02041538':[0,2,10]}
    if [c['name'] for c in calls]!=expected:raise ValueError('Mode4/5 independent callback order differs')
    for c in calls:
        if c['name'] in checks and c['args'][:len(checks[c['name']])]!=checks[c['name']]:raise ValueError('Mode4/5 independent callback arguments differ')
    for pointer,data in [(CONTEXT,context),(ROOT,root),(INPUT,inputBefore),(PROTOCOL,protocol),*modes.items()]:
        if bytes(engine.mem_read(pointer,len(data)))!=bytes(data):raise ValueError('Mode4/5 complete cursor/mode/protocol/input effects differ')
