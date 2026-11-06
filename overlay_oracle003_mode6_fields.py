import struct
from overlay_oracle003_modes45 import seed_modes45_003,modes45_call003,assert_modes45_003
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3

PANEL=0x021E0A18
BACKUP=0x021E0A30
CONTEXT=0x021E06B8
CURRENT=0x03008000
INPUT=0x03005000
ROWS=[(0x021DD8A4,0x021DD94C,2,33,0x021E036E,3,0x021E0362),(0x021DDA30,0x021DDAD8,1,34,0x021E0358,2,0x021E0354),(0x021DDBC0,0x021DDC68,2,35,0x021E0386,3,0x021E0368),(0x021DDD4C,0x021DDDF4,2,36,0x021E037A,3,0x021E0374),(0x021DDED8,0x021DDF80,2,37,0x021E035C,3,0x021E0380)]
FUNCTIONS={0x021DD6C4,*[a for row in ROWS for a in row[:2]]}
VALUES=[0,1,127,128,255,256,0x80000000,0xFFFFFFFF]
SELECT=[0,1,2,3,4,5,6,256,261,0xFFFFFFFF]
PRESS=[0,1,2,3,0x800,0x801,0x802,0xFFFF]
SETTERS=['func_020c35ec','func_020c360c','func_020c362c','func_020c364c','func_020c366c','func_020c368c']


