import hashlib
import json
import random
import re
import struct
import match_runtime
from project import ROOT,write_json,sha256
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
from wave20261106_ov000_actor_controller_source_first_paths import EVIDENCE
from wave20261106_ov000_actor_controller_source_first_bindings import inputs

REG=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]
SAVED=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
BASE=0x021d7240
ACTOR=0x03008000
FIELD=0x03011000
STACK=0x03030000
STOP=0x0303f000
SERVICES={0x020c5750:1,0x020c5868:1,0x0220ce54:1,0x0203d294:1,0x0220a2a4:3,0x02042104:3,0x021dc374:4}


def word(v):return struct.pack('<I',v&0xffffffff)


def signed32(v):return(v+0x80000000)%0x100000000-0x80000000


def model(address,case):
    actor=bytearray.fromhex(case['actor']);field=bytes.fromhex(case['field']);services=[];helpers={0x020c56b4:0,0x02042c0c:0,0x02209c68:0,0x0221089c:0}
    def timer():return struct.unpack_from('<h',actor,634)[0]
    def set_timer(value):struct.pack_into('<H',actor,634,value&65535)
    def read32(offset):return struct.unpack_from('<I',actor,offset)[0]
    def set32(offset,value):struct.pack_into('<I',actor,offset,value&0xffffffff)
    def service(a,args):services.append(dict(address=hex(a),args=[v&0xffffffff for v in args]))
    def record():
        helpers[0x020c56b4]+=1;identifier=struct.unpack_from('<h',actor,630)[0];service(0x020c5750 if case['cached']else 0x020c5868,[identifier]);return field
    def state(value):
        helpers[0x02209c68]+=1;old=actor[632];actor[632]=value;actor[633]=0;set_timer(0)
        if record()[7]==6:
            if value==4 and old!=3:actor[632]=6
            elif value==3 and old in[7,8]:actor[632]=5
            elif value==9 and record()[10]==7:actor[632]=old
    def active(value):helpers[0x02042c0c]+=1;actor[352]=value
    def flag(value):helpers[0x0221089c]+=1;actor[483]=value if(actor[482]or actor[484])and actor[352]>16 and not actor[485]else 0
    result=0
    if address==0x0220fcb8:
        if actor[632]not in[9,4]and record()[10]!=7:
            kind=record()[7];state(4 if kind==6 and actor[632]==3 else 9);result=1
    elif address==0x02210008:
        result=1
        if actor[632]in[9,1,7]:result=0
        elif actor[632]==3 and record()[7]==8:result=0
        elif actor[632]==6 and record()[8]==3:result=0
    elif address==0x0220c768:
        if timer()==0:
            set32(656,read32(116));set32(668,read32(116)-20480);actor[705]=1;active(31);flag(1)
        t=timer();product=(t*(t*178))&0xffffffff;set32(116,read32(656)-(signed32(product)>>1));kind=record()[12]
        service(0x021dc374,[ACTOR+112,ACTOR+528,STACK-24,kind])
        if case['collision']:
            set32(116,case['collisionY']);actor[705]=0;result=1
        set_timer(timer()+1)
    elif address==0x0220d8c4:
        if actor[633]==0:service(0x0220ce54,[ACTOR]);service(0x0203d294,[0x7fffffff]);set_timer((case['rng']&31)+30);actor[633]=10
        if actor[633]==10:
            set_timer(timer()-1)
            if timer()<=0:actor[633]=20
        if actor[633]==20:service(0x0220a2a4,[ACTOR,0,0]);actor[633]=30;set_timer(0)
        if actor[633]==30:
            set_timer(timer()+1)
            if timer()>15:set_timer(0);actor[633]=40
        if actor[633]==40:
            service(0x02042104,[ACTOR,368640,0]);set_timer(timer()+1)
            if timer()>=2:actor[633]=100
        if actor[633]==100:state(3);result=1
    else:raise ValueError('Unmodeled complete actor')
    return dict(returnWord=result,actor=actor.hex(),services=services,helpers={hex(a):n for a,n in helpers.items()})


