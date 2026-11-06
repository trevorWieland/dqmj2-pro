import struct
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_SP


from overlay_oracle003_statistics import seed_statistics003,statistics_call003,assert_statistics003


def word(engine,address):return int.from_bytes(engine.mem_read(address,4),'little')


def seed_caption003(engine,address,vector):
    if address!=0x021D9984:return seed_statistics003(engine,address,vector)
    selector=vector//216%2;engine.mem_write(0x021E057D,bytes([selector]))
    values=[]
    for i in range(3):
        p=0x03006000+i*256;identifier=[-32768,-1,0,1,32767][(vector+i)%5];level=[0,49,50,51,99,100][(vector+i)%6];marker=[0,127,128,255][(vector+i)%4]
        engine.mem_write(p+24,struct.pack('<h',identifier));engine.mem_write(p+28,bytes([i]));engine.mem_write(p+48,bytes([level,0,marker]));values.append((identifier,level,marker))
    for i in range(32):
        engine.mem_write(0x03008000+i*64,struct.pack('<I',0x03009000+i*64));engine.mem_write(0x03009004+i*64,struct.pack('<I',0x12340000+i))
    engine.mem_write(0x0300B000,struct.pack('<3I',0x100,0x200,0x300))
    return {'vector':vector,'mask':vector//27%8,'selector':selector,'counts':[vector//(3**i)%3 for i in range(3)],'values':values,'pos':None,'posCalls':0,'numberCalls':0}


def caption_arguments003(address,vector,args):
    if address==0x021D9984:args[:2]=[[0,11,21,0xFFFFFFFF][vector%4],0x0300B000]


def caption_call003(engine,address,name,value,state):
    if address!=0x021D9984:return statistics_call003(engine,address,name,value,state)
    args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2]]
    if name=='func_02061dcc':return 0x03008000+args[0]*64
    if name in {'func_02062a10','func_020c3948'}:
        i=args[0]//256-1
        if i not in range(3) or name!=('func_02062a10' if state['selector'] else 'func_020c3948'):raise ValueError('Caption record getter identity differs')
        return 0x03006000+i*256 if state['mask']>>i&1 else 0
    if name=='func_02044cdc':
        ids=[row[0]&0xFFFFFFFF for row in state['values']]
        if args[0] not in ids:raise ValueError('Caption signed identifier differs')
        return state['counts'][ids.index(args[0])]
    if name=='func_020630b0':
        if args[0] not in range(3):raise ValueError('Caption level category differs')
        return [0,50,100][args[0]]
    if name in {'func_0204aaf0','func_0204ab44'}:
        if bytes(engine.mem_read(args[1],4))!=bytes(4):raise ValueError('Caption local position not initialized')
        if name=='func_0204aaf0' and args[2]==5:
            state['posCalls']+=1;state['pos']=args[1]
            pair=([0,32760,-32768][state['posCalls']%3],[-32768,32767,0][state['posCalls']%3]);engine.mem_write(args[1],struct.pack('<2h',*pair));state['expectedPos']=pair
    if name=='func_0204ab98':
        x,y=state['expectedPos'];x=((x+16+32768)&65535)-32768
        if bytes(engine.mem_read(args[1],4))!=struct.pack('<2h',x,y):raise ValueError('Caption signed position addition before label differs')
        pair=([-32768,32760,0][state['posCalls']%3],[32767,0,-32768][state['posCalls']%3]);engine.mem_write(args[1],struct.pack('<2h',*pair));state['expectedPos']=pair
    if name=='func_0204a9d4':
        x,y=state['expectedPos'];x=((x+8+32768)&65535)-32768
        if bytes(engine.mem_read(args[1],4))!=struct.pack('<2h',x,y):raise ValueError('Caption SDK-updated number position differs')
        state['numberCalls']+=1
    return value


def assert_caption003(engine,address,args,calls,state):
    if address!=0x021D9984:return assert_statistics003(engine,address,args,calls,state)
    expected=['func_02061dcc','func_02049f4c']*10+['func_02061dcc','func_02049ffc']*10+['func_0204ab44'];offset=0;renders=[];draws=[];numbers=[];getter='func_02062a10' if state['selector'] else 'func_020c3948'
    for i in range(3):
        expected.append(getter)
        if not state['mask']>>i&1:continue
        identifier,level,marker=state['values'][i];count=state['counts'][i]
        expected+=['func_02044cdc','func_02061dcc','func_020602ec','func_020630b0','func_0204aaf0','func_0204ab98']
        renders.append([0x03009000+(offset+7)*64,identifier&0xFFFFFFFF,0x03006000+i*256,0])
        draws.extend([(offset+10,5,1,[1,1,1]),(offset+13,0,1,[marker,1,1])])
        if level!=100:expected.append('func_0204a9d4');numbers.append((offset+10,1 if level<[0,50,100][i] else 5,level))
        expected.append('func_0204aaf0');offset=(offset+count+1)&255
    if [c['name'] for c in calls]!=expected:raise ValueError('Caption row/reset/render/number order differs')
    getrows=[c for c in calls if c['name']=='func_02061dcc']
    if [c['args'][0] for c in getrows[:20]]!=list(range(6,16))*2:raise ValueError('Caption ten-cell reset traversal differs')
    if [c['args'][0] for c in calls if c['name']=='func_02049f4c']!=[0x03008000+i*64 for i in range(6,16)] or [c['args'][0] for c in calls if c['name']=='func_02049ffc']!=[0x12340000+i for i in range(6,16)]:raise ValueError('Caption nested cell handles differ')
    title=next(c for c in calls if c['name']=='func_0204ab44')
    if title['args'][0]!=6 or title['args'][2:]!=[20,0] or bytes.fromhex(title['stack'])[:12]!=struct.pack('<3I',args[0],1,1):raise ValueError('Caption title formatting arguments differ')
    if [c['args'] for c in calls if c['name']=='func_020602ec']!=renders or any(bytes.fromhex(c['stack'])[:8]!=struct.pack('<2I',0,1) for c in calls if c['name']=='func_020602ec'):raise ValueError('Caption signed record/detail rendering differs')
    for c,(cell,kind,mode,stack) in zip((c for c in calls if c['name']=='func_0204aaf0'),draws):
        if [c['args'][0],c['args'][2],c['args'][3]]!=[cell,kind,mode] or bytes.fromhex(c['stack'])[:12]!=struct.pack('<3I',*stack):raise ValueError('Caption label/marker target or formatting flags differ')
    for c in (c for c in calls if c['name']=='func_0204ab98'):
        if c['args'][2:]!=[1,0x021E02DC] or bytes.fromhex(c['stack'])[:4]!=bytes(4):raise ValueError('Caption label text identity differs')
    for c,(cell,color,number) in zip((c for c in calls if c['name']=='func_0204a9d4'),numbers):
        if [c['args'][0],c['args'][2],c['args'][3]]!=[cell,color,number] or bytes.fromhex(c['stack'])[:8]!=struct.pack('<2I',2,0):raise ValueError('Caption number/threshold color differs')
    if state['posCalls']!=state['mask'].bit_count() or state['numberCalls']!=len(numbers):raise ValueError('Caption present-record/number coverage differs')
