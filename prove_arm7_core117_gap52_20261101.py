import gzip
import hashlib
import itertools
import json
import random
import struct
from pathlib import Path
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
from project import ROOT,sha256,write_json
MAIN=0x027e0000
WRAM=0x037f8000
ENTRY=0x037fb454
END=0x037fb488
TAIL=0x027ea62c
PORT=0x04808180
STACK=0x03030000
STOP=0x0f000000
WORK=ROOT/'work/arm7-bulk-20261030/core117-gap52'
REPORT=ROOT/'evidence/arm7/core117-gap52-native-20261101.json'


def cases():return [dict(background=b,busy=n)for b,n in itertools.product((0,1,255,256,0x1234,0x8000,65535,0xaa55,0x55aa),(0,1,2,7,127,10239,10240,None))]


def execute(case,index,tail=False,budget=80000):
    original_main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();original_wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);rng=random.Random(ENTRY*10000+index);regions={MAIN:original_main+bytes(0x20000-len(original_main)),WRAM:original_wram+bytes(0x18000-len(original_wram)),STACK:rng.randbytes(4096),0x04808000:rng.randbytes(4096),STOP:bytes(4096)}
    for base,raw in regions.items():cpu.mem_map(base,len(raw));cpu.mem_write(base,raw)
    command=(0,1,255,256,65535,65536,0xc008,0x12345678,0xffffffff)[index%9];mode=0x10|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,((index%16)<<28)|mode);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=command;initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    returned=False;writes=[];reads=[];supplied=[];visited=[];gap_seen=False;arm_modes=[]
    def instruction(machine,address,width,user):
        nonlocal returned,gap_seen
        if address==STOP:returned=True;machine.emu_stop();return
        if address==ENTRY:gap_seen=True
        if not(ENTRY<=address<ENTRY+48 or tail and TAIL<=address<TAIL+24)or address%4 or machine.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('Original gap/tail chain escaped exact ARM instruction bounds')
        visited.append(address);arm_modes.append(machine.reg_read(UC_ARM_REG_CPSR)&32)
    def write(machine,access,address,width,value,user):
        if not tail or address not in(0x0480817e,0x0480817c)or width!=2:raise ValueError('Original gap chain wrote outside measured command halfwords')
        writes.append([address,width,value&65535])
    def read(machine,access,address,width,value,user):
        reads.append([address,width])
        if address==PORT and width==2:
            busy=case['busy'];raw=(case['background']&~1)|(1 if busy is None or len(supplied)<busy else 0);supplied.append(raw);machine.mem_write(PORT,struct.pack('<H',raw))
        elif width==4 and address in([ENTRY+48]+([TAIL+24,TAIL+28]if tail else[])):pass
        else:raise ValueError('Original gap read escaped own pool/qualified tail literals/halfword port')
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.emu_start(TAIL if tail else ENTRY,STOP+4,count=budget)
    if not returned or not gap_seen:raise ValueError('Original complete gap chain did not actually return')
    busy=case['busy'];clear=busy is not None and busy<10240;count=busy+1 if clear else 10240;result=0 if clear else 1;expected_supply=[(case['background']&~1)|1]*(count-1)+[(case['background']&~1)if clear else(case['background']|1)];expected_io=bytearray(regions[0x04808000]);struct.pack_into('<H',expected_io,0x180,expected_supply[-1]);expected_writes=[]
    if tail:struct.pack_into('<HH',expected_io,0x17c,(command>>16)&65535,command&65535);expected_writes=[[0x0480817e,2,command&65535],[0x0480817c,2,(command>>16)&65535]]
    preserved=list(range(3,12))if tail else list(range(3,13));abi=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in preserved)and cpu.reg_read(REGISTERS[-2])==initial[-2]and cpu.reg_read(REGISTERS[-1])==initial[-1]and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode;checks=dict(abi=abi,result=cpu.reg_read(REGISTERS[0])==result,port=cpu.reg_read(REGISTERS[1])==PORT,counter=cpu.reg_read(REGISTERS[2])==(busy if clear else 10240),flags=cpu.reg_read(UC_ARM_REG_CPSR)>>28==(4 if clear else 6),writes=writes==expected_writes,supply=supplied==expected_supply,readCount=len(supplied)==count,main=bytes(cpu.mem_read(MAIN,len(regions[MAIN])))==regions[MAIN],wram=bytes(cpu.mem_read(WRAM,len(regions[WRAM])))==regions[WRAM],stack=bytes(cpu.mem_read(STACK,4096))==regions[STACK],io=bytes(cpu.mem_read(0x04808000,4096))==bytes(expected_io),tailTarget=not tail or cpu.reg_read(REGISTERS[12])==ENTRY)
    return dict(actualCompleteEntryReturn=True,directGap=not tail,tailEntry=tail,actualGapReturnObserved=True,rawResult=cpu.reg_read(REGISTERS[0]),readCount=len(supplied),capExhausted=not clear,modelPassed=all(checks.values()),modelChecks=checks,orderedWrites=writes,orderedReads=reads,suppliedHalfwords=supplied,rawRegisters=[cpu.reg_read(x)for x in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),visited=sorted(set(visited)),instructionCount=len(visited),stackSha256=sha256_bytes(cpu.mem_read(STACK,4096)),ioSha256=sha256_bytes(cpu.mem_read(0x04808000,4096)),providerReplacements=[],originalAssemblyAuthorshipProven=False,physicalHardwareTimingProven=False)


