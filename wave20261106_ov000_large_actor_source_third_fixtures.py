import hashlib
import json
import random
import re
import struct
import match_runtime
from project import ROOT,write_json,sha256
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
from wave20261106_ov000_large_actor_source_third_paths import EVIDENCE
from wave20261106_ov000_large_actor_source_third_bindings import inputs

REG=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]
SAVED=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
BASE=0x021d7240
ACTOR=0x03008000
FIELD=0x03011000
TARGET=0x03012000
STACK=0x03030000
STOP=0x0303f000
SERVICES={0x020c5750:1,0x020c5868:1,0x0220a2a4:3,0x0203d294:1,0x0220cbe0:1,0x0220ce54:1,0x0220e0d8:1,0x021e60a8:2,0x021e07b8:1,0x020420c4:2}


def word(v):return struct.pack('<I',v&0xffffffff)


def signed(v):return(v+0x80000000)%0x100000000-0x80000000


def normalize(v):
    v=signed(v)
    while v>0xb4000:v-=0x168000
    while v < -0xb4000:v+=0x168000
    return v


def model(case):
    actor=bytearray.fromhex(case['actor']);field=bytes.fromhex(case['field']);services=[];helpers={a:0 for a in[0x020c56b4,0x02042c0c,0x02028158,0x02042104,0x02209c68]}
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
    def active(value):helpers[0x02042c0c]+=1;actor[352]=value&255
    def angle_add(value):
        helpers[0x02042104]+=1;helpers[0x02028158]+=1;previous=get32(140);set32(140,normalize(previous+value));actor[9]|=int(signed(previous)!=signed(value))
    def low(value):actor[706]=(actor[706]&240)|(value&15)
    result=0
    if actor[633]==0:
        service(0x0220cbe0,[ACTOR])
        if not case['ready']:state(6)
        else:service(0x0220ce54,[ACTOR]);service(0x0203d294,[0x7fffffff]);set_timer((case['rng']&31)+60);actor[633]=10
    if actor[633]==10:
        set_timer(timer()-1)
        if timer()<=0:
            service(0x0220a2a4,[ACTOR,0,0]);angle_add(737280);state(7 if record()[7]==6 else 3);result=1
        if actor[706]>>4==1:
            service(0x0220e0d8,[ACTOR])
            if case['destinationIndex']>=0:actor[656]=case['destinationIndex']&255;actor[633]=50
    if actor[633]==50:service(0x0220a2a4,[ACTOR,0,0]);set_timer(0);actor[633]=52
    if actor[633]==52:
        remaining=31-timer()
        if remaining<=0:actor[633]=54
        else:active(remaining);set_timer(timer()+2)
        low(int(remaining<20))
    if actor[633]==54:
        service(0x021e60a8,[actor[656],STACK-32]);actor[112:124]=bytes.fromhex(case['destination']);actor[272:284]=bytes.fromhex(case['destination']);service(0x021e07b8,[0]);service(0x020420c4,[ACTOR,TARGET]);set_timer(0);actor[633]=56
    if actor[633]==56:
        old=timer();active(old)
        if old>=31:actor[633]=58
        else:set_timer(old+2)
        low(int(old<20))
    if actor[633]==58:service(0x0220a2a4,[ACTOR,2,0]);actor[633]=0;state(7 if record()[7]==6 else 3);result=1
    return dict(returnWord=result,actor=actor.hex(),services=services,helpers={hex(a):n for a,n in helpers.items()})


def execute_one(row,body,case,value,image,main):
    address=int(row['address'],0);actor=bytes.fromhex(case['actor']);identifier=struct.unpack_from('<h',actor,630)[0];helpers={int(e['address'],0):e['bytes']for e in value['executedAcceptedHelpers']};uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(0x02000000,0x00400000);uc.mem_map(0x03000000,0x40000);uc.mem_write(0x02000000,main);uc.mem_write(BASE,image);uc.mem_write(address,body);uc.mem_write(ACTOR,actor);uc.mem_write(FIELD,bytes.fromhex(case['field']));uc.mem_write(TARGET,bytes(12));uc.mem_write(0x021d5404,word(0)+word((FIELD-44*identifier)&0xffffffff if case['cached']else 0));uc.reg_write(REG[0],ACTOR);uc.reg_write(UC_ARM_REG_SP,STACK);uc.reg_write(UC_ARM_REG_LR,STOP)
    saved=[0x70700000+i for i in range(8)]
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
            elif pc==0x0220cbe0:result=int(case['ready'])
            elif pc==0x0203d294:result=case['rng']
            elif pc==0x0220e0d8:result=case['destinationIndex']
            elif pc==0x021e60a8:
                if args[1]!=STACK-32:raise ValueError('Actual destination Vec3 stack/width ABI differs')
                machine.mem_write(args[1],bytes.fromhex(case['destination']))
            machine.reg_write(REG[0],result&0xffffffff);machine.reg_write(UC_ARM_REG_PC,machine.reg_read(UC_ARM_REG_LR));return
        if not address<=pc<address+len(body):raise ValueError(('Unqualified fade/provider body execution',hex(pc)))
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(address,STOP+4,count=30000)
    if not done or uc.reg_read(UC_ARM_REG_SP)!=STACK or[uc.reg_read(r)for r in SAVED]!=saved:raise ValueError('Complete fade return/SP/preserved register contract differs')
    result=dict(returnWord=uc.reg_read(REG[0]),actor=bytes(uc.mem_read(ACTOR,len(actor))).hex(),services=services,helpers={hex(a):n for a,n in counts.items()});expected=model(case)
    if result!=expected:raise ValueError(('Independent fade/teleport/union/nibble model differs',row['address'],case,result,expected))
    return result,dict(helperInvocations=sum(counts.values()),helperInstructions=instructions,serviceEntries=len(services),returned=True)


