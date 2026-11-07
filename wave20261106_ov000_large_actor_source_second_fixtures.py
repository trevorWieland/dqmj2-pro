import hashlib
import json
import random
import re
import struct
import match_runtime
from project import ROOT,write_json,sha256
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
from wave20261106_ov000_large_actor_source_second_paths import EVIDENCE
from wave20261106_ov000_large_actor_source_second_bindings import inputs

REG=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]
SAVED=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
BASE=0x021d7240
ACTOR=0x03008000
FIELD=0x03011000
TARGET=0x03012000
STACK=0x03030000
STOP=0x0303f000
SERVICES={0x020c5750:1,0x020c5868:1,0x0220a2a4:3,0x0203d294:1,0x02041f90:3,0x021e07b8:1,0x020028d8:2,0x0200235c:2,0x0220aac4:2,0x0220cbe0:1}


def word(v):return struct.pack('<I',v&0xffffffff)


def signed(v):return(v+0x80000000)%0x100000000-0x80000000


def normalize(v):
    v=signed(v)
    while v>0xb4000:v-=0x168000
    while v < -0xb4000:v+=0x168000
    return v


def model(address,case):
    actor=bytearray.fromhex(case['actor']);field=bytes.fromhex(case['field']);services=[];helpers={a:0 for a in[0x020c56b4,0x02042bfc,0x02042c2c,0x02028158,0x0202818c,0x02042104,0x02209c68,0x0220c598]}
    def get32(offset):return struct.unpack_from('<I',actor,offset)[0]
    def set32(offset,value):struct.pack_into('<I',actor,offset,value&0xffffffff)
    def timer():return struct.unpack_from('<h',actor,634)[0]
    def set_timer(value):struct.pack_into('<H',actor,634,value&65535)
    def service(a,args):services.append(dict(address=hex(a),args=[v&0xffffffff for v in args]))
    def record():
        helpers[0x020c56b4]+=1;identifier=struct.unpack_from('<h',actor,630)[0];service(0x020c5750 if case['cached']else 0x020c5868,[identifier]);return field
    def state(value):
        helpers[0x02209c68]+=1;old=actor[632];actor[632]=value;actor[633]=0;set_timer(0)
        if record()[7]==6:
            if value==4 and old!=3:actor[632]=6
            elif value==3 and old in[7,8]:actor[632]=5
            elif value==9 and record()[10]==7:actor[632]=old
    def normal(value):helpers[0x02028158]+=1;return normalize(value)
    def angle_get():helpers[0x02042c2c]+=1;return get32(140)
    def bearing():
        helpers[0x0202818c]+=1;target=struct.unpack('<III',bytes.fromhex(case['target']));service(0x020028d8,[target[0]-get32(112),target[2]-get32(120)]);service(0x0200235c,[case['atan'],71]);return case['bearing']
    def target_get():service(0x021e07b8,[0])
    def angle_add(delta):
        helpers[0x02042104]+=1;previous=get32(140);set32(140,normal(previous+delta));actor[9]|=int(signed(previous)!=signed(delta))
    def angle_set(value):service(0x02041f90,[ACTOR,value,0])
    def predicate(value):service(0x0220aac4,[ACTOR,value]);return case['predicate']
    result=0
    if address==0x0220cd28:
        if actor[633]==0:
            service(0x0220a2a4,[ACTOR,0,0]);set_timer(1);actor[633]=10;service(0x0220cbe0,[ACTOR])
            if not case['ready']:state(6)
        if actor[633]==10:
            target_get();wanted=normal(bearing());difference=normal(wanted-angle_get())
            if difference < -8192 or difference>8192:angle_add(8192 if difference>0 else -8192)
            else:angle_set(wanted)
            set_timer(timer()+1)
            if timer()>60:
                if predicate(0):set_timer(0)
                else:state(7)
    elif address==0x0220d7b8:
        phase=actor[633];result=1
        if phase==0:
            if predicate(0):
                service(0x0203d294,[60]);set_timer(case['rng60']+30);service(0x0220a2a4,[ACTOR,2,0]);metadata=record();helpers[0x02042bfc]+=1;set32(364,struct.unpack_from('<I',metadata,24)[0]);actor[633]=10
            else:state(7 if record()[7]==6 else 3);result=0
        elif phase==10:
            if not timer()&2:
                helpers[0x0220c598]+=1;target_get();wanted=bearing();current=angle_get();delta=normal(wanted-current);angle_add(delta>>2)
            set_timer(timer()-1)
            if timer()<=0:actor[633]=0
    elif address==0x0220ed9c:
        if actor[633]==0:
            service(0x0220a2a4,[ACTOR,1,0]);service(0x0203d294,[90]);angle=(case['rng90']-45+180)<<12;set32(636,normal(angle)>>5);set_timer(0);actor[633]=10
        if actor[633]==10:
            angle_add(signed(get32(636)));set_timer(timer()+1)
            if timer()>32:actor[633]=20
        if actor[633]==20:service(0x0220a2a4,[ACTOR,1,0]);service(0x0203d294,[0x7fffffff]);set_timer((case['rngWide']&63)+60);actor[633]=30
        if actor[633]==30:
            if not timer()&3 and predicate(1):actor[633]=200
            set_timer(timer()-1)
            if timer()<=0:actor[633]=100
        if actor[633]==100:state(3);result=1
        elif actor[633]==200:state(5 if record()[7]==6 else 4);result=1
    else:raise ValueError('Unmodeled second actor')
    return dict(returnWord=result,actor=actor.hex(),services=services,helpers={hex(a):n for a,n in helpers.items()})


