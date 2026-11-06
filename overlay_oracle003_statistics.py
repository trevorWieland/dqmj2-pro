import struct
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3

from overlay_oracle003_main_lifecycle import seed_main_lifecycle003,main_lifecycle_call003,assert_main_lifecycle003

FUNCTIONS={0x021D9E58,0x021D9E80,0x021D9EFC,0x021D9F18,0x021DA01C,0x021DA178,0x021DA378,0x021DA3D0}
BASE=0x021E0670
TABLES=[0x021E02F0,0x021E02E0,0x021E02EA,0x021E02F6,0x021E02E4]


def seed_statistics003(engine,address,vector):
    if address not in FUNCTIONS:return seed_main_lifecycle003(engine,address,vector)
    phase=[0,1,2,255][vector%4];dirty=[0,1,0x80000000,0xFFFFFFFF][vector//4%4]
    indices=[];v=vector%162
    for count in [3,2,3,3,3]:indices.append(v%count);v//=count
    values=[[0,1,65535,65536,0xFFFFFFD6,0xFFFFFFFF][vector%6],*indices]
    before=bytearray(engine.mem_read(BASE,32));before[0]=phase;struct.pack_into('<7I',before,4,dirty,*values);engine.mem_write(BASE,bytes(before))
    mode=[42,41,255][vector//16%3];engine.mem_write(0x0300426C,bytes([mode]))
    for i in range(32):engine.mem_write(0x03008000+i*64,struct.pack('<I',0x03009000+i*64));engine.mem_write(0x03009004+i*64,struct.pack('<I',0x12340000+i))
    labels=[(values[0]+42)&65535]+[int.from_bytes(engine.mem_read(table+index*2,2),'little') for table,index in zip(TABLES,indices)]+[61]
    return {'before':bytes(before),'mode':mode,'position':(0,0),'formats':0,'labels':labels,'vector':vector}


def statistics_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return main_lifecycle_call003(engine,address,name,value,state)
    args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]]
    if name=='func_02061944':return 0x03004000
    if name=='func_02061dcc':return 0x03008000+args[0]*64
    if name=='func_ov003_021d9f18' and address==0x021D9E58:
        if bytes(engine.mem_read(BASE+4,4))!=bytes(4):raise ValueError('Statistics dirty flag not cleared before layout callback')
        engine.mem_write(BASE+4,struct.pack('<I',17));engine.mem_write(BASE,b'\x99')
    if name=='func_ov003_021da178' and address==0x021D9E80:engine.mem_write(BASE+4,struct.pack('<I',9))
    if name in {'func_0204aaf0','func_0204ab98'}:
        x,y=state['position'];step=state['formats']
        if address==0x021DA01C:
            if name=='func_0204aaf0' and step:x=0
            elif name=='func_0204ab98':x=((x+(104 if step==1 else 96)+32768)&65535)-32768
        if bytes(engine.mem_read(args[1],4))!=struct.pack('<2h',x,y):raise ValueError('Statistics shared signed position/reset/carry differs')
        pair=([0,32760,-32768][step%3],[-32768,32767,0][(step+state['vector'])%3]);engine.mem_write(args[1],struct.pack('<2h',*pair));state['position']=pair;state['formats']+=1
    return value


def assert_statistics003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_main_lifecycle003(engine,address,args,calls,state)
    before=bytearray(state['before']);expected=[];phase=before[0];dirty=int.from_bytes(before[4:8],'little')
    if address==0x021D9E58:expected=['func_ov003_021d9f18'];before[0]=0;before[4:8]=struct.pack('<I',17)
    elif address==0x021D9E80:
        expected=['func_02061944']
        if phase==0:expected+=['func_ov003_021da01c','func_ov003_021da178'];before[0]=1;before[4:8]=struct.pack('<I',9)
        elif phase==1 and dirty:expected+=['func_ov003_021da178'];before[4:8]=bytes(4)
        if engine.reg_read(UC_ARM_REG_R0)!=int(state['mode']!=42):raise ValueError('Statistics update signed mode completion differs')
    elif address==0x021D9EFC:
        expected=['func_ov003_021da378','func_020622ec']
        if calls[-1]['args'][:3]!=[6,20,0]:raise ValueError('Statistics cleanup layer arguments differ')
    elif address==0x021D9F18:
        expected=['func_02061c1c']*14+['func_02045ed0'];geometry=[[6,2,4,14],[13,16,4,14]]+[[7+i,3,8+i*2,13] for i in range(6)]+[[14+i,16,8+i*2,13] for i in range(6)]
        if [c['args'] for c in calls[:-1]]!=geometry or any(bytes.fromhex(c['stack'])[:12]!=struct.pack('<3I',2,0,0) for c in calls[:-1]) or calls[-1]['args'][0]!=1:raise ValueError('Statistics fourteen-panel layout geometry differs')
    elif address in {0x021DA01C,0x021DA178}:
        start=6 if address==0x021DA01C else 13
        expected=['func_02061dcc','func_02049f4c']*7+['func_02061dcc','func_02049ffc']*7
        expected+=['func_0204aaf0','func_0204ab98']*7 if address==0x021DA01C else ['func_0204aaf0']*7
        if [c['args'][0] for c in calls if c['name']=='func_02061dcc']!=list(range(start,start+7))*2 or [c['args'][0] for c in calls if c['name']=='func_02049f4c']!=[0x03008000+i*64 for i in range(start,start+7)] or [c['args'][0] for c in calls if c['name']=='func_02049ffc']!=[0x12340000+i for i in range(start,start+7)]:raise ValueError('Statistics seven-cell nested reset handles differ')
        formats=[c for c in calls if c['name']=='func_0204aaf0'];labels=list(range(32,39)) if address==0x021DA01C else state['labels']
        for i,(c,label) in enumerate(zip(formats,labels)):
            if [c['args'][0],c['args'][2],c['args'][3]]!=[start+i,20,0] or bytes.fromhex(c['stack'])[:12]!=struct.pack('<3I',label,1,1):raise ValueError('Statistics enum lookup/font identifier/format arguments differ')
        for i,c in enumerate(c for c in calls if c['name']=='func_0204ab98'):
            if [c['args'][0],c['args'][2],c['args'][3]]!=[start+i,1,0x021E02FC if i==0 else 0x021E0300] or bytes.fromhex(c['stack'])[:4]!=bytes(4):raise ValueError('Statistics row suffix text identity differs')
        if state['formats']!=(14 if address==0x021DA01C else 7):raise ValueError('Statistics position mutation count differs')
    elif address==0x021DA378:
        expected=['func_020456ac']*2
        for c,layer in zip(calls,[1,2]):
            if c['args']!=[0,layer,0,0] or bytes.fromhex(c['stack'])[:8]!=struct.pack('<2I',32,24):raise ValueError('Statistics background clear differs')
    elif address==0x021DA3D0:before[4:8]=struct.pack('<I',1)
    if [c['name'] for c in calls]!=expected or bytes(engine.mem_read(BASE,32))!=bytes(before):raise ValueError('Statistics full state/call sequence differs')
