import gzip
import hashlib
import json
import struct
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import match_runtime
import unicorn
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB
from unicorn.arm_const import *
from project import ROOT,configuration,read_json,write_json,sha256
from link_runtime_unit import measured_module
import ov001_template349_fixture_20261031 as F
import ov001_template349_models_20261031 as G
import probe_ov000_birth329_20261031 as B
DISPATCH=0x021FBD6C
HANDLER=0x021FB7AC
WAIT=0x021F14E4
GETTER=0x021FBE70
STATE=0x02239A14
WAIT_OBJECT=0x02363000
UPPER={DISPATCH:260,HANDLER:296,WAIT:36,F.ENTRY:1352,GETTER:24}

class Machine(F.Machine):
    def __init__(self,*args):
        self.previousInstruction=None
        self.upperPhysical=[]
        self.stackFloor=B.STACK
        super().__init__(*args)

    def write(self,u,access,address,size,value,data):
        if size==1 and address in [STATE+1,STATE+0xA]:
            self.writes.append([hex(address),size,value&255])
            return
        super().write(u,access,address,size,value,data)

    def close_returns(self,u,address):
        start=len(self.returned)
        closing=list(self.frames)
        super().close_returns(u,address)
        completed=self.returned[start:]
        for record,frame in zip(completed,reversed(closing)):
            entry=int(record['entry'],0)
            if entry not in UPPER:continue
            if self.previousInstruction is None:raise ValueError('928 prior return instruction absent')
            pc,size,thumb=self.previousInstruction
            decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB if thumb else CS_MODE_ARM)
            instruction=next(decoder.disasm(bytes(u.mem_read(pc,size)),pc))
            proper=instruction.mnemonic.startswith('pop')and'pc'in instruction.op_str or instruction.mnemonic.startswith('bx')and instruction.op_str=='lr' or instruction.mnemonic.startswith('ldm')and'pc'in instruction.op_str
            if not entry<=pc<entry+UPPER[entry]or not proper:raise ValueError(('928 upper actual return opcode',hex(entry),hex(pc),instruction.mnemonic,instruction.op_str))
            self.upperPhysical.append(dict(entry=hex(entry),returnInstructionPc=hex(pc),returnInstruction=instruction.mnemonic+' '+instruction.op_str,rawR0=u.reg_read(UC_ARM_REG_R0)))

    def observe(self,u,address,size,data):
        super().observe(u,address,size,data)
        if address in UPPER and address!=F.ENTRY:
            self.trace.append(dict(entry=hex(address),arguments=[u.reg_read(r)for r in B.REGS[:4]],sp=hex(u.reg_read(UC_ARM_REG_SP))))
            self.frames.append(dict(entry=address,returnAddress=u.reg_read(UC_ARM_REG_LR)&~1,returnThumb=bool(u.reg_read(UC_ARM_REG_LR)&1),sp=u.reg_read(UC_ARM_REG_SP),preserved=[u.reg_read(r)for r in B.REGS[4:12]]))
        self.stackFloor=min(self.stackFloor,u.reg_read(UC_ARM_REG_SP))
        self.previousInstruction=(address,size,bool(u.reg_read(UC_ARM_REG_CPSR)&0x20))

    def invoke(self,entry):
        self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        values=[0xAB450000+i*0x100 for i in range(len(B.REGS))]
        for r,v in zip(B.REGS,values):self.u.reg_write(r,v)
        self.u.reg_write(UC_ARM_REG_SP,B.STACK)
        self.u.reg_write(UC_ARM_REG_LR,B.STOP)
        self.steps=0
        self.frames=[]
        self.returned=[]
        self.trace=[]
        self.writes=[]
        self.upperPhysical=[]
        self.previousInstruction=None
        self.u.emu_start(entry,B.STOP,count=200000)
        self.close_returns(self.u,self.u.reg_read(UC_ARM_REG_PC))
        if self.frames or self.u.reg_read(UC_ARM_REG_PC)!=B.STOP or self.u.reg_read(UC_ARM_REG_SP)!=B.STACK or self.u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or[self.u.reg_read(r)for r in B.REGS[4:12]]!=values[4:12]:raise ValueError('928 actual top return/frame differs')
        return dict(actualTopReturns=1,entry=hex(entry),rawR0=self.u.reg_read(UC_ARM_REG_R0),upperPhysicalReturns=list(self.upperPhysical),legacySelectedFrameCompletions=len(self.returned),nativeEntries=list(self.trace),writes=list(self.writes),steps=self.steps,measuredStackFloor=hex(self.stackFloor))


def compare_ram(vm,expected):
    after=bytes(vm.u.mem_read(0x02000000,0x800000))
    lo=vm.stackFloor-0x02000000
    hi=B.STACK-0x02000000
    if after[:lo]!=expected[:lo]or after[hi:]!=expected[hi:]:
        bad=next(i for i,(x,y)in enumerate(zip(after,expected))if x!=y and not lo<=i<hi)
        raise ValueError(('928 independent complete observable RAM model differs',hex(0x02000000+bad),after[bad],expected[bad]))
    return hashlib.sha256(after[:lo]+after[hi:]).hexdigest()