def seed_mode6_fields003(engine,address,vector):
    if address not in FUNCTIONS:return seed_modes45_003(engine,address,vector)
    row=next(((i,r) for i,r in enumerate(ROWS) if address in r[:2]),None);selected=SELECT[vector%10];pressed=PRESS[vector//10%8];changed=vector//80%2;afterSelected=(SELECT[(vector+1)%10] if changed else selected);afterPressed=(pressed^3 if changed else pressed)
    limit=5 if row is None else row[1][2]
    if afterPressed&0x800 and not afterPressed&3:afterSelected=(afterSelected%256)%(limit+1)
    if pressed&0x800 and not pressed&3:selected=(selected%256)%(limit+1)
    state={'vector':vector,'row':row,'selected':selected,'pressed':pressed,'afterSelected':afterSelected,'afterPressed':afterPressed,'enabled':VALUES[vector%8]%256,'afterEnabled':VALUES[vector//8%8]%256,'refreshes':0,'setterValues':[],'previews':[]}
    engine.mem_write(PANEL,bytes([state['enabled'],vector%7,limit,vector%256]));engine.mem_write(CONTEXT,struct.pack('<I',selected));engine.mem_write(INPUT,struct.pack('<4H',0,pressed,0,0))
    current=struct.pack('<6I',*[VALUES[(vector+i)%8] for i in range(6)]);backup=struct.pack('<6I',*[VALUES[(vector+i+3)%8] for i in range(6)]);engine.mem_write(CURRENT,current);engine.mem_write(BACKUP,backup)
    state.update(panel=bytes(engine.mem_read(PANEL,24)),context=bytes(engine.mem_read(CONTEXT,240)),input=bytes(engine.mem_read(INPUT,8)),current=current,backup=backup,root=bytes(engine.mem_read(0x021E0690,40)))
    if address==0x021DD6C4:state['callbacks']={0x02008E0C:'func_02008e0c'}
    return state


def mode6_fields_call003(engine,address,name,value,state):
    if address not in FUNCTIONS:return modes45_call003(engine,address,name,value,state)
    args=[engine.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]]
    if name=='func_0202a634':return INPUT
    if name=='func_020c36ac':
        if state['row'] is not None and address==state['row'][1][0] and bytes(engine.mem_read(PANEL+2,1))!=bytes([state['row'][1][2]]):raise ValueError('Mode6 field limit not stored before settings getter')
        return CURRENT
    if name=='func_ov003_021df4b4':engine.mem_write(PANEL,bytes([state['afterEnabled']]))
    if name=='func_ov003_021ded08':
        if state['row'] is not None:
            index=state['row'][0];enabled=int.from_bytes(state['current'][(index+1)*4:(index+2)*4],'little')%256
            if bytes(engine.mem_read(PANEL,1))!=bytes([enabled]):raise ValueError('Mode6 source setting not narrowed into enabled byte before formatter')
        engine.mem_write(PANEL,bytes([state['afterEnabled']]));engine.mem_write(CONTEXT+4,struct.pack('<I',state['vector']))
    if name=='func_ov003_021deda4':engine.mem_write(CONTEXT+8,struct.pack('<I',state['vector']^0x1234))
    if name=='func_ov003_021da3e4':
        if args[0]!=BACKUP:raise ValueError('Mode6 customized preview source identity differs')
        state['previews'].append(bytes(engine.mem_read(args[0],24)))
    if name=='func_ov003_021da3d0':
        state['refreshes']+=1;engine.mem_write(CONTEXT+4,struct.pack('<I',state['vector']+state['refreshes']))
        if address==0x021DD6C4 and state['refreshes']==1:engine.mem_write(CONTEXT,struct.pack('<I',state['afterSelected']));engine.mem_write(INPUT+2,struct.pack('<H',state['afterPressed']))
        if address==0x021DDAD8:engine.mem_write(PANEL,bytes([state['afterEnabled']]))
    if name in SETTERS:
        index=SETTERS.index(name);state['setterValues'].append((index,args[0]));engine.mem_write(CURRENT+index*4,struct.pack('<I',args[0]))
        if index<5:engine.mem_write(BACKUP+(index+1)*4,struct.pack('<I',VALUES[(state['vector']+index+1)%8]^0x55AA55AA))
    if name=='func_ov003_021deaf8':
        if args[0]!=CONTEXT:raise ValueError('Mode6 help cursor identity differs')
        old=int.from_bytes(engine.mem_read(CONTEXT,4),'little');engine.mem_write(CONTEXT,struct.pack('<I',old^0xFFFFFFFF))
    return value


def help_expected(engine,calls,table,index):
    c=next(c for c in calls if c['name']=='func_ov003_021dea38');message=int.from_bytes(engine.mem_read(table+index*2,2),'little')
    if c['args']!=[20,1,message,1] or bytes.fromhex(c['stack'])[:8]!=struct.pack('<2I',1,87):raise ValueError('Mode6 captured help index/table/message geometry differs')


def assert_mode6_fields003(engine,address,args,calls,state):
    if address not in FUNCTIONS:return assert_modes45_003(engine,address,args,calls,state)
    panel=bytearray(state['panel']);context=bytearray(state['context']);inputBefore=bytearray(state['input']);current=bytearray(state['current']);backup=bytearray(state['backup']);expected=[];checks={}
    if state['row'] is not None:
        index,row=state['row'];init,step,limit,identifier,label,count,help=row
        if address==init:
            expected=['func_ov003_021dad9c','func_ov003_021df4b4','func_020c36ac','func_ov003_021dad9c','func_ov003_021ded08','func_ov003_021dad9c','func_ov003_021deda4','func_ov003_021dfd18'];panel[0]=state['afterEnabled'];panel[2]=limit;struct.pack_into('<2I',context,4,state['vector'],state['vector']^0x1234)
            checks={'func_ov003_021df4b4':[4],'func_ov003_021dfd18':[1]};c=next(c for c in calls if c['name']=='func_ov003_021ded08')
            if c['args']!=[CONTEXT,identifier,16,3] or bytes.fromhex(c['stack'])!=struct.pack('<4I',7,28,2,2):raise ValueError('Mode6 settings-field header formatter geometry differs')
            c=next(c for c in calls if c['name']=='func_ov003_021deda4')
            if c['args']!=[CONTEXT,count,label,2] or bytes.fromhex(c['stack'])[:12]!=struct.pack('<3I',10,28,state['afterEnabled']):raise ValueError('Mode6 settings-field fresh enabled byte/list formatter differs')
        else:
            expected=['func_0202a634','func_ov003_021dad9c'];pressed=state['pressed'];selected=state['selected']
            if pressed&3:
                if pressed&1:struct.pack_into('<I',backup,(index+1)*4,selected)
                panel[1]=1;panel[0]=index;struct.pack_into('<I',panel,12,1)
                if pressed&1 and index==1:expected.append('func_ov003_021da3d0');panel[0]=state['afterEnabled'];struct.pack_into('<I',context,4,state['vector']+1)
                expected.append('func_0205e7a8');checks['func_0205e7a8']=[0xFFFFFFFF,82 if pressed&1 else 83]
            elif pressed&0x800:
                expected+=['func_ov003_021deaf8','func_ov003_021dea38'];struct.pack_into('<I',context,0,selected^0xFFFFFFFF);struct.pack_into('<I',panel,12,3);help_expected(engine,calls,help,selected%256)
    else:
        expected=['func_0202a634','func_ov003_021dad9c','func_ov003_021da3e4','func_ov003_021da3d0'];selected=state['afterSelected'];pressed=state['afterPressed'];struct.pack_into('<2I',context,0,selected,state['vector']+1);struct.pack_into('<H',inputBefore,2,pressed)
        if state['previews']!=[state['backup']]:raise ValueError('Mode6 full customized preview settings differ')
        if pressed&1:
            selected%=256
            if selected<5:panel[1]=selected+2
            if selected==5:
                expected+=['func_020c36ac','func_02008e0c']+SETTERS;current[:]=backup;setterValues=[(0,3)];struct.pack_into('<I',current,0,3)
                for i in range(1,6):
                    value=VALUES[(state['vector']+i)%8]^0x55AA55AA;struct.pack_into('<I',backup,i*4,value);struct.pack_into('<I',current,i*4,value);setterValues.append((i,value))
                if state['setterValues']!=setterValues:raise ValueError('Mode6 all six settings setters/fresh backup reloads differ')
                struct.pack_into('<I',panel,12,4)
            else:expected.append('func_ov003_021da3d0');struct.pack_into('<I',context,4,state['vector']+2);struct.pack_into('<I',panel,12,1)
            expected.append('func_0205e7a8');checks['func_0205e7a8']=[0xFFFFFFFF,82]
        elif pressed&2:
            expected+=['func_020c36ac','func_02008e0c','func_0205e7a8'];backup[:]=current;panel[1]=0;panel[0]=3;struct.pack_into('<I',panel,12,1);checks['func_0205e7a8']=[0xFFFFFFFF,83]
        elif pressed&0x800:
            expected+=['func_ov003_021deaf8','func_ov003_021dea38'];struct.pack_into('<I',context,0,selected^0xFFFFFFFF);struct.pack_into('<I',panel,12,3);help_expected(engine,calls,0x021E039C,selected%256)
        copies=[c['args'][:3] for c in calls if c['name']=='func_02008e0c']
        wanted=[[BACKUP,CURRENT,24]] if pressed&1 and selected==5 else [[CURRENT,BACKUP,24]] if not pressed&1 and pressed&2 else []
        if copies!=wanted:raise ValueError('Mode6 native complete settings copy direction/span differs')
    if [c['name'] for c in calls]!=expected:raise ValueError('Mode6 settings independent callback order differs')
    for c in calls:
        if c['name'] in checks and c['args'][:len(checks[c['name']])]!=checks[c['name']]:raise ValueError('Mode6 settings independent callback arguments differ')
    for pointer,data in [(PANEL,panel),(CONTEXT,context),(INPUT,inputBefore),(CURRENT,current),(BACKUP,backup),(0x021E0690,state['root'])]:
        if bytes(engine.mem_read(pointer,len(data)))!=bytes(data):
            actual=bytes(engine.mem_read(pointer,len(data)));different=[(i,actual[i],data[i]) for i in range(len(data)) if actual[i]!=data[i]][:8]
            raise ValueError(f'Mode6 complete settings effects differ at {pointer:08x}, vector {state["vector"]}: {different}')
