import hashlib
import json
import random
import re
import struct
import match_runtime
from project import ROOT,write_json,sha256
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
from wave20261106_ov000_large_actor_source_first_paths import EVIDENCE
from wave20261106_ov000_large_actor_source_first_bindings import inputs
from wave20261106_ov000_large_actor_source_first_angle_abi import signed,normalize

REG=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]
SAVED=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
BASE=0x021d7240
ACTOR=0x03008000
FIELD=0x03011000
STACK=0x03030000
STOP=0x0303f000
SERVICES={0x020c5750:1,0x020c5868:1,0x0220a2a4:3,0x0203d294:1,0x02041f90:3,0x0220f018:1}


def word(value):return struct.pack('<I',value&0xffffffff)


def model(address,case):
    actor=bytearray.fromhex(case['actor']);field=bytes.fromhex(case['field']);services=[];helpers={0x020c56b4:0,0x02042bfc:0,0x02042c2c:0,0x02028158:0,0x02042c0c:0,0x0221089c:0}
    def get32(offset):return struct.unpack_from('<I',actor,offset)[0]
    def set32(offset,value):struct.pack_into('<I',actor,offset,value&0xffffffff)
    def timer():return struct.unpack_from('<h',actor,634)[0]
    def set_timer(value):struct.pack_into('<H',actor,634,value&65535)
    def service(a,args):services.append(dict(address=hex(a),args=[v&0xffffffff for v in args]))
    def normal(value):helpers[0x02028158]+=1;return normalize(value)
    result=0
    if not actor[482]or not actor[352]:actor[633]=30
    if actor[633]==0:
        service(0x0220a2a4,[ACTOR,2,0]);helpers[0x020c56b4]+=1;identifier=struct.unpack_from('<h',actor,630)[0];service(0x020c5750 if case['cached']else 0x020c5868,[identifier]);helpers[0x02042bfc]+=1;set32(364,struct.unpack_from('<I',field,24)[0]);actor[706]=(actor[706]&240)|1;actor[633]=10
    if actor[633]==10:
        set_timer(timer()+1)
        if timer()<60:
            if timer()%30==0:
                service(0x0203d294,[2]);angle=normal(((case['rng']+1)*180+90)<<12);quotient=abs(angle)//30;set32(636,-quotient if angle<0 else quotient)
            helpers[0x02042c2c]+=1;angle=normal(get32(140)+get32(636));service(0x02041f90,[ACTOR,angle,0])
        elif address==0x0220f3dc:set_timer(31);actor[633]=20
        else:actor[633]=20
    if actor[633]==20:
        if address==0x0220f158:actor[633]=30;result=1
        else:
            set_timer(timer()-1)
            if timer()<=0:service(0x0220f018,[ACTOR]);actor[482]=0;actor[633]=30;result=1
            helpers[0x02042c0c]+=1;actor[352]=timer()&255;helpers[0x0221089c]+=1;actor[483]=0
    if actor[633]==30:actor[482]=0;actor[706]&=240;result=1
    return dict(returnWord=result,actor=actor.hex(),services=services,helpers={hex(a):n for a,n in helpers.items()})


def execute_one(row,body,case,value,image,main):
    address=int(row['address'],0);actor=bytes.fromhex(case['actor']);identifier=struct.unpack_from('<h',actor,630)[0];helpers={int(e['address'],0):e['bytes']for e in value['executedAcceptedHelpers']};uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(0x02000000,0x00400000);uc.mem_map(0x03000000,0x40000);uc.mem_write(0x02000000,main);uc.mem_write(BASE,image);uc.mem_write(address,body);uc.mem_write(ACTOR,actor);uc.mem_write(FIELD,bytes.fromhex(case['field']));uc.mem_write(0x021d5404,word(0)+word((FIELD-44*identifier)&0xffffffff if case['cached']else 0));uc.reg_write(REG[0],ACTOR);uc.reg_write(UC_ARM_REG_SP,STACK);uc.reg_write(UC_ARM_REG_LR,STOP)
    saved=[0x50500000+i for i in range(8)]
    for register,v in zip(SAVED,saved):uc.reg_write(register,v)
    counts={a:0 for a in helpers};services=[];instructions=0;done=False
    def hook(machine,pc,size,user):
        nonlocal instructions,done
        if pc==STOP:done=True;machine.emu_stop();return
        if pc in helpers:counts[pc]+=1
        if any(a<=pc<a+n for a,n in helpers.items()):instructions+=1;return
        if pc in SERVICES:
            args=[machine.reg_read(r)for r in REG[:SERVICES[pc]]];services.append(dict(address=hex(pc),args=args));result=FIELD if pc==0x020c5868 else case['rng']if pc==0x0203d294 else 0
            machine.reg_write(REG[0],result);machine.reg_write(UC_ARM_REG_PC,machine.reg_read(UC_ARM_REG_LR));return
        if not address<=pc<address+len(body):raise ValueError(('Unqualified large actor/provider body execution',hex(pc)))
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(address,STOP+4,count=30000)
    if not done or uc.reg_read(UC_ARM_REG_SP)!=STACK or[uc.reg_read(r)for r in SAVED]!=saved:raise ValueError('Complete larger actor return/SP/preserved register contract differs')
    result=dict(returnWord=uc.reg_read(REG[0]),actor=bytes(uc.mem_read(ACTOR,len(actor))).hex(),services=services,helpers={hex(a):n for a,n in counts.items()});expected=model(address,case)
    if result!=expected:raise ValueError(('Independent angle/turn/phase/record model differs',row['address'],case,result,expected))
    return result,dict(helperInvocations=sum(counts.values()),helperInstructions=instructions,serviceEntries=len(services),returned=True)


