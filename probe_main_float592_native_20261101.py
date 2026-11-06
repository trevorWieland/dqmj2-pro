import json
import gzip
import math
import struct
import sys
import match_runtime as c
import unicorn
from project import ROOT,write_json,configuration,sha256
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,STACK,STOP=0x02000000,0x027F0000,0x027FF800
U32FLOAT,DIVFLOAT,MULFLOAT,WIDEN,CEIL,TRUNC=0x02025A70,0x02025578,0x02025AB8,0x02025930,0x02022480,0x02024394
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def f32(value):return struct.unpack('<f',struct.pack('<f',value))[0]
def fw(value):return struct.unpack('<I',struct.pack('<f',value))[0]
def dw(value):return list(struct.unpack('<2I',struct.pack('<d',value)))


class Machine:
    def __init__(self,arm,case):
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM);self.u.ctl_set_cpu_model(UC_CPU_ARM_946);self.u.mem_map(BASE,0x800000);self.u.mem_write(BASE,arm);self.armLength=len(arm);self.case=case;self.seen=set();self.calls=[];self.instructions=0;self.u.hook_add(UC_HOOK_CODE,self.code);self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)
    def code(self,u,address,length,data):
        if not BASE<=address<BASE+self.armLength:raise ValueError(('592 PC outside measured initialized main',hex(address)))
        self.seen.add(address);self.instructions+=1
    def write(self,u,access,address,size,value,data):
        if not STACK-65536<=address<STACK+256:raise ValueError(('592 unexpected nonstack effect',hex(address)))
    def call(self,address,words):
        self.u.mem_write(STACK-65536,bytes(65536+256));initial=[(0xA5920000+(i<<8)+self.case)&0xFFFFFFFF for i in range(13)];self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        for reg,value in zip(REGS,initial):self.u.reg_write(reg,value)
        for reg,value in zip(REGS,words):self.u.reg_write(reg,value&0xFFFFFFFF)
        self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP);before=self.instructions;self.u.emu_start(address,STOP,count=100000)
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[self.u.reg_read(reg)for reg in REGS[4:12]]!=initial[4:12]:raise ValueError('592 actual native return differs')
        result=[self.u.reg_read(reg)for reg in REGS[:4]];self.calls.append(dict(entry=hex(address),preparedWords=[w&0xFFFFFFFF for w in words],returnedWords=result,instructions=self.instructions-before,actualReturned=True));return result


