import itertools
import struct
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1
from overlay_oracle003_record_copy import seed_record_copy003,record_copy_arguments003,record_copy_call003,assert_record_copy003

from overlay_oracle003_roster_prepare import seed_roster_prepare003,roster_prepare_call003,assert_roster_prepare003

FUNCTIONS={0x021DB7FC,0x021DB978,0x021DB6EC,0x021DB868,0x021DB57C}
PAIRS=[(i,j) for i in range(3) for j in range(3,6)]+[(0,1),(1,2),(0,2),(3,4),(4,5),(3,5)]


def seed_compatibility003(engine,address,vector):
    if address not in FUNCTIONS and address != 0x021DB4A8:return seed_roster_prepare003(engine,address,vector)
    if address not in FUNCTIONS:return seed_record_copy003(engine,address,vector)
    count=12 if address==0x021DB57C else 6;records=[]
    for i in range(count):
        p=0x03006000+i*256;data=bytearray(engine.mem_read(p,132));struct.pack_into('<IhB',data,20,0x1000+i,-32768+i,i%4);records.append({'pointer':p,'data':data,'family':i})
    mode=0;request=0;mask=63;altmask=63
    if address==0x021DB7FC:
        if vector<256:presence=15;fa,fb=divmod(vector,16)
        else:presence=(vector-256)%16;fa=(vector-256)//16;fb=fa if vector%2 else (fa+1)%16
        records[0]['family']=fa;records[1]['family']=fb
        if presence&4==0:struct.pack_into('<I',records[0]['data'],20,0)
        if presence&8==0:struct.pack_into('<I',records[1]['data'],20,0)
        pointers=[records[0]['pointer'] if presence&1 else 0,records[1]['pointer'] if presence&2 else 0]
    elif address==0x021DB978:
        presence=vector%16;kind=vector//16%6;pointers=[records[0]['pointer'] if presence&1 else 0,records[1]['pointer'] if presence&2 else 0]
        if presence&4==0:struct.pack_into('<I',records[0]['data'],20,0)
        if presence&8==0:struct.pack_into('<I',records[1]['data'],20,0)
        if kind in [0,1,4]:records[1]['data'][24:26]=records[0]['data'][24:26]
        if kind in [0,2,4]:records[1]['data'][26]=records[0]['data'][26]
        if kind==5:pointers[1]=pointers[0]
    else:
        if address==0x021DB57C:
            request=vector%3;mode=2 if vector//3%2 else 0;pattern=vector//6%4;pair=PAIRS[vector//24%15]
            groups=[0] if pattern==0 else [6] if pattern==1 else [0,6] if pattern==2 else []
            for base in groups:
                i,j=base+pair[0],base+pair[1]
                if request==0:records[j]['family']=records[i]['family']
                else:records[j]['data'][24:27]=records[i]['data'][24:27]
            if vector>=360:
                mask=(vector-360)%64;altmask=63^mask
                for i in range(12):records[i]['family']=0;records[i]['data'][24:27]=records[0]['data'][24:27]
        else:
            mode=2 if vector%2 else 0
            if vector<60:
                pair=PAIRS[vector//4%15]
                if vector//2%2:
                    i,j=pair
                    if address==0x021DB6EC:records[j]['family']=records[i]['family']
                    else:records[j]['data'][24:27]=records[i]['data'][24:27]
            else:
                mask=(vector-60)//2%64
                for i in range(6):records[i]['family']=0;records[i]['data'][24:27]=records[0]['data'][24:27]
        pointers=[record['pointer'] if (mask if i<6 else altmask)>>(i%6)&1 else 0 for i,record in enumerate(records)]
        engine.mem_write(0x0300B000,struct.pack('<6I',*pointers[:6]))
    lookup={};byPointer={}
    for i,record in enumerate(records):
        engine.mem_write(record['pointer'],bytes(record['data']));identifier=int.from_bytes(record['data'][24:26],'little',signed=True)&0xFFFFFFFF
        if identifier not in lookup:
            lookup[identifier]=0x03010000+i*16;flags=((vector*31)&0xFF0F)|(record['family']<<4);engine.mem_write(lookup[identifier]+4,struct.pack('<H',flags&65535))
        record['species']=identifier;record['id']=int.from_bytes(record['data'][20:24],'little');record['variant']=record['data'][26];byPointer[record['pointer']]=record
    callbacks={0x021DB6EC:'func_ov003_021db6ec',0x021DB868:'func_ov003_021db868',0x021DB7FC:'func_ov003_021db7fc',0x021DB978:'func_ov003_021db978',0x020C365C:'func_020c365c',0x020449D4:'func_020449d4'} if address in {0x021DB57C,0x021DB6EC,0x021DB868} else {}
    callbacks={target:name for target,name in callbacks.items() if target!=address}
    return {'records':records,'byPointer':byPointer,'lookup':lookup,'pointers':pointers,'mode':mode,'request':request,'mask':mask,'altmask':altmask,'callbacks':callbacks,'address':address}


def compatibility_arguments003(address,vector,args):
    record_copy_arguments003(address,vector,args)
    if address in {0x021DB7FC,0x021DB978}:
        if address==0x021DB7FC:presence=15 if vector<256 else (vector-256)%16
        else:presence=vector%16
        args[:2]=[0x03006000 if presence&1 else 0,0x03006100 if presence&2 else 0]
        if address==0x021DB978 and vector//16%6==5:args[1]=args[0]
    if address in {0x021DB6EC,0x021DB868}:args[:2]=[0x0300B000,0x0300B00C]
    if address==0x021DB57C:args[0]=vector%3


def compatibility_call003(engine,address,name,value,state):
    if address not in FUNCTIONS and address != 0x021DB4A8:return roster_prepare_call003(engine,address,name,value,state)
    if address not in FUNCTIONS:return record_copy_call003(engine,address,name,value,state)
    first=engine.reg_read(UC_ARM_REG_R0)
    if name=='func_020449d4':
        if first not in state['lookup']:raise ValueError('Compatibility signed species lookup differs')
        return state['lookup'][first]
    if name=='func_020c365c':return state['mode']
    if name in {'func_02062a50','func_02062a88'}:
        if first not in range(3):raise ValueError('Compatibility primary roster index differs')
        return state['pointers'][first+(3 if name=='func_02062a88' else 0)]
    if name in {'func_020c3828','func_020c3904'}:
        if first not in range(3):raise ValueError('Compatibility alternate roster index differs')
        return 0xA000+first+(9 if name=='func_020c3904' else 6)
    if name=='func_02062a10':
        index=first-0xA000
        if index not in range(6,12):raise ValueError('Compatibility alternate identifier resolution differs')
        return state['pointers'][index]
    return value


def pair_matches(state,a,b,family):
    if not a or not b:return False
    a,b=state['byPointer'][a],state['byPointer'][b]
    if not a['id'] or not b['id']:return False
    if family:
        first=state['lookup'][a['species']];second=state['lookup'][b['species']]
        return first==second or a['family']==b['family']
    return a['species']==b['species'] and a['variant']==b['variant']


def scanned(state,pointers,family):
    pairs=PAIRS[9:12] if state['mode']==2 else PAIRS
    visited=[]
    for i,j in pairs:
        a,b=pointers[i],pointers[j];visited.append([a,b])
        if pair_matches(state,a,b,family):return True,visited
    return False,visited


def assert_compatibility003(engine,address,args,calls,state):
    if address not in FUNCTIONS and address != 0x021DB4A8:return assert_roster_prepare003(engine,address,args,calls,state)
    if address not in FUNCTIONS:return assert_record_copy003(engine,address,args,calls,state)
    if address in {0x021DB7FC,0x021DB978}:
        expected=pair_matches(state,args[0],args[1],address==0x021DB7FC)
        valid=bool(args[0] and args[1] and state['byPointer'][args[0]]['id'] and state['byPointer'][args[1]]['id'])
        lookups=[state['byPointer'][p]['species'] for p in args[:2]] if valid and address==0x021DB7FC else []
        if [c['args'][0] for c in calls]!=lookups or any(c['name']!='func_020449d4' for c in calls):raise ValueError('Compatibility pair lookup short circuit differs')
    else:
        family=address==0x021DB6EC or address==0x021DB57C and state['request']==0;visited=[]
        if address==0x021DB57C:
            expected=False;useAlt=True
            if state['request'] in [0,1]:expected,first=scanned(state,state['pointers'][:6],family);visited+=first;useAlt=not expected
            if useAlt and state['request'] in [0,1]:expected,second=scanned(state,state['pointers'][6:],family);visited+=second
            getterNames=[c['name'] for c in calls if c['name'] in {'func_02062a50','func_02062a88','func_020c3828','func_020c3904','func_02062a10'}]
            getters=['func_02062a50']*3+['func_02062a88']*3
            if useAlt:getters+=['func_020c3828','func_02062a10']*3+['func_020c3904','func_02062a10']*3
            if getterNames!=getters:raise ValueError('Compatibility first/alternate roster fallback differs')
        else:expected,visited=scanned(state,state['pointers'],family)
        helper='func_ov003_021db7fc' if family else 'func_ov003_021db978'
        if [c['args'][:2] for c in calls if c['name']==helper]!=visited:raise ValueError('Compatibility pair order/early result or roster scope differs')
    if engine.reg_read(UC_ARM_REG_R0)!=int(expected):raise ValueError('Compatibility duplicate-family/species result differs')
    if any(bytes(engine.mem_read(record['pointer'],132))!=bytes(record['data']) for record in state['records']):raise ValueError('Compatibility unexpectedly changed a source record')
