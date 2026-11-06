import match_runtime
import copy
import hashlib
import json
import os
import re
import struct
import subprocess
from project import ROOT,read_json,write_json,sha256
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from elftools.elf.elffile import ELFFile

LANE=ROOT/'evidence/lanes/parallel-wave20261106/gp-randomchar-interface-repair-scout'
WORK=ROOT/'work/w6rr'
OLD='evidence/lanes/parallel-wave20261106/gp-core-resume-next/first'
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
BASE=0x02000000
END=0x04000000


def native_call(image,address,size,n,d=None,state=None):
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(BASE,0x400000);uc.mem_write(BASE,image);uc.mem_map(0x03000000,0x10000);uc.mem_map(END,0x1000);initial=[0x11220000+i*0x1001 for i in range(13)]
    for r,v in zip(REGS,initial):uc.reg_write(r,v)
    uc.reg_write(UC_ARM_REG_SP,0x0300f000);uc.reg_write(UC_ARM_REG_LR,END);uc.reg_write(UC_ARM_REG_R0,n&0xffffffff)
    if d is not None:uc.reg_write(UC_ARM_REG_R1,d&0xffffffff)
    if state is not None:uc.mem_write(state[0],struct.pack('<I',state[1]))
    returned=False;observed=set()
    def hook(machine,pc,amount,data):
        nonlocal returned
        if pc==END:returned=True;machine.emu_stop();return
        if not address<=pc<address+size:raise ValueError('Actual arithmetic/RNG execution escaped complete native body')
        observed.add(pc)
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(address,END+4,count=20000)
    if not returned or uc.reg_read(UC_ARM_REG_SP)!=0x0300f000 or[uc.reg_read(r)for r in REGS[4:12]]!=initial[4:12]:raise ValueError('Actual native arithmetic/RNG return/callee-save contract differs')
    return dict(r0=uc.reg_read(UC_ARM_REG_R0),r1=uc.reg_read(UC_ARM_REG_R1),state=None if state is None else struct.unpack('<I',uc.mem_read(state[0],4))[0],instructionAddresses=sorted(observed))