def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('928 pinned runtime differs')
    for row in read_json(ROOT/'evidence/verification/ov001-constructor928-inputs-20261102.json')['files']:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError(('928 input differs',row['path']))
    main,save,assets=B.inputs()
    info,overlay,unused=measured_module('ov001')
    mainInfo=measured_module('main')[0]
    rows=[]
    totals=dict(scenarios=0,actualDispatcherTopReturns=0,actualGetterTopReturns=0,actualTopReturns=0,actualNestedUpperPhysicalReturns=0,actualConstructorsReturned=0,legacySelectedFrameCompletions=0,suppliedCalls=0,rngEntries=0)
    for recipe in G.recipes(assets):
        for busy in [0,2]:
            vm=Machine(main,save,assets,overlay,recipe['seed'])
            actor,parameter=G.setup(vm,recipe)
            vm.captureOriginal=True
            vm.u.mem_write(B.STACK-0x10000,bytes(0x11000))
            vm.u.mem_write(STATE+1,bytes([95]))
            vm.u.mem_write(STATE+0xA,bytes([13]))
            vm.word(STATE+0x40,0 if recipe['null']else G.ACTOR)
            vm.word(0x02238F5C,WAIT_OBJECT)
            vm.word(WAIT_OBJECT+0x18,busy)
            before=bytes(vm.u.mem_read(0x02000000,0x800000))
            expected=bytearray(before)
            template=before[G.TEMPLATE-0x02000000:G.TEMPLATE-0x02000000+132]
            if busy==0:
                full,template=G.model(before,recipe,actor,parameter,assets)
                expected=bytearray(full)
                expected[STATE+1-0x02000000]=110
            first=vm.invoke(DISPATCH)
            firstHash=compare_ram(vm,expected)
            if first['rawR0']!=0:raise ValueError('928 first dispatcher return differs')
            constructors=[r for r in first['upperPhysicalReturns']if r['entry']==hex(F.ENTRY)]
            if len(constructors)!=(1 if busy==0 else 0):raise ValueError('928 actual constructor return count differs')
            if constructors and constructors[0]['rawR0']!=(0 if recipe['null']else 1):raise ValueError('928 actual constructor result differs')
            if busy==0:
                expected[STATE+1-0x02000000]=0
                expected[STATE+0xA-0x02000000]=15
            second=vm.invoke(DISPATCH)
            secondHash=compare_ram(vm,expected)
            if second['rawR0']!=0:raise ValueError('928 second dispatcher return differs')
            getter=vm.invoke(GETTER)
            getterHash=compare_ram(vm,expected)
            expectedPointer=G.TEMPLATE if template[0x67]else 0
            if getter['rawR0']!=expectedPointer:raise ValueError('928 getter condition differs')
            if vm.providers:raise ValueError('928 unexpected function providers')
            if vm.divisions:raise ValueError('928 unexpected hardware division read')
            for result in [first,second,getter]:
                totals['legacySelectedFrameCompletions']+=result['legacySelectedFrameCompletions']
                totals['actualNestedUpperPhysicalReturns']+=sum(r['entry']not in[hex(DISPATCH),hex(GETTER)]for r in result['upperPhysicalReturns'])
                totals['rngEntries']+=sum(r['entry']=='0x203d294'for r in result['nativeEntries'])
            if totals['rngEntries']:raise ValueError('928 unexpected scoped RNG entry')
            totals['scenarios']+=1
            totals['actualTopReturns']+=3
            totals['actualDispatcherTopReturns']+=2
            totals['actualGetterTopReturns']+=1
            totals['actualConstructorsReturned']+=len(constructors)
            rows.append(dict(recipe=recipe,waitFlagsWord=busy,first=first,second=second,getter=getter,expectedTemplateHex=template.hex(),actualTemplateHex=bytes(vm.u.mem_read(G.TEMPLATE,132)).hex(),originalConstructorObservedCodeBytes=sorted(vm.observed),hardwareDivisionReadEvents=len(vm.divisions),observableRamHashes=[firstHash,secondHash,getterHash],allPassed=True))
    raw=json.dumps(rows,sort_keys=True,separators=(',',':')).encode()
    artifact=ROOT/'evidence/generated/ov001-constructor928-chain-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,allPassed=True,sourceCredit=0,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',mode='arm',moduleSha256=info['sha256'],mainSha256=mainInfo['sha256'],totals=totals,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=hashlib.sha256(raw).hexdigest()),limits=['Actual original dispatcher selector13 invokes actual296-bytehandler at supplied timer95. Actual36-byte wait helper reads a supplied object flag word; if bit2 clear, original1352-byte FB214 executes to a proper return. No function providers and no source or opcode substitutions.','Frozen349 recipes supply raw modes3/7, copied actor/parameter data, measured EnmyKindTbl mapping, skill/stat/ancestry/flag inputs and old-bit histories. Entire132-byte template and nonstack flags are independently modeled; no normal-scene or loaded-asset membership claim.','Second original dispatcher call occurs on unchanged resulting RAM: after completed constructor it clears timer110 and writes selector15; busy paths remain95. Getter is then separately invoked by the driver. Null actor follows actual clear/return0, which the handler ignores before advancing; no bug or scene-validity inference.','Top returns360 and nested upper physical returns are separate counts. Upper includes handler/wait/constructor actual return opcodes within measured spans. Legacy inherited selected-frame completions are reported separately and are NOT reclassified as physical returns or added to top counts.','All observable8MiB RAM outside only the measured across-call private-stack union agrees with an independent model after every call. Busy paths preserve the supplied random scratch bytes: nonzero getter gate there is only a provided input, not proof that a constructor ran.','No RNG entry or inherited modeled hardware-division read occurs in these scoped raw modes. No current/future RNG, complete ordinary scene, persistence, acquisition meaning, game bug, source/module/ROM completion, host/device or application edit claim.'])
    write_json(ROOT/'evidence/application/ov001-constructor928-native-chain-20261102.json',report)
    print(totals,flush=True)

if __name__=='__main__':execute()
