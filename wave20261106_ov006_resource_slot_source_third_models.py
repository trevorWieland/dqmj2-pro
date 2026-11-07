import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from project import ROOT
from wave20261106_ov006_resource_slot_source_third_bindings import inputs

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
    m=Memory();specbase=0x2207e1c;tailbase=0x2207e70;primary=0x2219094;tail=0x221904c;specs=bytearray(image[specbase-base:specbase-base+51]);secondary=bytearray(image[tailbase-base:tailbase-base+18]);m.put(SCENE,bytes((i*17+case)&255 for i in range(136)));m.put(primary,bytes([0x65])*204);m.put(tail,bytes([0x76])*72)
    if case==1:specs[0]=128;specs[1]=0;secondary[1]=0
    if case==2:specs[6]=127;specs[7]=0;specs[8]=255
    m.put(specbase,specs);m.put(tailbase,secondary);initial=dict(m.data);events=[]
    def event(address,args=(),result=0x7bad0000,effects=(),checks=()):
        events.append(dict(address=address,args=tuple(word(v)for v in args),result=word(result),effects=[dict(address=hex(a),bytes=b.hex())for a,b in effects],checks=[dict(address=hex(a),bytes=b.hex())for a,b in checks]))
        for a,b in effects:m.put(a,b)
    event(0x20489f0,(1,));event(0x205fd80,(1,))
    for i in range(4):m.set32(CURSORS+16+i*4,32)
    m.set32(SCENE+0x7c,0)
    for address,args in[(0x2048f1c,(3,1)),(0x2048f2c,(2,1)),(0x2048f3c,(0,1)),(0x2046150,(1,0,1)),(0x2046150,(2,2,1))]:event(address,args)
    for i in range(4):event(0x2045680,(i,))
    for i in range(4):event(0x204607c,(i,))
    for i in[3,2,0]:
        buffer=0x3106000+i*0x100;event(0x2045560,(i,),buffer);event(0x2008c58,(0,buffer,32),effects=[(buffer,bytes(32))])
    asset=0x3108000;layout0=0x3109000+case*64;layout1=0xfffffff0 if case==5 else 0x34560000+case;out=STACK-36
    event(0x203cc2c,(0x220d378,1),asset);event(0x21e6e2c,(asset,));event(0x22076b4,(1,));event(0x204518c,(out,asset,1),out,effects=[(out,struct.pack('<2I',layout0,layout1))]);event(0x2045490,(1,layout0,0,layout1));m.set32(SCENE+0x7c,layout1);event(0x202a498,(1,asset),checks=[(CURSORS+20,struct.pack('<I',layout1))]);event(0x205ff80,(0x220d38c,))
    for i in range(17):
        p=specbase+i*3;record=primary+i*12;event(0x2008d78,(record,0,12),effects=[(record,bytes(12))]);tag,font,mode=m.get(p,3)
        if tag!=127:
            loaded=word(0xffffffe0+case+i*5);effects=[(record,struct.pack('<I',i+0x10203040))]
            if case>=3 and i==0:effects.extend([(p+1,b'\x00\x02'),(CURSORS+8,struct.pack('<I',0xfffffffd))])
            event(0x205ffcc,(record,word(signed8(tag)),font,mode,m.u32(CURSORS+font*16+mode*4)),loaded,effects=effects)
            font,mode=m.get(p+1,2);cell=CURSORS+font*16+mode*4;m.set32(cell,m.u32(cell)+loaded)
        else:
            m.put(record+8,bytes([tag]));m.put(record+10,bytes([font,mode]))
    for i in range(6):
        p=tailbase+i*3;tag,font,mode=m.get(p,3)
        if font==1:
            loaded=word(0xfffffff0+i*7+case);effects=[]
            if case==4 and i==0:effects=[(p+1,b'\x00\x01'),(CURSORS+4,struct.pack('<I',0xfffffffe))]
            event(0x2065730,(tail+i*12,word(signed8(tag)),font,mode,m.u32(CURSORS+font*16+mode*4)),loaded,effects=effects)
            font,mode=m.get(p+1,2);cell=CURSORS+font*16+mode*4;m.set32(cell,m.u32(cell)+loaded)
    event(0x205ff9c);event(0x21e7210,(0x220d3a0,4));answer=0x12340000+case;event(0x2048308,(),answer)
    regions=[(SCENE,136),(CURSORS,32),(primary,204),(tail,72),(specbase,51),(tailbase,18)]
    return dict(args=[],initial=initial,events=events,returnValue=answer,regions=regions,final=m.regions(regions))


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
    if negative:raise ValueError('Wrong C passed original field/branch/provider oracle')
    return dict(passed=True,records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeHelperInvocations=0,suppliedServiceCalls=sum(len(r[k]['trace'])for r in records for k in['original','compiled']),physicalAliasExplicit=dict(sceneBase='0x2218d90',cursorBase='0x2218df8',cursorWholeBytes=32,secondRowOffset=16,sceneWord7cEqualsCursorRow1Column1=True,storageCredit=0,portableGlobalDeclarationUnificationUnproved=True),limits='Only complete original/C676B callers execute. All layout/font/resource/clear callbacks are supplied with zero body or IO credit. Inputs cover signed tags,sentinel records,skipped secondary entries,post-callback cursor/metadata reloads,u32 wrapping,distinct17-/6-record collections,and the actual one-word helper6e2c boundary. One physical scene/cursor map is preserved; no storage,game,hardware,application reachability or nativeWindows proof.')
