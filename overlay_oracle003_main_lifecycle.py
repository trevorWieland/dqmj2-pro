import struct
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1

from overlay_oracle003_main_resources import seed_main_resources003,main_resources_call003,assert_main_resources003

FUNCTIONS={0x021DA3FC,0x021DA86C,0x021DAA0C,0x021DAA44,0x021DAD9C,0x021DADA8,0x021DADB8}
BASE=0x021E0690


def seed_main_lifecycle003(engine,address,vector):
    if address not in FUNCTIONS:return seed_main_resources003(engine,address,vector)
    before=bytearray(engine.mem_read(BASE,40));struct.pack_into('<I',before,36,[0,12,0xFFFFFFFF][vector%3]);engine.mem_write(BASE,bytes(before))
    return {'before':bytes(before),'initialMode':vector%6,'mode':vector%6,'game':vector//6%3,'oldHeap':[0,2,0x7FFFFFFF,0xFFFFFFFF,1,3][vector//18%6],'heapCalls':0,'objects':bytes(engine.mem_read(0x03008000,288))}


def main_lifecycle_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return main_resources_call003(engine,address,name,value,state)
    first=engine.reg_read(UC_ARM_REG_R0)
    if name=='func_0202a1e0':
        expected=2 if state['heapCalls']==0 else state['oldHeap']
        if first!=expected:raise ValueError('Overlay003 main heap switch/restore differs')
        state['heapCalls']+=1;return state['oldHeap']
    if name=='func_020c3a00':return state['mode']
    if name=='func_020c39f0':state['mode']=first
    if name=='func_02027400':return state['game']
    if name=='func_02048e74':
        if first!=BASE+24:raise ValueError('Overlay003 main pending-state identity differs')
        engine.mem_write(BASE+24,struct.pack('<3I',engine.reg_read(UC_ARM_REG_R1),0,12))
    if name=='func_02048fcc' and first!=BASE+40:raise ValueError('Overlay003 main context getter forwarding differs')
    if name=='func_02049ad0':return 0x03008000+first*8
    return value


def assert_main_lifecycle003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_main_resources003(engine,address,args,calls,state)
    before=bytearray(state['before']);expected=[]
    if address==0x021DA3FC:
        mode=state['initialMode'];selected={3:2,4:5}.get(mode,0)
        expected=['func_0202a1e0','func_ov003_021da898','func_02048e8c','func_ov003_021daa44','func_0202a1e0','func_ov003_021daac4','func_020414c8','func_020418b0']
        expected+=['func_020c3a00']*(1 if mode==2 else 2 if mode==3 else 3)
        if mode in [2,3]:expected.append('func_020c39f0');mode=1
        expected+=['func_02048e74','func_ov003_021dad9c','func_02048fcc','func_02027400']
        struct.pack_into('<4I',before,24,selected,0,12,12)
        if state['game']==2:expected.append('func_020c3a00')
        if state['game']==2 and mode==0:
            struct.pack_into('<I',before,28,4);before[0]=5;expected.append('func_020c39f0')
        else:
            expected.append('func_020c3a00')
            if mode==0:expected+=['func_ov003_021d79e4','func_020c39f0']
            expected.append('func_02041538')
        for c in calls:
            checks={'func_020414c8':[63],'func_020418b0':[2],'func_02048e74':[BASE+24,selected],'func_02041538':[0,2,10],'func_ov003_021d79e4':[33],'func_020c39f0':[1]}
            if c['name'] in checks and c['args'][:len(checks[c['name']])]!=checks[c['name']]:raise ValueError('Overlay003 main startup constants/selected mode differ')
        if state['heapCalls']!=2:raise ValueError('Overlay003 main heap restoration count differs')
    elif address==0x021DA86C:
        expected=['func_020c3a00']+(['func_020c39f0'] if state['initialMode']==1 else [])+['func_ov003_021de710','func_ov003_021dfbf4','func_ov003_021dacec','func_ov003_021daa0c']
        if state['initialMode']==1 and calls[1]['args'][0]!=0:raise ValueError('Overlay003 cleanup SDK mode reset differs')
    elif address==0x021DAA0C:
        expected=['func_02049940','func_020848d4','func_020848d4','func_0204617c','func_0204617c'];values=[[1],[1],[2],[1,2],[2,2]]
        if any(c['args'][:len(value)]!=value for c,value in zip(calls,values)):raise ValueError('Overlay003 rendering cleanup layer arguments differ')
    elif address==0x021DAA44:
        expected=['func_0205fd80']+['func_02049ad0']*36+['func_02048f3c','func_02048f2c','func_02048f1c','func_02048f4c'];objects=bytearray(state['objects'])
        for i in range(36):objects[i*8:i*8+7]=bytes([0,0,0,0,12,127,255])
        if bytes(engine.mem_read(0x03008000,288))!=bytes(objects) or [c['args'][0] for c in calls if c['name']=='func_02049ad0']!=list(range(36)):raise ValueError('Overlay003 complete 36-object initialization/padding differs')
        if calls[0]['args'][0]!=1 or [c['args'][:2] for c in calls[-4:]]!=[[2,1],[0,1],[1,1],[3,1]]:raise ValueError('Overlay003 object-bank initialization flags differ')
    else:
        result={0x021DAD9C:BASE+40,0x021DADA8:int.from_bytes(before[36:40],'little'),0x021DADB8:BASE+8}[address]
        if engine.reg_read(UC_ARM_REG_R0)!=result:raise ValueError('Overlay003 typed state/context getter differs')
    if [c['name'] for c in calls]!=expected or bytes(engine.mem_read(BASE,40))!=bytes(before):raise ValueError('Overlay003 main lifecycle state/call order differs')
