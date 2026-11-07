import hashlib
import json
import struct
import match_runtime
from project import ROOT,write_json,sha256
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
from wave20261106_ov000_roster_menu_source_first_paths import EVIDENCE
from wave20261106_ov000_roster_menu_source_first_bindings import inputs

REG=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]
SAVED=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
BASE=0x021d7240
MENU=0x022459b4
READY=0x0224532c+28
STACK=0x03030000
POINT=STACK-16
STOP=0x0303f000
SERVICES={0x021f7f9c:0,0x021f8044:0,0x0204b1c4:6,0x0204b380:2,0x021f9148:1,0x02062120:1,0x0206d250:1,0x0204b2d0:3,0x021f95b0:1,0x021f8b40:0,0x021f8c20:0,0x021f8d28:0,0x02063b40:1,0x021f8db4:3}


def word(v):return struct.pack('<I',v&0xffffffff)


def s8(v):return(v+128)%256-128


def s16(v):return(v+32768)%65536-32768


def model(case):
    menu=bytearray.fromhex(case['menu']);services=[];helpers={a:0 for a in[0x02215698,0x02215a7c,0x021f9118,0x021f9484]};observations=[]
    def service(address,args,point=None):
        event=dict(address=hex(address),args=[v&0xffffffff for v in args])
        if point is not None:event['pointAtEntry']=list(point)
        services.append(event)
    helpers[0x02215698]+=1;helpers[0x02215a7c]+=1
    ready=case['ready']
    if not ready:service(0x021f7f9c,[]);ready=1
    service(0x021f8044,[])
    if case['providerChangesMode']:
        menu[1178]=0;menu[1169]=2
    initial=case['initialPoint'];service(0x0204b1c4,[MENU+16,0,POINT,2,2,15],initial);observations.append(dict(provider='0x204b1c4',pointAtEarlierEntry=list(initial)))
    struct.pack_into('<hh',menu,36,*initial)
    service(0x0204b380,[MENU+16,0])
    if not menu[1178]:
        service(0x021f9148,[0]);menu[1168]=0;menu[1169]=0
        service(0x02062120,[s8(menu[1169])])
        index=s8(menu[1169]);slot=160+index*8;position=[menu[slot+4],menu[slot+5]]
        service(0x0206d250,[s8(menu[slot+6])]);service(0x0204b2d0,[MENU+16,case['height'],POINT],position)
    else:
        row=s8(menu[1168]);column=s8(menu[1169]);helpers[0x021f9118]+=1;helpers[0x02215698]+=1
        service(0x021f95b0,[(row+column*4)&255]);menu[1168]=row&255;menu[1169]=column&255
        helpers[0x021f9484]+=1;position=[s16(row*40+88),s16(column*40+48)]
        service(0x0204b2d0,[MENU+16,0,POINT],position)
    struct.pack_into('<hh',menu,36,*position)
    for address in[0x021f8b40,0x021f8c20,0x021f8d28]:service(address,[])
    for first,second,index in[(3,7,144),(4,8,75),(5,9,76),(6,6,22),(7,10,23)]:
        service(0x02063b40,[index]);service(0x021f8db4,[first,second,case['saveValues'][str(index)]&255])
    observations.append(dict(laterPoint=list(position),earlierObservationUnchanged=observations[0]['pointAtEarlierEntry']==list(initial)))
    return dict(menu=menu.hex(),ready=ready,services=services,helpers={hex(a):n for a,n in helpers.items()},pointObservations=observations)


