import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from project import ROOT
from wave20261106_ov006_resource_slot_source_first_bindings import inputs

STACK=0x3009000
STOP=0x4000000
ENTRY=0x3101000
LINK=0x3102000
RESOURCE=0x3103000
ACTIVE=0x3104000
SCENE=0x2218d90
CURSORS=0x2218df8
ID=0x220d114
SPECS=0x2207e4f
INDEX=0x2219160


def word(v):return v&0xffffffff
def signed8(v):return((v&255)^128)-128


class Memory:
    def __init__(self):self.data={}
    def put(self,a,b):self.data.update((a+i,v)for i,v in enumerate(b))
    def get(self,a,n):return bytes(self.data.get(a+i,0)for i in range(n))
    def u32(self,a):return struct.unpack('<I',self.get(a,4))[0]
    def set32(self,a,v):self.put(a,struct.pack('<I',word(v)))
    def regions(self,regions):return[dict(address=hex(a),bytes=self.get(a,n).hex())for a,n in regions]


def plan(row,case,image,base):
    a=int(row['address'],0);m=Memory();m.put(SCENE,bytes((i*37+case)&255 for i in range(128)));m.put(ENTRY,bytes([0x72])*12);m.set32(ENTRY,LINK);m.set32(LINK,0);m.set32(LINK+4,RESOURCE);m.put(RESOURCE+0x1c,bytes([0,127,128,255]));m.put(ENTRY+5,bytes([127]));m.put(ID,bytes([17]));m.set32(SCENE+0x34,ACTIVE);initial=[];events=[];regions=[(SCENE,128),(ENTRY,12),(RESOURCE,128),(ID,1)];args=[];answer=0
    def event(addr,args=(),result=0x7bad0000,effects=(),checks=()):
        record=dict(address=addr,args=tuple(word(x)for x in args),result=word(result),effects=[dict(address=hex(x),bytes=bytes(b).hex())for x,b in effects],checks=[dict(address=hex(x),bytes=bytes(b).hex())for x,b in checks]);events.append(record)
        for x,b in effects:m.put(x,b)
    if a==0x21e6c44:
        specs=bytearray(image[SPECS-base:SPECS-base+33]);
        if case%2:specs[4]=1
        m.put(SPECS,specs);regions.extend([(SPECS,33),(CURSORS,32)]);initial=dict(m.data)
        event(0x205fd80,(0,))
        for i in range(4):m.set32(CURSORS+i*4,32)
        for target,p in[(0x2048f1c,(2,0)),(0x2048f2c,(0,0)),(0x2046150,(0,0,1))]:event(target,p)
        for i in range(4):event(0x2045654,(i,))
        for i in[1,2,0]:
            buffer=0x3106000+i*0x100;event(0x2045514,(i,),buffer);event(0x2008c58,(0,buffer,32),effects=[(buffer,bytes(32))])
        file_size=32+case;asset1=0x3107000;asset2=0x3107100
        event(0x202a8e0,(0x2207e88,),file_size);event(0x203cc2c,(0x2207e88,1),asset1);event(0x20481b8,(asset1,0,file_size));event(0x20481b8,(0x2207dbe,0,2));event(0x202a498,(1,asset1));event(0x22076b4,(0,));event(0x203cc2c,(0x2207e9c,1),asset2)
        m.set32(SCENE+0x70,0x3000);event(0x204540c,(2,asset2,0,0x3000),checks=[(CURSORS+8,struct.pack('<I',0x3000))]);event(0x202a498,(1,asset2));event(0x205ff80,(0x220d334,))
        for i in range(11):
            p=SPECS+i*3;tag,font,mode=m.get(p,3)
            if font==0:
                cursor=CURSORS+font*16+mode*4;loaded=word(0xfffffff0+case+i*7);effects=[]
                if case>=2 and i==0:effects=[(p+1,b'\x01\x03'),(CURSORS+28,struct.pack('<I',0xfffffffd))]
                event(0x2065730,(0x2218fc8+i*12,word(signed8(tag)),font,mode,m.u32(cursor)),loaded,effects=effects)
                font,mode=m.get(p+1,2);post=CURSORS+font*16+mode*4;m.set32(post,m.u32(post)+loaded)
        event(0x205ff9c);event(0x21e7370,(0xffffffff,));event(0x204b9d0,(1,CURSORS),checks=[(CURSORS,m.get(CURSORS,32))]);answer=0x12340000+case;event(0x2048308,(),answer)
    elif a==0x21e7268:
        if case%2==0:m.set32(SCENE+0x34,0)
        initial=dict(m.data)
        if case%2:
            event(0x20485b4,(ACTIVE,),effects=[(ID,bytes([128+case]))]);event(0x20484dc,(1,128+case));m.set32(SCENE+0x34,0);m.put(ID,b'\x7f');answer=ID
    elif a==0x21e75ec:
        args=[word(case*71-129)];initial=dict(m.data);answer=[0,1,0x80000000,0xffffffff][case%4];event(0x21e749c,(args[0],0,0,0xffffffff,0xffffffff),answer)
    elif a==0x21e7608:
        args=[word(case*17-129)]
        if case==1:m.set32(ENTRY,0)
        if case==2:m.set32(LINK+4,0)
        initial=dict(m.data);event(0x21e75ec,(args[0],),0 if case==0 else 1)
        if case:
            event(0x2049ad0,(word(signed8(args[0])),),ENTRY)
            if m.u32(ENTRY):
                if m.u32(LINK+4):event(0x205ff4c,(LINK,))
                m.set32(ENTRY,0)
            m.put(ENTRY+4,b'\xff\xff\xff\x00');m.set32(ENTRY+8,0);answer=1
    elif a==0x21e76f0:
        args=[word(case*33-129),0x10203040+case]
        if case==1:m.set32(ENTRY,0)
        if case==2:m.set32(LINK+4,0)
        initial=dict(m.data);event(0x2049ad0,(word(signed8(args[0])),),0 if case==0 else ENTRY)
        if case>=3:
            tag=127 if case%2 else 255;event(0x204a0b0,(RESOURCE,args[1]),effects=[(ENTRY+5,bytes([tag]))]);event(0x2085270,(RESOURCE+0x3c,0 if tag==127 else 8,0));answer=1
    elif a==0x21e79b0:
        args=[0x87650000+case,0 if case%2==0 else 0x80000000,0x13570000+case];initial=dict(m.data);event(0x20414c8,(63,));event(0x204157c,(0,));event(0x2041538,(args[0],2 if args[1]==0 else 3,args[2]));m.set32(SCENE+0x28,0);m.set32(SCENE+0x4c,0);answer=SCENE
    elif a==0x21e7ab0:
        args=[case,0x1234007f,0x12340080,0x123400ff,0x87650080+case];initial=dict(m.data);handle=0x3130400+case;event(0x21e7a9c,(args[0],),handle);event(0x206006c,(handle,*[word(signed8(v))for v in args[1:]]));answer=1
    elif a==0x21e7b00:
        args=[case];m.set32(INDEX+case*4,16-case);regions.append((INDEX,32))
        if case==1:m.set32(ENTRY,0)
        initial=dict(m.data);event(0x2049ad0,(case,),0 if case==0 else ENTRY)
        if case>=2:event(0x21e7ab0,(16-case,0,127,128,255));answer=1
    else:raise ValueError('No independent caller model')
    return dict(args=args,initial=initial,events=events,returnValue=word(answer),regions=regions,final=m.regions(regions))