def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('592 runtime differs')
    module,arm,symbols=measured_module('main')
    if module['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':raise ValueError('592 main differs')
    functions=[]
    for address in[U32FLOAT,DIVFLOAT,MULFLOAT,WIDEN,CEIL,TRUNC]:
        line=next(line for line in symbols.splitlines()if'addr:0x%08x'%address in line.lower());functions.append(dict(address=hex(address),canonicalSymbolLine=line))
    direct=[];chains=[];observed=set();values=set(range(256))
    for bit in range(32):values.update(v for v in[(1<<bit)-1,1<<bit,(1<<bit)+1]if v<=0xFFFFFFFF)
    values.add(0xFFFFFFFF)
    for index,value in enumerate(sorted(values)):
        m=Machine(arm,index);result=m.call(U32FLOAT,[value]);expected=fw(float(value))
        if result[0]!=expected:raise ValueError(('592 unsigned conversion differs',value))
        direct.append(dict(inputWord=value,expectedF32Word=expected,calls=m.calls));observed.update(m.seen)
    for count in[3,4,5]:
        for byte in range(256):
            index=len(chains);m=Machine(arm,index);cf=m.call(U32FLOAT,[count])[0];bf=m.call(U32FLOAT,[byte])[0]
            if cf!=fw(float(count))or bf!=fw(float(byte)):raise ValueError('592 positive conversion differs')
            ratio=m.call(DIVFLOAT,[cf,fw(5.0)])[0];ratioValue=f32(count/5.0)
            if ratio!=fw(ratioValue):raise ValueError('592 finite float division differs')
            product=m.call(MULFLOAT,[bf,ratio])[0];productValue=f32(f32(float(byte))*ratioValue)
            if product!=fw(productValue):raise ValueError('592 finite float product differs')
            wide=m.call(WIDEN,[product])[:2]
            if wide!=dw(productValue):raise ValueError('592 float widening differs')
            rounded=m.call(CEIL,wide)[:2];expected=float(math.ceil(productValue))
            if rounded!=dw(expected):raise ValueError('592 finite positive ceiling differs')
            integral=m.call(TRUNC,rounded)[0]
            if integral!=int(expected):raise ValueError('592 finite signed conversion differs')
            chains.append(dict(count=count,inputByte=byte,ratioWord=ratio,productWord=product,expectedIntegral=int(expected),calls=m.calls));observed.update(m.seen)
        print(dict(count=count,completedChains=len(chains)),flush=True)
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=module['sha256'],mode='arm',emulationModel='UC_CPU_ARM_946',sourceCredit=0,providedCalls=0,functions=functions,directUnsignedToFloatCases=len(direct),finiteRowChains=len(chains),actualTopReturns=len(direct)+7*len(chains),nestedHelperReturnsNotCounted=True,nonstackWrites=0,nonStackMemoryEffects='No native nonstack write is allowed; code/data image remains measured and unchanged',observedAddresses=sorted(observed),directUnsignedConversion=direct,chainCases=chains,physicalContracts=[dict(entry=hex(U32FLOAT),view='R0 unsigned32 to IEEE binary32 in R0',qualifiedDomain='Listed328 unsigned values including high-bit and rounding boundaries'),dict(entry=hex(DIVFLOAT),view='Binary32 R0 / binary32 R1, binary32 R0 result',qualifiedDomain='Positive count3/4/5 divided by5.0'),dict(entry=hex(MULFLOAT),view='Binary32 R0 * binary32 R1, binary32 R0 result',qualifiedDomain='Byte0..255 times the measured count/5.0 result'),dict(entry=hex(WIDEN),view='Binary32 R0 to exact binary64 R0-low/R1-high',qualifiedDomain='Listed nonnegative finite products'),dict(entry=hex(CEIL),view='Binary64 R0-low/R1-high to binary64 R0-low/R1-high',qualifiedDomain='Listed nonnegative finite products agree with mathematical ceiling'),dict(entry=hex(TRUNC),view='Binary64 R0-low/R1-high to signed32 R0',qualifiedDomain='Listed integral results0..255; R1 remains scratch')],limits=['Direct original-native finite contracts only; no selected-C source qualification, public prototype or source credit.','The seven-stage sequence is synthetic and derived from static caller word flow; it is not an execution of the ordinary overlay caller.','Soft-float NaNs,infinities,negative float arithmetic,overflow and unsupported conversion domains are not generalized.','High incoming unused register words are poisoned and each call has fresh stack/register state; no inherited R2/R3 input is assumed.','The measured main image is mapped privately; no file,scene,RNG,asset or current-game-state claim.'])
    report['physicalContracts'][0]['qualifiedDomain']=f'Listed {len(direct)} unsigned values including high-bit and rounding boundaries';encoded=lambda value:json.dumps(value,sort_keys=True,separators=(',',':')).encode();raw=encoded(dict(directUnsignedConversion=direct,chainCases=chains));artifact=ROOT/'evidence/generated/main-float592-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0));report['generatedTrace']=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw));report['directUnsignedConversion']=[dict(inputWord=r['inputWord'],expectedF32Word=r['expectedF32Word'],actualTopReturns=1,traceSha256=c.sha(encoded(r)))for r in direct];report['chainCases']=[dict(count=r['count'],inputByte=r['inputByte'],ratioWord=r['ratioWord'],productWord=r['productWord'],expectedIntegral=r['expectedIntegral'],actualTopReturns=7,traceSha256=c.sha(encoded(r)))for r in chains];write_json(ROOT/'evidence/abi/main-float592-row-parameter-chain-20261101.json',report);print(dict(direct=len(direct),chains=len(chains),actualTopReturns=report['actualTopReturns'],providers=0,sourceCredit=0),flush=True)


if __name__=='__main__':execute()