def main():
    if LANE.resolve()!=(ROOT/'evidence/lanes/parallel-wave20261106/gp-randomchar-interface-repair-scout').resolve()or WORK.resolve()!=(ROOT/'work/w6rr').resolve():raise ValueError('Exact new private repair paths differ')
    if (WORK/"corrected.o").exists()or(WORK/"match.c").exists():raise ValueError('One bounded copied-source correction trial only; private work already exists')
    LANE.mkdir(parents=True,exist_ok=True);WORK.mkdir(parents=True,exist_ok=True);old=ROOT/OLD;manifest=read_json(old/'inputs.json');before={p['path']:sha256(ROOT/p['path'])for p in manifest['files']};old_entry=next(e for e in read_json(old/'match.json')['matches']if int(e['address'],0)==0x020aced4);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text(encoding='utf-8');primary='deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gpi-connect/GP/gpiConnect.c';text=(ROOT/primary).read_text(encoding='utf-8');literal=re.search(r'^#define RANDSTRING\s+("[^"\n]+")',text,re.M)[1];alphabet=json.loads(literal).encode()+b'\0'
    if len(alphabet)!=63 or image[0xe0890:0xe0890+63]!=alphabet:raise ValueError('Actual full63-byte original primary alphabet/NUL differs')
    native_specs=[]
    for address,size in[(0x02026144,524),(0x02026350,484),(0x0201d5d4,52)]:
        line=next((s for s in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(size,address),s)),None)
        if line is None:raise ValueError('Actual full native helper canonical ARM entry/extent differs')
        native_specs.append(dict(address=hex(address),bytes=size,mode='arm',nativeSha256=hashlib.sha256(image[address-BASE:address-BASE+size]).hexdigest(),canonicalInventoryRecord=line,sourceCredit=0))
    numerators=[0,1,61,62,63,0x7fffffff,0x80000000,0xffffffff];denominators=[1,2,3,62,255,0x8000,0x7fffffff,0x80000000,0xffffffff];unsigned=[];signed=[];distinguishing=[]
    for n in numerators:
        for d in denominators:
            value=native_call(image,0x02026350,484,n,d)
            if(value['r0'],value['r1'])!=(n//d,n%d):raise ValueError('Unsigned native div/rem ABI differs')
            unsigned.append(dict(numerator=hex(n),denominator=hex(d),quotient=value['r0'],remainder=value['r1']))
            sn=n if n<0x80000000 else n-0x100000000;sd=d if d<0x80000000 else d-0x100000000
            if sn==-0x80000000 and sd==-1:continue
            q=abs(sn)//abs(sd)*(-1 if(sn<0)!=(sd<0)else 1);rem=sn-q*sd;sv=native_call(image,0x02026144,524,n,d)
            if(sv['r0'],sv['r1'])!=(q&0xffffffff,rem&0xffffffff):raise ValueError('Signed native div/rem ABI differs')
            signed.append(dict(numerator=sn,denominator=sd,quotient=q,remainder=rem))
            if(value['r0'],value['r1'])!=(sv['r0'],sv['r1']):distinguishing.append(dict(numerator=hex(n),denominator=hex(d),unsignedResult=[value['r0'],value['r1']],signedResult=[sv['r0'],sv['r1']]))
    state_addr,multiplier,mask=struct.unpack_from('<III',image,0x1d5fc);seeds=[0,1,0xffffffff,*[1<<i for i in range(32)]];seed=0x73b19da5
    for i in range(128):seed=(seed*1664525+1013904223)&0xffffffff;seeds.append(seed)
    rand=[]
    if multiplier!=1103515245 or mask!=0x7fff or image[0x1d5e8:0x1d5f8].hex()!='390080e2030a80e2000082e5200801e0':raise ValueError('Actual rand multiplier/increment/mask instruction witness differs')
    for seed in seeds:
        expected=(seed*multiplier+12345)&0xffffffff;v=native_call(image,0x0201d5d4,52,0,state=(state_addr,seed))
        if v['state']!=expected or v['r0']!=(expected>>16)&0x7fff:raise ValueError('Actual rand full-state/output contract differs')
        rand.append(dict(seed=hex(seed),nextState=hex(expected),result=v['r0']))
    source=WORK/'match.c';source.write_bytes((ROOT/old_entry['source']).read_bytes());context_root=(ROOT/old_entry['source']).parent
    for path in context_root.glob('*.h'):(WORK/path.name).write_bytes(path.read_bytes())
    context=WORK/'context.h';original=context.read_text(encoding='utf-8');corrected=original.replace('extern const char native_data_020e0890[];','extern const char native_data_020e0890[63];').replace('#define RANDOMCHAR() (RANDSTRING[rand()%62])','#define RANDOMCHAR() (RANDSTRING[rand() % (sizeof(RANDSTRING) - 1)])')
    if corrected==original or'RANDSTRING[rand()%62]'in corrected:raise ValueError('Only actual primary unsigned sizeof correction permitted')
    context.write_text(corrected,encoding='utf-8');compiler=ROOT/old_entry['compiler'];obj=WORK/'corrected.o';argv=[str(compiler),*old_entry['compilerFlags'],'-c',str(source),'-o',str(obj)];process=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')));(LANE/'compile.log').write_text(process.stdout+process.stderr,encoding='utf-8')
    if process.returncode:raise ValueError('Single genuine unsigned-sizeof correction did not compile')
    with obj.open('rb')as stream:
        elf=ELFFile(stream);table=elf.get_section_by_name('.symtab');symbol=next(s for s in table.iter_symbols()if s.name==old_entry['name']);section=elf.get_section(symbol['st_shndx']);start=symbol['st_value']&~1;body=section.data()[start:start+symbol['st_size']];relocations=[]
        for s in elf.iter_sections():
            if s['sh_type']not in['SHT_REL','SHT_RELA']or s['sh_info']!=symbol['st_shndx']:continue
            syms=elf.get_section(s['sh_link'])
            for rel in s.iter_relocations():
                if start<=rel['r_offset']<start+symbol['st_size']:relocations.append(dict(offset=rel['r_offset']-start,type=rel['r_info_type'],symbol=syms.get_symbol(rel['r_info_sym']).name))
        full_symbol=dict(name=symbol.name,type=symbol['st_info']['type'],bytes=symbol['st_size'],sectionIndex=symbol['st_shndx'],sectionName=section.name,sectionType=section['sh_type'],sectionFlags=section['sh_flags'],sectionOffset=start,thumbMapping=any(s.name=='$t'and s['st_shndx']==symbol['st_shndx']and s['st_value']==start for s in table.iter_symbols()))
    if full_symbol['type']!='STT_FUNC'or len(body)!=44 or not full_symbol['thumbMapping']or not any(r['symbol']=='_u32_div_f'and r['offset']==20 and r['type']==10 for r in relocations)or any(r['symbol']=='_s32_div_f'for r in relocations):raise ValueError('Actual corrected whole44 C symbol/unsigned helper relocation differs')
    row=copy.deepcopy(old_entry);row.update(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),sourceDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in sorted(WORK.glob('*.h'))],object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),sectionIndex=full_symbol['sectionIndex'],sectionOffset=start,compiledBytes=44)
    row['relocations']=[dict(r,target={14:'0x201d5d4',20:'0x2026350',40:'0x20e0890'}[r['offset']],addend=0 if r['type']==2 else-4,binding='independently-proven-canonical-native-ABI')for r in relocations]
    from recover_linked_runtime import qualified_bindings
    from link_runtime_unit import validate
    bindings=qualified_bindings(row);link=validate(row,bindings,WORK/'link');native=image[0xaced4:0xaced4+44]
    if not link['exactCallerBytes']or(WORK/'link/caller.bin').read_bytes()!=native:raise ValueError('Corrected unsigned C failed whole genuine native44 link')
    after={p:sha256(ROOT/p)for p in before}
    if before!=after:raise ValueError('Frozen original GP packet inputs changed')
    result=dict(status='passed-single-private-typed-correction-feasibility',sourceCredit=0,sharedOrFrozenWrites=False,oldInputsRehashed=len(before),oldInputsChanged=[],primary=dict(path=primary,sha256=sha256(ROOT/primary),macro=re.search(r'^#define RANDOMCHAR\(\).*',text,re.M)[0],alphabetLiteral=literal,alphabetWithNulBytes=63,sizeofUnsignedSemantics=True),nativeSpecs=native_specs,unsignedHelper=dict(address='0x2026350',bytes=484,actualReturningCases=len(unsigned),quotientRegister='R0',remainderRegister='R1',vectors=unsigned),signedHelper=dict(address='0x2026144',bytes=524,actualReturningCases=len(signed),quotientRegister='R0',remainderRegister='R1',vectors=signed),signedUnsignedDistinguishingCases=distinguishing,nativeRand=dict(address='0x201d5d4',bytes=52,stateAddress=hex(state_addr),multiplier=multiplier,increment=12345,mask=hex(mask),actualReturningCases=len(rand),allPossibleOutputsDomain=[0,32767],domainProof='Exact final AND with0x7fff proves sign bit zero for every32-bit seed;actual full-body state/output vectors verify instruction-derived LCG model',vectors=rand),correction=dict(source=row['source'],sourceSha256=row['sourceSha256'],context=context.relative_to(ROOT).as_posix(),contextSha256=sha256(context),onlyChanges=['Real complete63-byte alphabet declaration including NUL','Original primary sizeof(RANDSTRING)-1 unsigned divisor expression'],compiler=old_entry['compiler'],compilerSha256=sha256(compiler),compilerFlags=old_entry['compilerFlags'],argv=argv,exitCode=0,object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualSymbol=full_symbol,actualRelocations=relocations,originalObjectCodeBeforeRelocationSha256=hashlib.sha256(body).hexdigest(),genuineLink=link,nativeSymbolEntries=bindings,exactNativeCallerBytes=True),riskExplanation='Within actual rand0..32767 and divisor62,signed/unsigned remainder agree;old bounded caller execution could not reveal the compiler-helper nominal/ABI mismatch. Primary sizeof unsignedness selects the correct_u32_div_f symbol without any core alias change.',repairProposal='Root may admit a separate replacement for this one44-byte identity using genuine sized alphabet/sizeof header. Preserve all original source/helpers/Ready/specs and both unrelated frozen GP-core444/580 units. No exception to collect/helper collisions.')
    write_json(LANE/'feasibility.json',result);write_json(LANE/'corrected-private-row.json',row);print(dict(status=result['status'],unsignedHelperReturns=len(unsigned),signedHelperReturns=len(signed),randReturns=len(rand),correctedSymbol='_u32_div_f',bytes=44,exactGenuineNativeLink=True,frozenInputsUnchanged=len(before)),flush=True)


if __name__=='__main__':main()