def execute(row,code,p):
    address=int(row['address'],0);uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(0x2000000,0x300000);uc.mem_map(0x3000000,0x10000);uc.mem_map(0x3100000,0x10000);uc.mem_map(STOP,0x1000);uc.mem_write(address,bytes(code));uc.mem_write(STOP,b'\x1e\xff\x2f\xe1')
    for a,b in p['initial'].items():uc.mem_write(a,bytes([b]))
    uc.reg_write(UC_ARM_REG_CPSR,0x10);uc.reg_write(UC_ARM_REG_SP,STACK);uc.reg_write(UC_ARM_REG_LR,STOP);regs=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3];saved={r:0x77550000+i for i,r in enumerate([UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11])}
    for r,v in saved.items():uc.reg_write(r,v)
    for r,v in zip(regs,p['args'][:4]):uc.reg_write(r,v)
    if len(p['args'])>4:uc.mem_write(STACK,struct.pack('<%dI'%(len(p['args'])-4),*p['args'][4:]))
    event_index=0;steps=0;returned=False;targets={int(r['target'],0)for r in row['relocations']if r['type']==1};trace=[]
    def hook(engine,pc,size,data):
        nonlocal event_index,steps,returned
        if pc==STOP:returned=True;engine.emu_stop();return
        if pc in targets:
            if event_index>=len(p['events']):raise ValueError('Unexpected supplied helper invocation')
            e=p['events'][event_index];count=len(e['args']);args=[word(engine.reg_read(r))for r in regs[:min(count,4)]]
            if count>4:args.extend(struct.unpack('<%dI'%(count-4),engine.mem_read(engine.reg_read(UC_ARM_REG_SP),4*(count-4))))
            if pc!=e['address']or tuple(args)!=e['args']:raise ValueError(('Independent caller provider argument/order mismatch',event_index,hex(pc),args,e))
            for check in e['checks']:
                if bytes(engine.mem_read(int(check['address'],0),len(bytes.fromhex(check['bytes'])))).hex()!=check['bytes']:raise ValueError('Native/C pre-provider memory snapshot mismatch')
            for effect in e['effects']:engine.mem_write(int(effect['address'],0),bytes.fromhex(effect['bytes']))
            for i,r in enumerate([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12]):engine.reg_write(r,0xbb110000+i)
            engine.reg_write(UC_ARM_REG_R0,e['result']);engine.reg_write(UC_ARM_REG_PC,engine.reg_read(UC_ARM_REG_LR));trace.append((pc,args));event_index+=1;return
        if not address<=pc<address+len(code):raise ValueError('Caller escaped exact source body/qualified supplied services')
        steps+=1
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(address,STOP+4,count=20000)
    if not returned or event_index!=len(p['events'])or word(uc.reg_read(UC_ARM_REG_R0))!=p['returnValue']or uc.reg_read(UC_ARM_REG_SP)!=STACK or any(uc.reg_read(r)!=v for r,v in saved.items()):raise ValueError('Independent caller return/ABI/service-count mismatch')
    final=[dict(address=hex(a),bytes=bytes(uc.mem_read(a,n)).hex())for a,n in p['regions']]
    if final!=p['final']:raise ValueError('Independent caller physical memory/write oracle mismatch')
    return dict(returnValue=p['returnValue'],trace=trace,instructions=steps,final=final)


