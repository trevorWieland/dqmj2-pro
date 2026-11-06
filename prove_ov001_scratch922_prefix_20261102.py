import gzip
import hashlib
import json
import struct
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import match_runtime
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
import ov001_selector917_machine_20261102 as B
START=0x021FB214
CHECKPOINT=0x021FB248
MODE=0x020F69E8
WORD=0x020DD9BC

class Machine(B.Machine):
    def __init__(self,main,overlay,mode,argument):
        p=dict(ordinal=mode,phase=30,counter=0xED,gate=0xA7,seed=0x12345678,threshold=0,busy=0)
        super().__init__(main,overlay,None,p)
        self.argument=argument
        self.ranges.update({START:(1352,1),0x021FB1DC:(56,0),0x02008D78:(148,3),0x020443EC:(16,0),0x02044520:(28,0)})
        self.u.mem_write(MODE,bytes([mode]))
        self.originalWord=struct.unpack('<I',self.u.mem_read(WORD,4))[0]
        if self.originalWord!=1:raise ValueError('922 measured initialized word differs')
        self.u.mem_write(B.SCRATCH-1,bytes([0x5A]))
        self.u.mem_write(B.SCRATCH,bytes((i*37+mode+1)&255 for i in range(132)))
        self.u.mem_write(B.SCRATCH+132,bytes([0xA5]))

    def code(self,u,pc,size,unused):
        if pc==CHECKPOINT and self.entry==START and self.argument!=0:
            u.emu_stop()
            return
        super().code(u,pc,size,unused)

    def prefix(self):
        self.entry=START
        self.frames=[]
        self.entries=[]
        self.returns=[]
        self.writes=[]
        self.provided=[]
        self.pcs=set()
        self.steps=0
        self.previous=None
        self.privateStackStart=B.SP
        self.u.reg_write(UC_ARM_REG_CPSR,0xD3)
        for i,r in enumerate(B.REGS[:13]):self.u.reg_write(r,0x11110000+i*0x101)
        self.u.reg_write(B.REGS[0],self.argument)
        self.u.reg_write(B.REGS[13],B.SP)
        self.u.reg_write(B.REGS[14],B.STOP)
        self.topFrame=dict(entry=START,sp=B.SP,saved=[self.u.reg_read(r)for r in B.REGS[4:12]])
        self.u.emu_start(START,B.STOP+4,count=50000)
        expectedPc=CHECKPOINT if self.argument else B.STOP
        if self.u.reg_read(UC_ARM_REG_PC)!=expectedPc or self.frames:raise ValueError('922 prefix endpoint differs')
        before=self.u.mem_read(B.SCRATCH-1,1)[0]
        after=self.u.mem_read(B.SCRATCH+132,1)[0]
        scratch=bytes(self.u.mem_read(B.SCRATCH,132))
        expected=bytearray(132)
        if self.argument:expected[0x67]=1
        if scratch!=expected or before!=0x5A or after!=0xA5:raise ValueError('922 independent clear/gate/canary model differs')
        if self.provided:raise ValueError('922 unexpected supplied call')
        expectedR0=int(self.p['ordinal']in[3,7])if self.argument else 0
        if self.u.reg_read(B.REGS[0])!=expectedR0:raise ValueError('922 native mode predicate result differs')
        if self.argument and self.writes[-1]!=[B.SCRATCH+0x67,1,1]:raise ValueError('922 raw gate writer ordering differs')
        if any(not B.SCRATCH<=r[0]<B.SCRATCH+132 for r in self.writes):raise ValueError('922 unexpected nonstack writes')
        return dict(mode=self.p['ordinal'],argumentWord=self.argument,checkpointPc=hex(expectedPc),actualTopReturned=self.argument==0,unfinishedTopFrame=self.argument!=0,actualHelperPhysicalReturns=self.returns,nativeEntries=self.entries,writes=self.writes,scratchHex=scratch.hex(),nativeR0=self.u.reg_read(B.REGS[0]),stackPointer=hex(self.u.reg_read(B.REGS[13])),initializedMainWord=hex(self.originalWord),canaries=[before,after],steps=self.steps)


def execute():
    info,main,unused=measured_module('main')
    moduleInfo,overlay,unused=measured_module('ov001')
    rows=[]
    totals=dict(nonnullPrefixCheckpoints=0,actualNullTopReturns=0,actualNullGetterReturns=0,actualHelperPhysicalReturns=0,suppliedCalls=0)
    for mode in range(256):
        vm=Machine(main,overlay,mode,0x02540000)
        row=vm.prefix()
        rows.append(row)
        totals['nonnullPrefixCheckpoints']+=1
        totals['actualHelperPhysicalReturns']+=len(row['actualHelperPhysicalReturns'])
    vm=Machine(main,overlay,0,0)
    row=vm.prefix()
    getter=vm.run(B.GETTER)
    if getter['registers'][0]!=0 or getter['writes']:raise ValueError('922 getter after actual null return differs')
    row['actualGetterReturnWord']=getter['registers'][0]
    rows.append(row)
    totals['actualNullTopReturns']+=1
    totals['actualNullGetterReturns']+=1
    totals['actualHelperPhysicalReturns']+=len(row['actualHelperPhysicalReturns'])
    raw=json.dumps(rows,sort_keys=True,separators=(',',':')).encode()
    artifact=ROOT/'evidence/generated/ov001-scratch922-prefix-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,allPassed=True,sourceCredit=0,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',mode='arm',address=hex(START),nativeBytes=1352,moduleSha256=moduleInfo['sha256'],mainSha256=info['sha256'],totals=totals,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=hashlib.sha256(raw).hexdigest()),limits=['Only original prefix through PC021FB248 is executed for nonnull arguments;256 checkpoints are explicitly NOT top returns. Actor pointer is supplied and its first dereference at checkpoint is not executed.','Original02008D78 clears132 bytes at02239ABC; when incoming argument nonzero, actual021FB1DC/020443EC/02044520 complete before STRB one to scratch+0x67 at021FB244. Every other scratch byte remains zero at checkpoint, including+0x64/+0x66. Thus raw getter gate can be set before later fields are populated; this is not a completed-record or concurrency claim.','Mode raw u8[020F69C4+0x24] spans all256 values. The measured initialized main wordu32[020DD9BC] remains original1; no synthetic word9 rewrite. NativeFB1DC result is1 only for raw modes3/7 in this corpus, but gate write is unconditional for nonnull input.','Null input actually returns0 after the clear; actual subsequent021FBE70 getter returnsNULL. Getter is not invoked in an unfinished nonnull frame. Its prior all-byte behavior is separately frozen in912.','All real helper returns have opcode/SP/callee-saved checks, zero providers, exact clear/write ordering/bounds/canaries, and no original ROM/save file changes. Later constructor effects, RNG draws, record completion, ordinary caller/scene reachability and lifecycle remain unresolved.','This overlay001 scratch02239ABC is distinct from overlay000 birth scratch and saved-record byte33 evidence. Zero source/module/ROM completion or host/device claim.'])
    write_json(ROOT/'evidence/application/ov001-scratch922-prefix-20261102.json',report)
    print(totals,flush=True)

if __name__=='__main__':execute()
