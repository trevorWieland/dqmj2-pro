import struct
from overlay_oracle003_mode7_helpers import seed_mode7_helpers003,mode7_helpers_arguments003,mode7_helpers_call003,assert_mode7_helpers003
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP

MODE=0x021E07E0
DISPLAY=0x021E07F4
PRIMARY=0x021E07FC
SECONDARY=0x021E08EC
CONTEXT=0x021E06B8
FUNCTIONS={0x021DC52C,0x021DC6C0}


def parameters(address,vector):
    if address==0x021DC52C:
        return {'protocol':vector%2 if vector<96 else [2,255][vector%2],'first':vector//2%4,'second':vector//8%4,'high':[0,0x100,0xFFFFFF00][vector//32%3],'actualFirst':(vector//2%4 if vector//32%3==0 else 3-vector//2%4),'mask':vector%64,'kind':0}
    return {'kind':2 if vector<256 else 4 if vector<768 else [0,1,3,5,0xFFFFFFFF][vector-768],'total':vector%256,'flag':(vector-256)%256,'swap':vector//256%2,'recordValue':[0,127,128,255][vector//64%4]}


def seed_mode7_setup003(engine,address,vector):
    if address not in FUNCTIONS:return seed_mode7_helpers003(engine,address,vector)
    state=parameters(address,vector);state['vector']=vector
    if address==0x021DC52C:engine.mem_write(MODE+1,bytes([state['protocol']]))
    before=bytearray(engine.mem_read(DISPLAY,532));before[492]=vector%7;before[493]=vector%4;before[494]=(vector+1)%4;struct.pack_into('<I',before,488,0x03006000)
    if address==0x021DC6C0:
        before[492]=state['total'];struct.pack_into('<2I',before,8,[0,1,0x80000000,0xFFFFFFFF][vector%4],[0xFFFFFFFF,0x80000000,1,0][vector//4%4])
    engine.mem_write(DISPLAY,bytes(before))
    state.update(display=bytes(before),mode=bytes(engine.mem_read(MODE,20)),context=bytes(engine.mem_read(CONTEXT,240)),records={p:bytes(engine.mem_read(p,132)) for p in [0x03006000,0x03006100]})
    return state


def mode7_setup_arguments003(address,vector,args):
    mode7_helpers_arguments003(address,vector,args)
    if address==0x021DC6C0:args[0]=parameters(address,vector)['kind']


def formatter_words(vector):return struct.pack('<4I',0xAABB0000+vector,0xDDCC0000+vector,0x12340000+vector,0xFEDC0000+vector)


def mode7_setup_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return mode7_helpers_call003(engine,address,name,value,state)
    args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP]]
    if address==0x021DC52C:
        firstName='func_02062aa0' if state['protocol']==0 else 'func_020c385c';secondName='func_02062ad0' if state['protocol']==0 else 'func_020c3938'
        if name==firstName:
            if bytes(engine.mem_read(DISPLAY+500,24))!=bytes(24):raise ValueError('Mode7 six-record list not cleared before count query')
            return state['high']+state['first']
        if name==secondName:
            if bytes(engine.mem_read(DISPLAY+493,1))!=bytes([state['first']]):raise ValueError('Mode7 first count byte not stored before second query')
            engine.mem_write(DISPLAY+493,bytes([state['actualFirst']]))
            return state['high']+state['second']
        if name in {'func_02062a50','func_02062a88','func_020c3838','func_020c3914'}:
            secondary=name in {'func_02062a88','func_020c3914'};index=args[0]+(state['actualFirst'] if secondary else 0)
            if args[0] not in range(state['second'] if secondary else state['actualFirst']):raise ValueError('Mode7 combined roster local index differs')
            return 0x03006000+index*256 if state['mask']>>index&1 else 0
    else:
        if name=='func_ov003_021deb60':engine.mem_write(DISPLAY+492,bytes([(state['total']+5)&255]))
        if name=='func_ov003_021deedc':
            if args[0]!=PRIMARY or bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_SP),20))!=struct.pack('<5I',(state['total']+1)&255,(state['total']+1)&255,1,15,1):raise ValueError('Mode7 primary cursor builder identity/five stack arguments differ')
            engine.mem_write(PRIMARY,formatter_words(state['vector']))
        if name=='func_ov003_021dec40':engine.mem_write(CONTEXT+16,bytes([state['flag']]))
        if name=='func_ov003_021de868' and bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_SP),20))!=struct.pack('<5I',3,30,2,0,1):raise ValueError('Mode7 secondary formatter five stack arguments differ')
        if name=='func_ov003_021deda4':
            if args[0]!=SECONDARY:raise ValueError('Mode7 secondary formatter identity differs')
            engine.mem_write(SECONDARY,formatter_words(state['vector']));record=0x03006100 if state['swap'] else 0x03006000;engine.mem_write(DISPLAY+488,struct.pack('<I',record));engine.mem_write(record+50,bytes([state['recordValue']]))
        if name=='func_ov003_021dfd18' and state['kind']==2:
            if bytes(engine.mem_read(PRIMARY,8))!=state['display'][8:16]:raise ValueError('Mode7 saved primary cursor not restored before activation')
    return value