def execute(rows):
    value,image,inventory,records,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes();rng=random.Random(20261106704);records=[];helper_calls=0;helper_insns=0;service_calls=0
    for helper in value['executedAcceptedHelpers']:
        address=int(helper['address'],0);base=0x02000000 if helper['module']=='main'else BASE;raw=main if helper['module']=='main'else image;config=main_inventory if helper['module']=='main'else inventory
        if(helper['processor'],helper['mode'])!=('arm9','arm')or sha256(ROOT/helper['sourceUnit'])!=helper['sourceSha256']or hashlib.sha256(raw[address-base:address-base+helper['bytes']]).hexdigest()!=helper['targetSha256']or not re.search(r'^\S+ kind:function\(arm,size=0x%x\) addr:0x%08x$'%(helper['bytes'],address),config,re.M):raise ValueError('Executed actual helper identity differs')
    phases=[0,0,10,10,10,10,50,52,52,52,52,54,56,56,56,56,58,255,10,10,52,56,52,56,10,10,52,56,0,10,52,56];timers=[0,1,0,1,2,61,0,10,11,12,31,17,0,19,30,31,7,3,-32768,32767,-32768,-32768,32767,32767,0,1,32,32,0,1,30,20]
    for row in rows:
        a=int(row['address'],0);native=image[a-BASE:a-BASE+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes()
        for index in range(len(phases)):
            actor=bytearray(rng.randbytes(708));field=bytearray(rng.randbytes(44));struct.pack_into('<h',actor,630,[-32768,-1,0,1,32767][index%5]);actor[632]=[3,7,8,0][index%4];actor[633]=phases[index];struct.pack_into('<h',actor,634,timers[index]);actor[706]=[0x10,0x1f,0x20,0xff,0x00][index%5];struct.pack_into('<I',actor,140,[0,0xb4000,(-0xb4000)&0xffffffff][index%3]);field[7]=6 if index%2 else 8;case=dict(actor=actor.hex(),field=field.hex(),cached=index%2==0,ready=index%3!=0,rng=[0,31,0x7ffffffe][index%3],destinationIndex=[-1,0,15][index%3],destination=(word(0x12345678)+word(0x87654321)+word(index)).hex());pair=[];counts=[]
            for body in[native,compiled]:
                result,count=execute_one(row,body,case,value,image,main);pair.append(result);counts.append(count);helper_calls+=count['helperInvocations'];helper_insns+=count['helperInstructions'];service_calls+=count['serviceEntries']
            if pair[0]!=pair[1]:raise ValueError('Complete original/C fade effects differ')
            records.append(dict(address=row['address'],case=index,input=case,result=pair[0],executions=counts))
    trace=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest();limits=['Synthetic708-byte actors,44-byte metadata and provided destination/target vectors; no fullgame/teleport/animation/device execution.', 'Five actual accepted getter/byte/state/angle-add/normalizer helper bodies execute wherecalled,with angle-updateargument0. No additional helper/source/storage credit.', 'Readiness/setup/RNG/destination-index/destination-vector/target/orientation/animation providers supply bounded values/effects and execute0body instructions.', 'Exact low/high4-bit flags,byte index versus12-byte state-dependent scratch union,Vec3 copies at0x70/0x110,signed16 timers and same-call phase cascades are independently modeled.']
    result=dict(passed=True,functions=len(rows),vectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualOriginalHelperInvocations=helper_calls,actualOriginalHelperInstructions=helper_insns,suppliedServiceCalls=service_calls,suppliedServiceBodyInstructionsExecuted=0,traceSha256=trace,limits=limits,records=records);write_json(EVIDENCE/'caller-fixtures.json',result);return result