def sha256_bytes(raw):return hashlib.sha256(bytes(raw)).hexdigest()


def main():
    rom='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6';main=ROOT/'extract/arm7/runtime/arm7-main.bin';wram=ROOT/'extract/arm7/runtime/arm7-wram.bin'
    if sha256(ROOT/'inputs/game.nds')!=rom or sha256(main)!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'or sha256(wram)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Measured host ROM/runtime namespace differs')
    binary=wram.read_bytes();body=binary[ENTRY-WRAM:END-WRAM];main_body=main.read_bytes()[TAIL-MAIN:TAIL-MAIN+32]
    if struct.unpack_from('<I',body,48)[0]!=PORT or struct.unpack_from('<2I',main_body,24)!=(0x0480817e,ENTRY):raise ValueError('Exact gap pool or incoming ARM tail literal differs')
    inventory=json.loads((ROOT/'evidence/arm7/ghidra-runtime-inventory.json').read_text())['functions'];starts={int(x['address'],0)for x in inventory if x['module']=='arm7-wram'}
    if ENTRY in starts or ENTRY-52 not in starts or END not in starts:raise ValueError('Historical raw boundary gap/neighbors differ')
    records=[];visited=set();totals=dict(runs=0,directGapCompleteReturns=0,tailEntryCompleteReturns=0,gapObservedReturns=0,capExhaustedRuns=0)
    for tail in(False,True):
        for index,case in enumerate(cases()):
            value=execute(case,index,tail)
            if not value['modelPassed']:raise ValueError('Independent original gap/tail model differs')
            records.append(dict(case=case,tail=tail,execution=value));visited.update(value['visited']);totals['runs']+=1;totals['gapObservedReturns']+=1;totals['tailEntryCompleteReturns'if tail else'directGapCompleteReturns']+=1;totals['capExhaustedRuns']+=value['capExhausted']
    if not set(range(ENTRY,ENTRY+48,4)).issubset(visited):raise ValueError('Full gap instruction scope not executed')
    literal_refs=[];branch_refs=[]
    for module,path,base in [('arm7-main',main,MAIN),('arm7-wram',wram,WRAM)]:
        data=path.read_bytes()
        for off in range(0,len(data)-3,4):
            word=struct.unpack_from('<I',data,off)[0];pc=base+off
            if ENTRY<=word<END:literal_refs.append(dict(module=module,address=hex(pc),value=hex(word),exactEntry=word==ENTRY,evidenceClass='aligned literal candidate; only qualified A62C context proves ARM tail use'))
            if (word>>25)&7==5 and word>>28!=15:
                delta=(word&0xffffff)<<2
                if delta&0x2000000:delta-=0x4000000
                target=(pc+8+delta)&0xffffffff
                if ENTRY<=target<END:branch_refs.append(dict(module=module,address=hex(pc),target=hex(target),internal=ENTRY<=pc<END,evidenceClass='aligned ARM branch candidate; data false positives possible'))
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();WORK.mkdir(parents=True,exist_ok=True);trace=WORK/'records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=rom,processor='arm7',program='',module='arm7-wram',mode='arm',address=hex(ENTRY),bytes=52,codeBytes=48,literalBytes=4,initializedDenominatorDelta=0,sourceCredit=0,assemblySourceCredit=0,functionMatchedBytes=0,originalDataSourceCredit=0,sharedConfigOrInventoryEdited=False,moduleInputSha256=sha256(wram),spanSha256=sha256_bytes(body),rawInventorySha256=sha256(ROOT/'evidence/arm7/ghidra-runtime-inventory.json'),bounds=dict(start=hex(ENTRY),codeEnd=hex(ENTRY+48),pool=hex(ENTRY+48),end=hex(END),previousEntry='0x37fb420',nextEntry=hex(END)),qualifiedIncomingTail=dict(module='arm7-main',address=hex(TAIL),bytes=32,mode='arm',moduleSha256=sha256(main),spanSha256=sha256_bytes(main_body),target=hex(ENTRY),targetMode='arm',literalAddress=hex(TAIL+28),literalHash=sha256_bytes(main_body[28:32]),actualBxToEntryObserved=True),literalCandidates=literal_refs,alignedBranchCandidates=branch_refs,totals=totals,actualEntryExecutions=144,observedGapReturnsOverlapTailRunsNotAdditionalExecutions=True,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=sha256_bytes(raw),compressedSha256=sha256(trace),gzipMtime=0),limitations=['Original initialized gap evidence only; no source or ordinary assembly authorship credit','No global function-interior/reference completeness claim from bounded aligned scans','Raw inventories/configurations remain unchanged pending independent review','Synthetic per-read port inputs do not prove physical hardware timing or scene reachability']);write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),runs=totals['runs'],sourceCredit=0)),flush=True)
if __name__=='__main__':main()