def execute_one(row,body,case,value,image,main):
    address=int(row['address'],0);actor=bytes.fromhex(case['actor']);field=bytes.fromhex(case['field']);identifier=struct.unpack_from('<h',actor,630)[0]
    helpers={int(v['address'],0):v['bytes']for v in value['executedAcceptedHelpers']};uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(0x02000000,0x00400000);uc.mem_map(0x03000000,0x40000);uc.mem_write(0x02000000,main);uc.mem_write(BASE,image);uc.mem_write(address,body);uc.mem_write(ACTOR,actor);uc.mem_write(FIELD,field)
    uc.mem_write(0x021d5404,word(0)+word((FIELD-44*identifier)&0xffffffff if case['cached']else 0));uc.reg_write(REG[0],ACTOR);uc.reg_write(UC_ARM_REG_SP,STACK);uc.reg_write(UC_ARM_REG_LR,STOP)
    saved=[0xa0000000+i*0x101 for i in range(8)]
    for reg,v in zip(SAVED,saved):uc.reg_write(reg,v)
    counts={a:0 for a in helpers};services=[];instructions=0;done=False
    def hook(machine,pc,size,user):
        nonlocal instructions,done
        if pc==STOP:done=True;machine.emu_stop();return
        if pc in helpers:counts[pc]+=1
        if any(a<=pc<a+n for a,n in helpers.items()):instructions+=1;return
        if pc in SERVICES:
            args=[machine.reg_read(r)for r in REG[:SERVICES[pc]]];services.append(dict(address=hex(pc),args=args));result=0
            if pc==0x020c5868:result=FIELD
            elif pc==0x0203d294:result=case['rng']
            elif pc==0x021dc374:
                if args[:3]!=[ACTOR+112,ACTOR+528,STACK-24]:raise ValueError('Actual collision vector ABI/frame differs')
                machine.mem_write(args[2],word(0x11223344)+word(case['collisionY'])+word(0x55667788));result=int(case['collision'])
            machine.reg_write(REG[0],result);machine.reg_write(UC_ARM_REG_PC,machine.reg_read(UC_ARM_REG_LR));return
        if not address<=pc<address+len(body):raise ValueError(('Unqualified actor/provider body execution',hex(pc)))
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(address,STOP+4,count=3000)
    if not done or uc.reg_read(UC_ARM_REG_SP)!=STACK or[uc.reg_read(r)for r in SAVED]!=saved:raise ValueError('Complete actor return/SP/callee-saved contract differs')
    result=dict(returnWord=uc.reg_read(REG[0]),actor=bytes(uc.mem_read(ACTOR,len(actor))).hex(),services=services,helpers={hex(a):n for a,n in counts.items()})
    expected=model(address,case)
    if result!=expected:raise ValueError(('Independent actor/record/state/DSP model differs',row['address'],case,result,expected))
    return result,dict(helperInvocations=sum(counts.values()),helperInstructions=instructions,serviceEntries=len(services),returned=True)


def execute(rows):
    value,image,inventory,records,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes();rng=random.Random(20261106752);records=[];helper_calls=0;helper_insns=0;service_calls=0
    for helper in value['executedAcceptedHelpers']:
        address=int(helper['address'],0);base=0x02000000 if helper['module']=='main'else BASE;raw=main if helper['module']=='main'else image;config=main_inventory if helper['module']=='main'else inventory
        if(helper['processor'],helper['mode'])!=('arm9','arm')or sha256(ROOT/helper['sourceUnit'])!=helper['sourceSha256']:raise ValueError('Actual accepted helper source/CPU/mode differs')
        if hashlib.sha256(raw[address-base:address-base+helper['bytes']]).hexdigest()!=helper['targetSha256']or not re.search(r'^\S+ kind:function\(arm,size=0x%x\) addr:0x%08x$'%(helper['bytes'],address),config,re.M):raise ValueError('Actual executed whole helper body/native boundary differs')
    states=[9,4,3,6,7,8,0,3,5,10,255,1];phases=[0,10,10,20,30,30,40,40,100,255,10,30];timers=[0,1,2,-1,14,15,0,1,32767,-32768,-32768,32767]
    for row in rows:
        a=int(row['address'],0);native=image[a-BASE:a-BASE+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes()
        for index in range(12):
            actor=bytearray(rng.randbytes(708));field=bytearray(rng.randbytes(44));struct.pack_into('<h',actor,630,[-32768,-1,0,1,32767][index%5]);actor[632]=states[index];actor[633]=phases[index];struct.pack_into('<h',actor,634,timers[index]);actor[482]=index%2;actor[484]=int(index%3==0);actor[485]=int(index%4==0);field[7]=[6,8,6,8,6,1,2,6,8,6,0,255][index];field[8]=3 if index%2 else 0;field[10]=[7,7,0,5,7,6,0,0,7,8,0,7][index]
            if a==0x02210008:
                actor[632]=[9,1,7,3,3,6,6,0,255,4,8,10][index]
                field[7]=8 if index==3 else 6
                field[8]=3 if index==5 else 0
            case=dict(actor=actor.hex(),field=field.hex(),cached=index%2==0,collision=index%3==0,collisionY=0x76543210+index,rng=[0,31,123456][index%3]);pair=[];counts=[]
            for body in[native,compiled]:
                result,count=execute_one(row,body,case,value,image,main);pair.append(result);counts.append(count);helper_calls+=count['helperInvocations'];helper_insns+=count['helperInstructions'];service_calls+=count['serviceEntries']
            if pair[0]!=pair[1]:raise ValueError('Original/C complete actor results differ')
            records.append(dict(address=row['address'],case=index,input=case,result=pair[0],executions=counts))
    trace=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest();limits=['Synthetic708-byte actor and44-byte field records; no scene/map/physics/animation/network/device execution.', 'Actual accepted68B FieldRecord getter,160B state setter,16B active-byte setter and64B flag setter execute where called; no additional helper/source/storage credit.', 'Cache/fallback,collision,RNG,animation andangle providers supply bounded results/effects and execute0body instructions; collision caller contract and DSP word-wrap effects are independently modeled.', 'Metadata byte7/8/10/12 and actor field semantics are measured offsets; gameplay labels remain inferred.']
    result=dict(passed=True,functions=len(rows),vectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualOriginalHelperInvocations=helper_calls,actualOriginalHelperInstructions=helper_insns,suppliedServiceCalls=service_calls,suppliedServiceBodyInstructionsExecuted=0,traceSha256=trace,limits=limits,records=records);write_json(EVIDENCE/'caller-fixtures.json',result);return result