def execute(rows):
    value,image,inventory,records,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes();rng=random.Random(20261106808);records=[];helper_calls=0;helper_insns=0;service_calls=0
    for helper in value['executedAcceptedHelpers']:
        address=int(helper['address'],0);base=0x02000000 if helper['module']=='main'else BASE;raw=main if helper['module']=='main'else image;config=main_inventory if helper['module']=='main'else inventory
        if(helper['processor'],helper['mode'])!=('arm9','arm')or sha256(ROOT/helper['sourceUnit'])!=helper['sourceSha256']or hashlib.sha256(raw[address-base:address-base+helper['bytes']]).hexdigest()!=helper['targetSha256']or not re.search(r'^\S+ kind:function\(arm,size=0x%x\) addr:0x%08x$'%(helper['bytes'],address),config,re.M):raise ValueError('Original executed helper identity/source/mode/body differs')
    phases=[0,0,10,10,10,10,10,10,10,10,20,20,20,20,30,255,0,10,10,10,10,20,10,10];timers=[0,29,28,29,30,58,59,-1,-31,32767,0,1,2,-32768,0,3,58,-32768,0,59,60,32767,-30,-60]
    for row in rows:
        a=int(row['address'],0);native=image[a-BASE:a-BASE+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes()
        for index in range(24):
            actor=bytearray(rng.randbytes(708));field=bytearray(rng.randbytes(44));struct.pack_into('<h',actor,630,[-32768,-1,0,1,32767][index%5]);actor[633]=phases[index];struct.pack_into('<h',actor,634,timers[index]);actor[482]=0 if index==22 else 1;actor[352]=0 if index==23 else 31;actor[484]=index%2;actor[485]=int(index%4==0);actor[706]=[0xa5,0xff,0][index%3];struct.pack_into('<I',actor,140,[0,0xb4000,(-0xb4000)&0xffffffff][index%3]);struct.pack_into('<I',actor,636,[-12288&0xffffffff,12288,8192][index%3]);struct.pack_into('<I',field,24,[0xffffffff,0,0x80000000,0x12345][index%4]);case=dict(actor=actor.hex(),field=field.hex(),cached=index%2==0,rng=index%2);pair=[];counts=[]
            for body in[native,compiled]:
                result,count=execute_one(row,body,case,value,image,main);pair.append(result);counts.append(count);helper_calls+=count['helperInvocations'];helper_insns+=count['helperInstructions'];service_calls+=count['serviceEntries']
            if pair[0]!=pair[1]:raise ValueError('Complete original/C larger actor effects differ')
            records.append(dict(address=row['address'],case=index,input=case,result=pair[0],executions=counts))
    trace=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest();limits=['Synthetic708-byte actors and44-byte metadata; no fullscene/map/animation/physics/device execution.', 'Six actual accepted getter/setter/normalizer helper bodies execute where called; their code receives0newsourcecredit. Accepted02028158 definition remainsvoid despite observed signedR0 return; explicit zero-byte interface debt is separately pinned.', 'Cache/fallback,anim-start,RNG,angle-update andcleanup providers supply bounded values/noextra memoryeffects and execute0body instructions. Their services/returns are not game/nativeprovider executions.', 'Signed16 timer truncation,wordwrapped angle addition,signeddivision/modulo30,metadataword24 and observed call ordering are independently modeled.']
    result=dict(passed=True,functions=len(rows),vectors=len(records),nativeAndCompiledReturningCalls=2*len(records),actualOriginalHelperInvocations=helper_calls,actualOriginalHelperInstructions=helper_insns,suppliedServiceCalls=service_calls,suppliedServiceBodyInstructionsExecuted=0,traceSha256=trace,limits=limits,records=records);write_json(EVIDENCE/'caller-fixtures.json',result);return result