def execute_one(row,body,case,value,image,main):
    address=int(row['address'],0);helpers={int(e['address'],0):e['bytes']for e in value['executedAcceptedHelpers']};uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(0x02000000,0x00400000);uc.mem_map(0x03000000,0x40000);uc.mem_write(0x02000000,main);uc.mem_write(BASE,image);uc.mem_write(address,body);uc.mem_write(MENU,bytes.fromhex(case['menu']));uc.mem_write(READY,word(case['ready']));uc.mem_write(STACK-128,bytes([case['stackSeed']])*256);uc.mem_write(POINT,struct.pack('<hh',*case['initialPoint']));uc.reg_write(UC_ARM_REG_SP,STACK);uc.reg_write(UC_ARM_REG_LR,STOP)
    saved=[0x70700000+i for i in range(8)]
    for register,v in zip(SAVED,saved):uc.reg_write(register,v)
    counts={a:0 for a in helpers};services=[];observations=[];instructions=0;done=False
    def hook(machine,pc,size,user):
        nonlocal instructions,done
        if pc==STOP:done=True;machine.emu_stop();return
        if pc in helpers:counts[pc]+=1
        if any(a<=pc<a+n for a,n in helpers.items()):instructions+=1;return
        if pc in SERVICES:
            args=[machine.reg_read(r)for r in REG[:min(4,SERVICES[pc])]]
            if SERVICES[pc]>4:args.extend(struct.unpack('<'+'I'*(SERVICES[pc]-4),bytes(machine.mem_read(machine.reg_read(UC_ARM_REG_SP),4*(SERVICES[pc]-4)))))
            event=dict(address=hex(pc),args=args);result=0
            if pc in[0x0204b1c4,0x0204b2d0]:
                point=list(struct.unpack('<hh',bytes(machine.mem_read(args[2],4))));event['pointAtEntry']=point;machine.mem_write(MENU+36,struct.pack('<hh',*point))
                if pc==0x0204b1c4:observations.append(dict(provider='0x204b1c4',pointAtEarlierEntry=list(point)))
                else:observations.append(dict(laterPoint=list(point),earlierObservationUnchanged=observations[0]['pointAtEarlierEntry']==list(case['initialPoint'])))
            elif pc==0x021f7f9c:machine.mem_write(READY,word(1))
            elif pc==0x021f8044 and case['providerChangesMode']:machine.mem_write(MENU+1178,bytes([0]));machine.mem_write(MENU+1169,bytes([2]))
            elif pc==0x021f9148:machine.mem_write(MENU+1168,bytes([0,args[0]&255]));result=1
            elif pc==0x0206d250:result=case['height']
            elif pc==0x02063b40:result=case['saveValues'][str(args[0])]
            elif pc==0x021f8db4:result=0x51510000+args[0]
            services.append(event);machine.reg_write(REG[0],result&0xffffffff);machine.reg_write(UC_ARM_REG_PC,machine.reg_read(UC_ARM_REG_LR));return
        if address<=pc<address+len(body):return
        raise ValueError(('Unqualified native execution',hex(pc)))
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(address,STOP+4,count=3000)
    if not done or uc.reg_read(UC_ARM_REG_SP)!=STACK or[uc.reg_read(r)for r in SAVED]!=saved:raise ValueError('Caller return/SP/callee-saved state differs')
    actual=dict(menu=bytes(uc.mem_read(MENU,len(bytes.fromhex(case['menu'])))).hex(),ready=struct.unpack('<I',bytes(uc.mem_read(READY,4)))[0],services=services,helpers={hex(a):n for a,n in counts.items()},pointObservations=observations)
    expected=model(case)
    if actual!=expected:raise ValueError(('Independent incoming-stack/caller model differs',case['case'],actual,expected))
    if bytes(uc.mem_read(POINT,4))!=struct.pack('<hh',*observations[-1]['laterPoint']):raise ValueError('Later actual caller Point writes differ')
    return dict(returned=True,helperInvocations=sum(counts.values()),helperInstructions=instructions,suppliedServiceCalls=len(services),suppliedServiceBodyInstructions=0,pointObservations=observations,modelSha256=hashlib.sha256(json.dumps(expected,sort_keys=True).encode()).hexdigest(),voidCallerRegisterReturnNotPortableValue=True)


def cases():
    values=[(-32768,32767),(1,-1),(1234,-2345),(17,19),(-80,400),(32767,-32768),(0,0),(-1,-1)]
    result=[]
    for i,point in enumerate(values):
        menu=bytearray((j*17+i*13)&255 for j in range(1180));menu[1168]=[0,3,127,-128,-1,1,2,0][i]&255;menu[1169]=[0,1,2,-1,127,2,1,0][i]&255;menu[1178]=[0,0,1,1,2,255,1,0][i]
        for slot in range(3):struct.pack_into('<I',menu,160+slot*8,0x11110000+slot);menu[164+slot*8]=[0,255,88][slot];menu[165+slot*8]=[255,0,128][slot];menu[166+slot*8]=[127,128,255][(slot+i)%3]
        result.append(dict(case=i,menu=menu.hex(),ready=i%2,initialPoint=list(point),stackSeed=0x30+i,height=[0,1,2,255,3,0xffffffff,4,5][i],providerChangesMode=i==6,saveValues={str(index):(index*29+i*257)&0xffffffff for index in[144,75,76,22,23]}))
    return result


def execute(rows):
    value,image,inventory,records,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes()
    for helper in value['executedAcceptedHelpers']:
        a=int(helper['address'],0);body=image[a-BASE:a-BASE+helper['bytes']]
        if sha256(ROOT/helper['sourceUnit'])!=helper['sourceSha256']or hashlib.sha256(body).hexdigest()!=helper['targetSha256']:raise ValueError('Actual accepted helper source/native span changed')
    vectors=cases();proof=[]
    for row in rows:
        a=int(row['address'],0);original=image[a-BASE:a-BASE+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes()
        for case in vectors:proof.append(dict(address=row['address'],case=case['case'],initialPoint=case['initialPoint'],executions=[execute_one(row,body,case,value,image,main)for body in[original,compiled]]))
    trace=hashlib.sha256(json.dumps(proof,sort_keys=True).encode()).hexdigest();result=dict(passed=True,records=proof,returningVectors=len(vectors),nativeAndCompiledReturningCalls=2*len(proof),actualOriginalHelperInvocations=sum(x['helperInvocations']for p in proof for x in p['executions']),actualOriginalHelperInstructions=sum(x['helperInstructions']for p in proof for x in p['executions']),suppliedServiceCalls=sum(x['suppliedServiceCalls']for p in proof for x in p['executions']),traceSha256=trace,suppliedServiceBodyInstructionsExecuted=0,actual268ByteInitialProviderExecuted=False,incomingStackPoints=[c['initialPoint']for c in vectors],limits=['Actual complete400B original/compiled caller and four accepted original helper extents execute; supplied providers receive0body credit.','Point local is uninitialized at first268B provider boundary. Distinct initialized fixture stacks are synthetic machine inputs; this proves incoming-stack dependence,not defined portablehost-C initialization.','Earlier provider Point reads are immutable snapshots; later caller writes and supplied update effects mustnot change earlier observations.','Opaque UI/audio/save/display providers have explicit bounded supplied reads/effects,not real device/scene execution. Voidcaller R0 isnot claimed as a defined portableC return value.','Actual021f9118 helper alwaysreturns1; its fallback branch is byte-proven but not credited as reachable game behavior. All imported helpers/storage0newauthorship.'])
    write_json(EVIDENCE/'caller-fixtures.json',result);return result
