import struct
from overlay_oracle003_mode6 import seed_mode6_003,mode6_call003,assert_mode6_003
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP

FUNCTIONS={0x021DCD3C,0x021DCD84,0x021DCE34,0x021DCE68,0x021DCF60}
ROOT=0x021E0690
CONTEXT=0x021E06B8
MODE=0x021E0A08
SELECT=[-2147483648,-1,0,1,2,2147483647]


def seed_mode2_003(engine,address,vector):
    if address not in FUNCTIONS:return seed_mode6_003(engine,address,vector)
    state={'vector':vector,'phase':[0,1,2,3,4,5,6,99][vector%8],'result':[0,1,0x80000000,0xFFFFFFFF][vector//8%4],'previous':[1,2,12,0xFFFFFFFF][vector%4],'afterPrevious':[1,2,12,0xFFFFFFFF][vector//4%4],'selected':SELECT[vector%6],'pressed':[0,1,2,3][vector//6%4],'repeat':[0,64,128,192][vector//24%4],'changed':vector//96%2,'ready':[0,1,2,0xFFFFFFFF][vector//32%4],'fade':vector//16%2,'formatCalls':0}
    engine.mem_write(ROOT+36,struct.pack('<I',state['previous']));engine.mem_write(MODE,struct.pack('<2I',state['result'],state['phase']));engine.mem_write(CONTEXT,struct.pack('<i',state['selected']));engine.mem_write(0x03005000,struct.pack('<4H',0,state['pressed'],0,state['repeat']))
    state.update(root=bytes(engine.mem_read(ROOT,40)),mode=bytes(engine.mem_read(MODE,16)),context=bytes(engine.mem_read(CONTEXT,240)),input=bytes(engine.mem_read(0x03005000,8)))
    return state


def mode2_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return mode6_call003(engine,address,name,value,state)
    args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]]
    if name=='func_0202a634':return 0x03005000
    if name=='func_02048e74':
        if args[:2]!=[MODE,2]:raise ValueError('Mode2 SDK initialization identity differs')
        engine.mem_write(MODE,struct.pack('<4I',2,0,12,12))
    if name=='func_02048fcc':
        if args[0]!=CONTEXT:raise ValueError('Mode2 cleared context identity differs')
        engine.mem_write(CONTEXT,bytes(240));engine.mem_write(ROOT+36,struct.pack('<I',state['afterPrevious']))
    if name=='func_02041814':return state['ready']
    if name=='func_02041944':return state['fade']
    if address==0x021DCD84:
        if name in {'func_ov003_021dce68','func_ov003_021dcf60'}:engine.mem_write(MODE,struct.pack('<I',state['result']^0x100));engine.mem_write(CONTEXT,struct.pack('<I',state['vector']))
        if name=='func_ov003_021dff60':engine.mem_write(CONTEXT+4,struct.pack('<I',state['vector']^0x100))
        if name=='func_ov003_021df6ac':engine.mem_write(CONTEXT+8,struct.pack('<I',state['vector']^0x200))
    if address==0x021DCF60 and name=='func_0205e7a8' and args[1]==85 and state['changed']:
        engine.mem_write(CONTEXT,struct.pack('<i',SELECT[(state['vector']+1)%6]));engine.mem_write(0x03005002,struct.pack('<H',state['pressed']^3))
    if address==0x021DCE68:
        if name=='func_ov003_021ded08':
            state['formatCalls']+=1;engine.mem_write(CONTEXT,struct.pack('<I',0x12340000+state['formatCalls']));engine.mem_write(ROOT+36,struct.pack('<I',state['afterPrevious']))
        if name=='func_ov003_021deda4':engine.mem_write(CONTEXT+4,struct.pack('<I',state['vector']))
    return value


