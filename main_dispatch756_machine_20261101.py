import copy
import struct
import main_nodemix754_machine_20261101 as B
import main_nodemix754_models_20261101 as P
from unicorn.arm_const import *
ENTRY,SIZE,PRIVATE=0x0202F820,72,B.PRIVATE
TABLE,RETURN=0x020DD790,0x0202FB70

def profiles():
    profiles=[]
    original=P.profiles()
    for flags in[0,0x40,0x20,0x60,0xFFFFFFFF,0x80000000]:
        for option in range(0,256,32):
            p=copy.deepcopy(original[len(profiles)%len(original)]);p.update(name=f'dispatch-{len(profiles)}',flags=flags,option=option,opcode=9|option);profiles.append(p)
    return profiles

class Machine(B.Machine):
    def __init__(self,original,profile,body=None,private=False):
        super().__init__(original,profile)
        self.code=PRIVATE if private else ENTRY;self.extent=len(body)if body is not None else SIZE
        if body is not None:self.u.mem_write(self.code,body)
        self.u.mem_write(B.RS+8,struct.pack('<I',profile['flags']));self.u.mem_write(B.RS+0x10,bytes(4));self.u.mem_write(B.COMMAND+3+len(profile['entries'])*3,b'\x01')
        self.before=bytes(self.u.mem_read(B.BASE,0x800000));self.callback=None;self.callbackEntries=[];self.callbackReturns=[];self.nodes=[];self.node=None
    def write(self,u,access,address,size,value,data):
        if(address,size)==(B.RS+8,4):self.writes.append([u.reg_read(UC_ARM_REG_PC),address,size,value&0xFFFFFFFF]);return
        super().write(u,access,address,size,value,data)
    def observe(self,u,address,size,data):
        if self.callback is not None and address==self.callback['returnPc']:
            frame=self.callback;self.callback=None
            if u.reg_read(UC_ARM_REG_SP)!=frame['sp']or[u.reg_read(r)for r in B.REGS[4:12]]!=frame['saved']:raise ValueError('756 callback did not preserve dispatcher frame')
            self.callbackReturns.append(dict(entry=frame['entry'],returnPc=address,returnInstructionPc=self.lastPC,rawR0=u.reg_read(UC_ARM_REG_R0),actuallyReturned=True))
            if frame['entry']==B.ENTRY:
                self.node.update(after=bytes(u.mem_read(B.BASE,0x800000)),ioAfter=bytes(u.mem_read(B.IO,0x10000)),coreRegistersAndCpsr=[u.reg_read(r)for r in B.REGS+[UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR]],nativeCalls=self.calls[self.node['callStart']:],actualNativeReturnEvents=self.events[self.node['eventStart']:],nonstackWrites=self.writes[self.node['writeStart']:]);self.nodes.append(self.node);self.node=None
        if address in[B.ENTRY,RETURN]:
            if self.callback is not None:raise ValueError('756 unexpected nested command callback')
            words=[u.reg_read(r)for r in B.REGS[:4]];self.callbackEntries.append(dict(entry=address,preparedWords=words[:2],rawRegisterWords=words));self.callback=dict(entry=address,returnPc=u.reg_read(UC_ARM_REG_LR)&~1,sp=u.reg_read(UC_ARM_REG_SP),saved=[u.reg_read(r)for r in B.REGS[4:12]])
            if address==B.ENTRY:self.node=dict(profile=self.p,initialRegisters=[u.reg_read(r)for r in B.REGS],before=bytes(u.mem_read(B.BASE,0x800000)),ioBefore=bytes(u.mem_read(B.IO,0x10000)),callStart=len(self.calls),eventStart=len(self.events),writeStart=len(self.writes))
        if B.ENTRY<=address<B.ENTRY+B.SIZE or RETURN<=address<RETURN+40:
            code,extent=self.code,self.extent
            self.code,self.extent=(B.ENTRY,B.SIZE)if B.ENTRY<=address<B.ENTRY+B.SIZE else(RETURN,40)
            super().observe(u,address,size,data);self.code,self.extent=code,extent;return
        super().observe(u,address,size,data)
    def run(self,budget=200000):
        result=super().run(budget)
        if self.callback is not None or self.node is not None:raise ValueError('756 command callback did not finish')
        result.update(callbackEntries=self.callbackEntries,callbackReturns=self.callbackReturns,nodes=self.nodes,dispatcherObserved=[pc for pc in result['ownObserved']if self.code<=pc<self.code+self.extent]);return result

def model(result):
    p=result['profile'];entries=[dict(entry=row['entry'],preparedWords=row['preparedWords'])for row in result['callbackEntries']];expected=[dict(entry=B.ENTRY,preparedWords=[B.RS,p['option']])]
    initial=p['flags']&0xFFFFFFBF
    if initial&0x20==0:expected.append(dict(entry=RETURN,preparedWords=[B.RS,0]))
    if entries!=expected:raise ValueError(('756 actual callback arguments/order differ',entries,expected))
    if len(result['nodes'])!=1 or len(result['callbackReturns'])!=len(expected):raise ValueError('756 actual callback return count differs')
    node=P.model(result['nodes'][0]);actual=int.from_bytes(result['after'][B.RS-B.BASE+8:B.RS-B.BASE+12],'little');final=initial|0x20
    if actual!=final or result['coreRegistersAndCpsr'][0]!=final:raise ValueError('756 dispatcher final flags/rawR0 differ')
    beforeNode=result['nodes'][0]['before'];afterNode=result['nodes'][0]['after'];before=result['before'];after=result['after']
    lo,hi=B.STACK-65536-B.BASE,B.STACK+256-B.BASE
    for left,right in[(before,beforeNode),(afterNode,after)]:
        flag=B.RS-B.BASE+8
        if left[:flag]!=right[:flag]or left[flag+4:lo]!=right[flag+4:lo]or left[hi:]!=right[hi:]:raise ValueError('756 outer dispatcher changed unexpected RAM')
    if result['ioBefore']!=result['nodes'][0]['ioBefore']or result['ioAfter']!=result['nodes'][0]['ioAfter']:raise ValueError('756 dispatcher added unmodeled MMIO effects')
    flagWrites=[row[1:]for row in result['nonstackWrites']if row[1]==B.RS+8]
    expectedWrites=[[B.RS+8,4,initial]]if initial&0x20 else[[B.RS+8,4,initial],[B.RS+8,4,initial],[B.RS+8,4,final]]
    if flagWrites!=expectedWrites:raise ValueError(('756 dispatcher ordered flags differ',flagWrites,expectedWrites))
    return dict(node=node,callbackReturns=len(expected),callbackOptions=p['option'],finalFlags=final,actualNativeHelperReturnInstructions=node['actualNativeReturnInstructions'],completedNativeHelperEntries=node['completedNativeEntries'],allNativeNoProviders=True)