def execute_one(row,body,case,value,image,main):
    address=int(row['address'],0);actor=bytes.fromhex(case['actor']);identifier=struct.unpack_from('<h',actor,630)[0];helpers={int(e['address'],0):e['bytes']for e in value['executedAcceptedHelpers']};uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(0x02000000,0x00400000);uc.mem_map(0x03000000,0x40000);uc.mem_write(0x02000000,main);uc.mem_write(BASE,image);uc.mem_write(address,body);uc.mem_write(ACTOR,actor);uc.mem_write(FIELD,bytes.fromhex(case['field']));uc.mem_write(TARGET,bytes.fromhex(case['target']));uc.mem_write(0x021d5404,word(0)+word((FIELD-44*identifier)&0xffffffff if case['cached']else 0));uc.reg_write(REG[0],ACTOR);uc.reg_write(UC_ARM_REG_SP,STACK);uc.reg_write(UC_ARM_REG_LR,STOP)
    saved=[0x60600000+i for i in range(8)]
    for register,v in zip(SAVED,saved):uc.reg_write(register,v)
    counts={a:0 for a in helpers};services=[];instructions=0;done=False
    def hook(machine,pc,size,user):
        nonlocal instructions,done
        if pc==STOP:done=True;machine.emu_stop();return
        if pc in helpers:counts[pc]+=1
        if any(a<=pc<a+n for a,n in helpers.items()):instructions+=1;return
        if pc in SERVICES:
            args=[machine.reg_read(r)for r in REG[:SERVICES[pc]]];services.append(dict(address=hex(pc),args=args));result=0
            if pc==0x020c5868:result=FIELD
            elif pc==0x021e07b8:result=TARGET
            elif pc==0x020028d8:result=case['atan']
            elif pc==0x0200235c:result=case['bearing']
            elif pc==0x0220aac4:result=int(case['predicate'])
            elif pc==0x0220cbe0:result=int(case['ready'])
            elif pc==0x0203d294:
                if args[0]not in[60,90,0x7fffffff]:raise ValueError('RNG caller limit differs')
                result=case['rng60']if args[0]==60 else case['rng90']if args[0]==90 else case['rngWide']
            machine.reg_write(REG[0],result&0xffffffff);machine.reg_write(UC_ARM_REG_PC,machine.reg_read(UC_ARM_REG_LR));return
        if not address<=pc<address+len(body):raise ValueError(('Unqualified second actor/provider body execution',hex(pc)))
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(address,STOP+4,count=30000)
    if not done or uc.reg_read(UC_ARM_REG_SP)!=STACK or[uc.reg_read(r)for r in SAVED]!=saved:raise ValueError('Second actor return/SP/callee-saved contract differs')
    result=dict(returnWord=uc.reg_read(REG[0]),actor=bytes(uc.mem_read(ACTOR,len(actor))).hex(),services=services,helpers={hex(a):n for a,n in counts.items()});expected=model(address,case)
    if result!=expected:raise ValueError(('Independent second actor/vector/phase model differs',row['address'],case,result,expected))
    return result,dict(helperInvocations=sum(counts.values()),helperInstructions=instructions,serviceEntries=len(services),vectorForwardingInvocations=counts[0x0202818c],returned=True)


