import struct
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3

from overlay_oracle003_first_mode import seed_first_mode003,first_mode_arguments003,first_mode_call003,assert_first_mode003

FUNCTIONS={0x021DA898,0x021DAAC4,0x021DAC44}
BASE=0x021E0690


def word(engine,address,width=4):return int.from_bytes(engine.mem_read(address,width),'little')


def seed_main_resources003(engine,address,vector):
    if address not in FUNCTIONS:return seed_first_mode003(engine,address,vector)
    state={'vector':vector,'heap':[0,2,0xFFFFFFFF][vector%3],'indexCalls':{},'sizes':[vector%65,(vector*7)%129,(vector*13)%65],'sectionCalls':[],'cursor':0x03007000,'cursorInitial':[0,0xFFFFFFFF,0x80000000][vector%3]}
    engine.mem_write(0x03007000,struct.pack('<I',state['cursorInitial']))
    state['prefix']=bytes(engine.mem_read(BASE,24));state['buffer']=bytes(engine.mem_read(0x0300D000,2048));state['payload']=bytes(engine.mem_read(0x0300C000,65));state['gpu']={p:word(engine,p,4 if p==0x04001000 else 2) for p in [0x04001000,0x04001008,0x0400100A,0x0400100C,0x0400100E]}
    if address==0x021DAAC4:state['callbacks']={0x0204518C:'func_0204518c',0x02045490:'func_02045490',0x0202A44C:'func_0202a44c',0x02008E0C:'func_02008e0c',0x02045994:'func_02045994'}
    return state


def main_resources_arguments003(address,vector,args):
    first_mode_arguments003(address,vector,args)
    if address==0x021DAC44:args[:3]=[0x0300F000,vector%4,0x03007000]


def index_result(name,call,vector):
    if name=='func_02048f6c':return vector%4 if call==0 else vector//4%4
    if name=='func_02048f5c':return vector//16%4
    if name=='func_02048f7c':return (vector+1)%4 if call==0 else (vector+2)%4
    return [vector%4,vector//4%4,vector//16%4][call]


def main_resources_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return first_mode_call003(engine,address,name,value,state)
    args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]]
    if name=='func_0202a250':return state['heap']
    if name in {'func_02048f6c','func_02048f5c','func_02048f7c','func_02048f8c'}:
        call=state['indexCalls'].get(name,0);state['indexCalls'][name]=call+1
        if args[0]!=1:raise ValueError('Main resource bank selector differs')
        return index_result(name,call,state['vector'])
    if name=='func_0203cc2c':
        if args[:2]!=[0x021E0304,state['heap']]:raise ValueError('Main resource archive/heap identity differs')
        return 0x0300F000
    if name=='func_0204518c':
        kind=args[2]
        if args[1]!=0x0300F000 or kind not in range(3):raise ValueError('Main resource section owner/kind differs')
        engine.mem_write(args[0],struct.pack('<2I',0x0300A000+kind*4096,state['sizes'][kind]));state['sectionCalls'].append(kind)
    if name=='func_02045490':
        state['cursor']=BASE+8+index_result('func_02048f8c',2,state['vector'])*4 if address==0x021DAAC4 else 0x03007000
        state['beforeTransferCursor']=word(engine,state['cursor']);engine.mem_write(state['cursor'],struct.pack('<I',(state['beforeTransferCursor']+3)&0xFFFFFFFF))
    if name=='func_0202a44c':
        if args[:3]!=[2,2048,4]:raise ValueError('Main resource allocation heap/size/alignment differs')
        return 0x0300D000
    if name=='func_0201d444':
        if args[1]!=0x021E0318 or bytes(engine.mem_read(args[0],32))!=bytes(32):raise ValueError('Main resource complete zeroed filename/identity differs')
        template=bytes(engine.mem_read(args[1],32)).split(b'\0',1)[0];engine.mem_write(args[0],template+b'\0');state['filename']=template
    if name=='func_0205ff80' and bytes(engine.mem_read(args[0],len(state['filename'])+1))!=state['filename']+b'\0':raise ValueError('Main resource formatted filename differs')
    return value


