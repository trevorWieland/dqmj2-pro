import hashlib
import json
import re
import sys
from project import ROOT,configuration,sha256,write_json
sys.path.insert(0,str(ROOT/'deps/native'))
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,ENTRY,SIZE,STACK,STOP=0x02000000,0x02026144,524,0x027F0000,0x027FF800
ABI=ROOT/'evidence/verification/main-nav562-signed-division-abi-20261101.json'
ABI_HASH='4d7b8fe5af8e3326e6bc012b049fe0a7636c11b0cff2cb6e13f1ac2dd128d5ff'
DIRECT_HASH='1c0cf1e5b668a8ed7521fa1d354e05b14a9dd11f62847250d6232b9ec4c6a1f9'
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def one(arm,numerator,denominator):
    u=Uc(UC_ARCH_ARM,UC_MODE_ARM);u.ctl_set_cpu_model(UC_CPU_ARM_946);u.mem_map(BASE,0x800000);u.mem_write(BASE,arm);u.reg_write(UC_ARM_REG_CPSR,0x10);initial=[0xA0570000+i*0x100 for i in range(13)]
    for reg,value in zip(REGS,initial):u.reg_write(reg,value)
    u.reg_write(UC_ARM_REG_R0,numerator&0xFFFFFFFF);u.reg_write(UC_ARM_REG_R1,denominator&0xFFFFFFFF);u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP);observed=[];writes=[]
    def observe(vm,address,length,data):
        if not ENTRY<=address<ENTRY+SIZE:raise ValueError(('570 unexpected PC',hex(address)))
        observed.append(address)
    def written(vm,access,address,size,value,data):
        if not STACK-65536<=address<STACK+4096:writes.append([address,size,value])
    u.hook_add(UC_HOOK_CODE,observe);u.hook_add(UC_HOOK_MEM_WRITE,written);u.emu_start(ENTRY,STOP,count=50000)
    if u.reg_read(UC_ARM_REG_PC)!=STOP or u.reg_read(UC_ARM_REG_SP)!=STACK or u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[u.reg_read(reg)for reg in REGS[4:12]]!=initial[4:12]or writes:raise ValueError('570 actual return/state differs')
    returned=[u.reg_read(reg)for reg in REGS[:4]];quotient=(abs(numerator)//abs(denominator))*(-1 if(numerator<0)!=(denominator<0)else 1)if denominator else numerator;remainder=numerator-quotient*denominator if denominator else 0
    if returned[:2]!=[quotient&0xFFFFFFFF,remainder&0xFFFFFFFF]:raise ValueError('570 independent quotient/remainder differs')
    return dict(numerator=numerator,denominator=denominator,returnedWords=returned,instructions=len(observed),actualReturned=True,callerHalfwordDomain=0<=numerator<=65535 and 0<=denominator<=65535)


def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('570 pinned runtime differs')
    if sha256(ABI)!=ABI_HASH:raise ValueError('570 exact frozen ABI JSON differs')
    abi=json.loads(ABI.read_text());armfile=ROOT/'extract/arm9/arm9.bin';symbols=ROOT/'config/arm9/symbols.txt';arm=armfile.read_bytes();span=arm[ENTRY-BASE:ENTRY-BASE+SIZE]
    if configuration()['romSha256']!=abi['romSha256']or sha256(armfile)!=abi['moduleSha256']or hashlib.sha256(span).hexdigest()!=abi['nativeSpanSha256']:raise ValueError('570 measured input identity differs')
    if re.search(r'^\S+ kind:function\(arm,size=0x20c\) addr:0x02026144$',symbols.read_text(),re.M)is None:raise ValueError('570 canonical ARM boundary differs')
    profiles=[(n,d)for n in[0,1,2,3,4,7,255,256,32767,32768,65534,65535]for d in[0,1,2,3,7,255,256,32767,32768,65535]]+[(-7,3),(7,-3),(-7,-3),(-1,3),(-2147483648,1),(-2147483648,-1),(-2147483648,3),(2147483647,-7),(-1,0)];cases=[one(arm,n,d)for n,d in profiles];digest=hashlib.sha256(encoded(cases)).hexdigest()
    if digest!=DIRECT_HASH:raise ValueError('570 frozen direct-native record digest differs')
    report=dict(schemaVersion=1,sourceCredit=0,processor='arm9',program='',module='main',mode='arm',address=hex(ENTRY),nativeBytes=SIZE,romSha256=abi['romSha256'],moduleSha256=abi['moduleSha256'],nativeSpanSha256=abi['nativeSpanSha256'],emulationModel='UC_CPU_ARM_946',frozenAbi=dict(path=ABI.relative_to(ROOT).as_posix(),sha256=ABI_HASH),actualOriginalReturns=len(cases),providedCalls=0,halfwordDomainCases=120,additionalSignedCases=9,zeroDenominatorCases=sum(d==0 for n,d in profiles),actualReturnStackModePreserved=True,nonstackWrites=0,directRecordsSha256=digest,directRecordsMatchFrozenNearPacketRecords=True,cases=cases,producer=dict(path='probe_main_division570_native_20261101.py',sha256=sha256(ROOT/'probe_main_division570_native_20261101.py')),limitations=['Finite native ABI observations; no reconstructed helper or caller source credit.','Physical denominator-zero and signed-overflow observations do not define abstract C division/remainder behavior.','Frozen ABI JSON historical report/trace references are not runtime dependencies; no 708-byte near draft, sweep or source is loaded.','No original public C return type or invented wide return is asserted.']);write_json(ROOT/'evidence/verification/main-division570-native-20261101.json',report);print(dict(actualOriginalReturns=len(cases),providedCalls=0,zeroDenominatorCases=report['zeroDenominatorCases'],frozenDirectRecordsMatch=True,sourceCredit=0),flush=True)


if __name__=='__main__':execute()