def check(rows,flats,negative=False):
    value,images,inventories,relocations=inputs();base=int(value['images']['ov006']['base'],0);records=[]
    for row,flat in zip(rows,flats):
        a=int(row['address'],0);native=images['ov006'][a-base:a-base+row['bytes']]
        for case in range(6):
            p=plan(row,case,images['ov006'],base);original=execute(row,native,p)
            try:compiled=execute(row,flat,p)
            except ValueError as error:
                if negative:return dict(rejected=True,address=row['address'],case=case,reason=str(error))
                raise
            records.append(dict(address=row['address'],case=case,original=original,compiled=compiled))
    if negative:raise ValueError('Wrong C passed independent physical-memory caller model')
    return dict(passed=True,records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeHelperInvocations=0,suppliedServiceCalls=sum(len(r[k]['trace'])for r in records for k in['original','compiled']),physicalAliasExplicit=dict(scene='0x2218d90',cursor='0x2218df8',offset=104,sceneWord70EqualsCursorRow0Column2=True,storageAuthorshipCredit=0,portableGlobalDeclarationUnificationUnproved=True),limits='Only complete original/C caller bodies execute. All supplied helpers and IO/font/resource services receive zero body/instruction credit. The reset-success model requires the actual entry getter nonnull, matching its measured native address domain; invalid null-after-success dereferences are not returning coverage. Imported scene/cursor aliases share one physical memory map. No authored storage,game execution,hardware transfer,transitive application reachability or native Windows proof.')