def execute(rows):
    value,image,inventory,records,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes();rng=random.Random(20261106948);records=[];helper_calls=0;helper_insns=0;service_calls=0;vector_calls=0
    for helper in value['executedAcceptedHelpers']:
        address=int(helper['address'],0);base=0x02000000 if helper['module']=='main'else BASE;raw=main if helper['module']=='main'else image;config=main_inventory if helper['module']=='main'else inventory
        if(helper['processor'],helper['mode'])!=('arm9','arm')or sha256(ROOT/helper['sourceUnit'])!=helper['sourceSha256']or hashlib.sha256(raw[address-base:address-base+helper['bytes']]).hexdigest()!=helper['targetSha256']or not re.search(r'^\S+ kind:function\(arm,size=0x%x\) addr:0x%08x$'%(helper['bytes'],address),config,re.M):raise ValueError('Executed helper source/native identity differs')
    phases=[0,0,10,10,10,10,10,10,10,10,20,20,30,30,30,30,100,200,255,0,10,30,10,30];timers=[0,29,0,1,2,3,31,32,59,60,0,1,0,1,4,60,32767,-32768,3,58,-32768,-32768,32767,32767]
    for row in rows:
        a=int(row['address'],0);native=image[a-BASE:a-BASE+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes()
        for index in range(24):
            actor=bytearray(rng.randbytes(708));field=bytearray(rng.randbytes(44));struct.pack_into('<h',actor,630,[-32768,-1,0,1,32767][index%5]);actor[632]=[3,7,8,0][index%4];actor[633]=phases[index];struct.pack_into('<h',actor,634,timers[index]);struct.pack_into('<I',actor,140,[0,0xb4000,(-0xb4000)&0xffffffff,8192][index%4]);struct.pack_into('<I',actor,636,[-12288&0xffffffff,12288,8192][index%3]);field[7]=6 if index%2 else 8;field[10]=7 if index%3 else 0;struct.pack_into('<I',field,24,[0,0xffffffff,0x80000000][index%3]);case=dict(actor=actor.hex(),field=field.hex(),target=(word(0x1234)+word(0x5678)+word(0x9abc)).hex(),cached=index%2==0,predicate=index%2==0,ready=index%3!=0,rng60=[0,59,30][index%3],rng90=[0,89,45][index%3],rngWide=[0,63,0x7ffffffe][index%3],atan=[0,0x1234,0xffff0000][index%3],bearing=[0,8192,-8192,0xb4000,-0xb4000,12288,-12288][index%7]);pair=[];counts=[]
            for body in[native,compiled]:
                result,count=execute_one(row,body,case,value,image,main);pair.append(result);counts.append(count);helper_calls+=count['helperInvocations'];helper_insns+=count['helperInstructions'];service_calls+=count['serviceEntries'];vector_calls+=count['vectorForwardingInvocations']
            if pair[0]!=pair[1]:raise ValueError('Original/C second actor effects differ')
            records.append(dict(address=row['address'],case=index,input=case,result=pair[0],executions=counts))
    trace=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest();limits=['Synthetic708-byte actors,44-byte metadata and supplied target vectors; no complete game/physics/animation execution.', 'Eight actual accepted getter/setter/normalizer/vector-forwarder/relative-angle/helper bodies execute wherecalled,including actual176B angle-add with updateargument0 only. No additional helper/source/storage credit.', 'Vector44 forwards actualR0 from supplied atan/div services; underlying math providers execute0body. Its old acceptedvoid source is a separate zero-byte interface debt,not repaired here.', 'Cache/fallback,anim/RNG,target/predicate anddirect-angle-set providers supply declared bounded values/noextra memoryeffects and execute0body instructions. Signed16 timers,wordwrap andnativeconditional sequencing independently modeled.']
    result=dict(passed=True,functions=len(rows),vectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualOriginalHelperInvocations=helper_calls,actualOriginalHelperInstructions=helper_insns,actualNativeVector44ForwardingInvocations=vector_calls,suppliedServiceCalls=service_calls,suppliedServiceBodyInstructionsExecuted=0,traceSha256=trace,limits=limits,records=records);write_json(EVIDENCE/'caller-fixtures.json',result);return result