def assert_mode2_003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_mode6_003(engine,address,args,calls,state)
    mode=bytearray(state['mode']);context=bytearray(state['context']);root=bytearray(state['root']);inputBefore=bytearray(state['input']);expected=[];checks={};phase=state['phase'];result=state['result'];selected=state['selected'];pressed=state['pressed']
    ui=['func_ov003_021dad9c','func_ov003_021dff60','func_ov003_021dad9c','func_ov003_021df6ac']
    if address==0x021DCD3C:
        expected=['func_02048e74','func_ov003_021dad9c','func_02048fcc','func_ov003_021dada8'];mode[:]=struct.pack('<4I',2,0,12,12);context[:]=bytes(240);struct.pack_into('<I',root,36,state['afterPrevious'])
        if state['afterPrevious']==12:expected.append('func_ov003_021dad9c');struct.pack_into('<I',context,0,1)
    elif address==0x021DCD84:
        if phase in [0,2]:
            expected=['func_ov003_021dce68' if phase==0 else 'func_ov003_021dcf60']+ui;struct.pack_into('<I',mode,0,result^0x100);struct.pack_into('<3I',context,0,state['vector'],state['vector']^0x100,state['vector']^0x200)
            if phase==0:struct.pack_into('<I',mode,4,1)
        elif phase==1:
            expected=['func_ov003_021dad9c','func_ov003_021dff60','func_02041814'];struct.pack_into('<I',context,4,state['vector']^0x100)
            if state['ready']!=1:struct.pack_into('<I',mode,4,2)
        elif phase in [3,4,5]:result={3:3,4:11,5:1}[phase]
        if engine.reg_read(UC_ARM_REG_R0)!=result:raise ValueError('Mode2 dispatcher captured result differs')
        checks={'func_ov003_021dff60':[CONTEXT],'func_ov003_021df6ac':[CONTEXT]}
    elif address==0x021DCE34:expected=['func_ov003_021df4b4','func_ov003_021dfccc'];checks={'func_ov003_021df4b4':[2 if phase==5 else 1]}
    elif address==0x021DCF60:
        expected=['func_0202a634','func_ov003_021dad9c'];sounds=[]
        if state['repeat']&64:selected=selected-1 if selected>0 else 1
        elif state['repeat']&128:selected=selected+1 if selected<1 else 0
        if state['repeat']&192:
            expected.append('func_0205e7a8');sounds.append([0xFFFFFFFF,85])
            if state['changed']:selected=SELECT[(state['vector']+1)%6];pressed^=3;struct.pack_into('<H',inputBefore,2,pressed)
        struct.pack_into('<i',context,0,selected)
        if pressed&1:
            if selected in [0,1]:
                expected.append('func_020c356c');checks['func_020c356c']=[selected];struct.pack_into('<I',mode,4,3+selected)
                if selected==1:expected.append('func_020c39f0');checks['func_020c39f0']=[3]
            expected+=['func_02041538','func_02061260','func_0205e7a8'];checks.update({'func_02041538':[1,2,10],'func_02061260':[1]});sounds.append([0xFFFFFFFF,82])
        elif pressed&2:struct.pack_into('<I',mode,4,5);expected.append('func_0205e7a8');sounds.append([0xFFFFFFFF,83])
        if [c['args'][:2] for c in calls if c['name']=='func_0205e7a8']!=sounds:raise ValueError('Mode2 navigation/confirm/cancel sound priority differs')
    else:
        expected=['func_ov003_021dada8'];formats=[]
        if state['previous']!=1:expected+=['func_ov003_021dad9c','func_ov003_021ded08'];formats.append(([CONTEXT,2,16,1],[3,30,2,0]))
        expected+=['func_ov003_021dad9c','func_ov003_021ded08','func_ov003_021dad9c','func_ov003_021dad9c','func_ov003_021deda4','func_ov003_021dfd18','func_ov003_021dada8'];formats.append(([CONTEXT,12,16,2],[5,29,2,1]));selected=0x12340000+len(formats);struct.pack_into('<2I',context,0,selected,state['vector']);struct.pack_into('<I',root,36,state['afterPrevious'])
        if state['afterPrevious']!=1:expected.append('func_020620e8')
        expected.append('func_02041944')
        if state['fade']:expected.append('func_02041538')
        for c,(values,stack) in zip([c for c in calls if c['name']=='func_ov003_021ded08'],formats):
            if c['args']!=values or bytes.fromhex(c['stack'])!=struct.pack('<4I',*stack):raise ValueError('Mode2 separate cursor formatter geometry/flags differ')
        c=next(c for c in calls if c['name']=='func_ov003_021deda4')
        if c['args']!=[CONTEXT,2,0x021E0350,2] or bytes.fromhex(c['stack'])[:12]!=struct.pack('<3I',8,28,selected):raise ValueError('Mode2 cursor selection captured after formatters differs')
        checks={'func_ov003_021dfd18':[1],'func_020620e8':[37,1],'func_02041538':[0,2,10]}
    if [c['name'] for c in calls]!=expected:raise ValueError('Mode2 independent callback order differs')
    for c in calls:
        if c['name'] in checks and c['args'][:len(checks[c['name']])]!=checks[c['name']]:raise ValueError('Mode2 independent callback arguments differ')
    for pointer,data in [(MODE,mode),(CONTEXT,context),(ROOT,root),(0x03005000,inputBefore)]:
        if bytes(engine.mem_read(pointer,len(data)))!=bytes(data):raise ValueError('Mode2 complete state/cursor/input effects differ')