def assert_mode7_setup003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_mode7_helpers003(engine,address,args,calls,state)
    display=bytearray(state['display']);mode=bytearray(state['mode']);context=bytearray(state['context']);records={p:bytearray(data) for p,data in state['records'].items()};expected=[]
    if address==0x021DC52C:
        display[500:524]=bytes(24)
        if state['protocol'] in [0,1]:
            firstName,secondName=('func_02062aa0','func_02062ad0') if state['protocol']==0 else ('func_020c385c','func_020c3938');expected=[firstName,secondName];total=state['actualFirst']+state['second'];display[492:495]=bytes([total,state['actualFirst'],state['second']])
            expectedPointers=[]
            for index in range(total):
                secondary=index>=state['actualFirst'];name=('func_02062a88' if secondary else 'func_02062a50') if state['protocol']==0 else ('func_020c3914' if secondary else 'func_020c3838');expected.append(name);expectedPointers.append(0x03006000+index*256 if state['mask']>>index&1 else 0)
            for i,pointer in enumerate(expectedPointers):struct.pack_into('<I',display,500+i*4,pointer)
            if state['protocol']==1:expected.append('func_020625ac')
        expected+=['func_020620b4','func_02008c58','func_02008c58'];display[:8]=struct.pack('<2I',1,7);display[8:488]=bytes(480)
        clears=[c['args'][:3] for c in calls if c['name']=='func_02008c58']
        if clears!=[[0,PRIMARY,240],[0,SECONDARY,240]]:raise ValueError('Mode7 complete two native cursor-clear spans differ')
        if any(c['args'][0]!=1 for c in calls if c['name'] in {'func_020625ac','func_020620b4'}):raise ValueError('Mode7 roster kind input enable/selection sync differs')
    else:
        expected=['func_ov003_021dad9c'];kind=state['kind']
        if kind==2:
            expected+=['func_ov003_021deb60','func_ov003_021deedc','func_ov003_021dfd18','func_ov003_021dfd50'];rows=(state['total']+1)&255;mode[0]=state['total'];display[492]=(state['total']+5)&255;display[16:24]=formatter_words(state['vector'])[8:16]
            c=next(c for c in calls if c['name']=='func_ov003_021deedc')
            if c['args']!=[PRIMARY,1,3,28] or bytes.fromhex(c['stack'])!=struct.pack('<4I',rows,rows,1,15):raise ValueError('Mode7 primary count-plus-cancel row wrapping/geometry differs')
        elif kind==4:
            expected+=['func_ov003_021dad9c','func_ov003_021dec40','func_ov003_021de868','func_ov003_021deda4','func_ov003_021dfd18','func_ov003_021dfd50'];context[16]=state['flag'];mode[0]=5;display[248:264]=formatter_words(state['vector']);record=0x03006100 if state['swap'] else 0x03006000;struct.pack_into('<I',display,488,record);records[record][50]=state['recordValue'];struct.pack_into('<I',display,248,state['recordValue'])
            c=next(c for c in calls if c['name']=='func_ov003_021de868');flag=int.from_bytes(bytes([state['flag']]),'little',signed=True)&0xFFFFFFFF
            if c['args']!=[5,flag,2,1] or bytes.fromhex(c['stack'])!=struct.pack('<4I',3,30,2,0):raise ValueError('Mode7 signed context byte/secondary menu geometry differs')
            c=next(c for c in calls if c['name']=='func_ov003_021deda4')
            if c['args']!=[SECONDARY,5,0,2] or bytes.fromhex(c['stack'])[:12]!=struct.pack('<3I',6,28,0):raise ValueError('Mode7 secondary formatter dimensions differ')
        expected.append('func_ov003_021dc820')
        for c in calls:
            values={'func_ov003_021deb60':[5,0,5],'func_ov003_021dec40':[CONTEXT,1],'func_ov003_021dfd18':[1],'func_ov003_021dfd50':[224,64,1] if kind==2 else [224,0,0],'func_ov003_021dc820':[kind]}
            if c['name'] in values and c['args'][:len(values[c['name']])]!=values[c['name']]:raise ValueError('Mode7 rebuild cursor/context/common-render arguments differ')
    if [c['name'] for c in calls]!=expected or bytes(engine.mem_read(DISPLAY,532))!=bytes(display) or bytes(engine.mem_read(MODE,20))!=bytes(mode) or bytes(engine.mem_read(CONTEXT,240))!=bytes(context) or any(bytes(engine.mem_read(p,132))!=bytes(data) for p,data in records.items()):raise ValueError('Mode7 setup complete counts/cursor/record/context effects differ')