def assert_main_resources003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_first_mode003(engine,address,args,calls,state)
    if address==0x021DA898:
        expected=['func_02002d00','func_020038a8','func_02003950','func_020039c0','func_02003a40','func_020489f0','func_02046150','func_02046150','func_020848d0']+['func_02008c58']*4+['func_02045738']
        values=[[0],[4],[256],[0],[0],[1],[1,0,2],[2,2,2],[],[0,0x06200000,0x20000],[0,0x06600000,0x20000],[0,0x05000400,0x400],[0,0x07000400,0x400],[1]]
        if any(c['args'][:len(v)]!=v for c,v in zip(calls,values)):raise ValueError('Main graphics setup layers/VRAM/palette clear ranges differ')
        gpu=state['gpu'];control=((gpu[0x04001000]&0xFFCFFFEF)|16)&~0x1F00|0x1F00
        if word(engine,0x04001000)!=control:raise ValueError('Main graphics display control mask differs')
        for i,mode,priority in [(0,0x108,1),(1,4,2),(2,0x218,0),(3,0x310,3)]:
            if word(engine,0x04001008+i*2,2)!=(((gpu[0x04001008+i*2]&0x43)|mode)&~3|priority):raise ValueError('Main graphics background modes/priorities differ')
    else:
        helper=['func_0204518c','func_02045490','func_0202a44c','func_0204518c','func_02008e0c','func_02045994']
        if address==0x021DAAC4:
            expected=['func_0202a250','func_02048f6c','func_02048f5c','func_02048f7c','func_02048f8c','func_0203cc2c','func_0204518c','func_0204820c','func_0204820c','func_02048308','func_02048f8c','func_02048f8c','func_ov003_021dac44']+helper+['func_0202a498','func_ov003_021de6b4','func_0201d444','func_0205ff80','func_ov003_021de768','func_ov003_021de7d8','func_0205ff9c','func_02048f6c','func_ov003_021de840','func_ov003_021df928','func_02048f7c','func_02045680','func_ov003_021deb78']
            prefix=bytearray(state['prefix']);banks=list(struct.unpack('<4I',prefix[8:24]))
            for name,value in [('func_02048f6c',32),('func_02048f5c',32),('func_02048f7c',32),('func_02048f8c',0)]:banks[index_result(name,0,state['vector'])]=value
            cursorIndex=index_result('func_02048f8c',2,state['vector']);banks[cursorIndex]=(banks[cursorIndex]+3+state['sizes'][1])&0xFFFFFFFF
            prefix[8:24]=struct.pack('<4I',*banks);prefix[4:8]=struct.pack('<I',0x0300D000)
            if bytes(engine.mem_read(BASE,24))!=bytes(prefix):raise ValueError('Main resource bank cursor/allocated pointer differs')
            bank=index_result('func_02048f8c',1,state['vector'])
            for c in calls:
                if c['name']=='func_ov003_021dac44' and c['args'][:3]!=[0x0300F000,bank,BASE+8+cursorIndex*4]:raise ValueError('Nested resource bank/cursor ownership differs')
                if c['name']=='func_0204820c':
                    if c['args'][0]==0x0300A000:
                        if c['args'][:3]!=[0x0300A000,0,state['sizes'][0]]:raise ValueError('Main palette section upload differs')
                    elif c['args'][1:3]!=[0,2] or bytes(engine.mem_read(c['args'][0],2))!=bytes(2):raise ValueError('Main palette zero entry differs')
                if c['name']=='func_0202a498' and c['args'][:2]!=[state['heap'],0x0300F000]:raise ValueError('Main resource free heap/owner differs')
                if c['name'] in {'func_ov003_021de768','func_ov003_021de7d8'} and c['args'][0]!=BASE+8:raise ValueError('Main resource bank context forwarding differs')
                if c['name']=='func_ov003_021de840':
                    value=banks[index_result('func_02048f6c',1,state['vector'])];signed=value if value<0x80000000 else value-0x100000000
                    if c['args'][0]!=(signed>>5)&0xFFFFFFFF:raise ValueError('Main resource signed bank tile cursor differs')
                if c['name']=='func_02045680' and c['args'][0]!=index_result('func_02048f7c',1,state['vector']):raise ValueError('Main resource final bank differs')
                if c['name']=='func_ov003_021deb78' and c['args'][:2]!=[BASE+40,0]:raise ValueError('Main resource rendering context differs')
        else:
            expected=helper;bank=args[1]
            if word(engine,0x03007000)!=(state['cursorInitial']+3+state['sizes'][1])&0xFFFFFFFF or word(engine,BASE+4)!=0x0300D000:raise ValueError('Resource helper mutable cursor reload/allocation differs')
        if state['sectionCalls']!=([0,1,2] if address==0x021DAAC4 else [1,2]):raise ValueError('Resource section sequence differs')
        for c in calls:
            if c['name']=='func_02045490' and c['args']!=[bank,0x0300B000,state['beforeTransferCursor'],state['sizes'][1]]:raise ValueError('Resource graphics transfer cursor/span differs')
            if c['name']=='func_02008e0c' and c['args'][:3]!=[0x0300C000,0x0300D000,state['sizes'][2]]:raise ValueError('Resource native copy span/ownership differs')
            if c['name']=='func_02045994' and c['args']!=[bank,0x0300D000,0,2048]:raise ValueError('Resource allocated bank upload differs')
        expectedBuffer=state['payload'][:state['sizes'][2]]+state['buffer'][state['sizes'][2]:]
        if bytes(engine.mem_read(0x0300D000,2048))!=expectedBuffer:raise ValueError('Resource native copy bytes or preserved allocation boundary differs')
    if [c['name'] for c in calls]!=expected:raise ValueError('Main resources complete dependency call order differs')
