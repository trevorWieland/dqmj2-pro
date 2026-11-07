import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from project import ROOT
from wave20261106_ov006_resource_slot_source_second_bindings import inputs

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
    m=Memory();selector=case;entry=ENTRY;link=LINK;resource=RESOURCE;specbase=0x2207e1c;specIndex=case%17;spec=specbase+specIndex*3
    domains=[(0,0,-1,-1),(0,0,-1,-1),(0,0,-1,-1),(0,0,-1,-1),(3,-2,7,-1),(-9,300,-1,5),(-2147483648,2147483647,2147483647,-1),(0,0,-1,0),(0,0,0,-1),(0,0,-2,-3),(32,0,128,255),(0,32,0,0)]
    dx,dy,width,height=domains[case];args=[selector,word(dx),word(dy),word(width),word(height)];events=[];m.put(ENTRY,bytes([0x61])*12);m.set32(ENTRY,0 if case==1 else LINK);m.set32(LINK+4,0 if case==2 else RESOURCE);m.put(RESOURCE,bytes([0x72])*128);m.put(RESOURCE+0x1c,bytes([128,255,255,128]));m.put(RESOURCE+0x7c,b'\xfe');mode=5 if case==5 else 3;m.put(spec,bytes([127,1,mode]));m.set32(INDEX+selector*4,specIndex);initial=dict(m.data)
    def event(address,args,result=0x7bad0000,effects=()):
        events.append(dict(address=address,args=tuple(word(v)for v in args),result=word(result),effects=[dict(address=hex(a),bytes=b.hex())for a,b in effects],checks=[]))
        for a,b in effects:m.put(a,b)
    event(0x2049ad0,(word(signed8(selector)),),0 if case==0 else ENTRY)
    answer=0 if case==0 else 1
    if case>=3:
        reset=dx==0 and dy==0 and width<0 and height<0
        if width<0:width=m.get(RESOURCE+0x1e,1)[0]
        if height<0:height=m.get(RESOURCE+0x1f,1)[0]
        if mode!=5:
            x,y=m.get(RESOURCE+0x1c,2);event(0x2045dc4,(1,mode,(x+dx)&255,(y+dy)&255,width&255,height&255),effects=[(RESOURCE+0x1c,b'\x7f\x80'),(RESOURCE+0x7c,b'\xfd'),(RESOURCE+0x1e,b'\x01\x02')])
        x,y=m.get(RESOURCE+0x1c,2);layer=m.get(RESOURCE+0x7c,1)[0];event(0x2045dc4,(1,layer,(x+dx)&255,(y+dy)&255,width&255,height&255))
        if reset:event(0x2049ffc,(RESOURCE,))
        else:event(0x204a010,(RESOURCE,word(dx<<3),word(dy<<3),word(width<<3),word(height<<3)))
        event(0x20850a0,(RESOURCE,))
    regions=[(ENTRY,12),(RESOURCE,128),(specbase,51),(INDEX,48)]
    return dict(args=args,initial=initial,events=events,returnValue=answer,regions=regions,final=m.regions(regions))


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
        for case in range(12):
            p=plan(row,case,images['ov006'],base);original=execute(row,native,p)
            try:compiled=execute(row,flat,p)
            except ValueError as error:
                if negative:return dict(rejected=True,address=row['address'],case=case,reason=str(error))
                raise
            records.append(dict(address=row['address'],case=case,original=original,compiled=compiled))
    if negative:raise ValueError('Wrong C passed original field/branch/provider oracle')
    return dict(passed=True,records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeHelperInvocations=0,suppliedServiceCalls=sum(len(r[k]['trace'])for r in records for k in['original','compiled']),physicalAliasExplicit=dict(entryRecordBytes=12,consumedEntryPrefixBytes=8,resourceViewIndependentOfSceneRoot=True,storageCredit=0),limits='Only the complete original/C336B caller executes; every draw/slot/resource callback is supplied with zero body credit. Cases cover null entry/link/resource, successful return1 despite null inner objects, metadata type5, both implicit extents versus explicit extents,byte wrap,signed32 scaling,and reloaded coordinates/layer after callback effects. Readonly metadata is not mutated. No resource/storage/game/hardware/nativeWindows execution credit.')
