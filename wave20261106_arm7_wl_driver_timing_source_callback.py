import copy
import re
import os
import struct
import subprocess
from project import ROOT,read_json,write_json,sha256
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from elftools.elf.elffile import ELFFile
from link_runtime_unit import binding_object,relocation_rows,LINKER,LINKER_HASH

CERTIFICATE=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-driver-timing-next/first/callback-certificate.json'
SHA='f912ed1139854b3e5038ce69a08d9da168ecab68af1f2eda3b2ee591770f157b'
WORK=ROOT/'work/w6wdt/callback'


def source_type(text):
    name='native_host_arm7_arm_027ea9a8';pattern=r'(?m)^\s*(?:extern\s+)?void\s+'+name+r'\s*\(\s*void\s*\*\s*arg\s*\)\s*;'
    if len(re.findall(pattern,text))!=1:raise ValueError('Actual owned callback declaration is not the original void(void*) function interface')
    return True


def qualify(row,relocation,image,modules):
    if sha256(CERTIFICATE)!=SHA:raise ValueError('Frozen exact original callback certificate changed')
    pin=read_json(CERTIFICATE)
    if (row.get('program')or'',row['processor'],row['module'],row['mode'],row.get('sourceModule'),row['address'],row['bytes'],row['targetSha256'])!=('','arm7','arm7-main','arm','arm7-main',pin['callerAddress'],180,pin['callerSha256']):raise ValueError('Exact callback caller namespace/span changed')
    if (relocation['symbol'],relocation['type'],relocation['format'],relocation['explicitAddend'],int(row['address'],0)+relocation['offset'])!=(pin['symbol'],2,'SHT_RELA',0,int(pin['origin'],0)):raise ValueError('Exact original typed callback ABS32 symbol/origin/addend differs')
    module=modules['arm7-main'];base=int(module['base'],0)
    if module['sha256']!=pin['inputModuleSha256']or C.sha(image)!=pin['inputModuleSha256']or base!=0x027e0000:raise ValueError('Actual original callback ARM7 module differs')
    address=int(pin['address'],0);body=image[address-base:address-base+12];caller=int(row['address'],0)
    if C.sha(image[caller-base:caller-base+180])!=pin['callerSha256']or image[int(pin['origin'],0)-base:int(pin['origin'],0)-base+4].hex()!=pin['originalWord']:raise ValueError('Complete native caller/literal word differs')
    if struct.unpack('<3I',body)!=(0xe3a01000,0xe5801000,0xe12fff1e)or C.sha(body)!=pin['nativeBodySha256']or int.from_bytes(bytes.fromhex(pin['originalWord']),'little')!=address:raise ValueError('Actual ARMv4T zero-word-store callback instructions/type tag differ')
    if any(pin[k]for k in ['sourceCredit','calleeCredit','storageCredit']):raise ValueError('Imported callback acquired source/body/storage credit')
    from wave20261106_arm7_wl_driver_timing_source_first_build import dependencies
    source_type('\n'.join((ROOT/name).read_text()for name in [row['source']]+[p['path']for p in dependencies(ROOT/row['source'])]))
    return dict(program='',processor='arm7',module='arm7-main',mode='arm',kind='function',address=pin['address'],boundarySource='exact-original-ABS32-caller-typed-C-pointer-and-three-reachable-ARMv4T-words-zero-credit')


def controls(row,relocation,image,modules):
    results=[];positive=qualify(row,relocation,image,modules)
    for label in ['cpu','program','module','source-module','mode','caller-address','caller-hash','origin','symbol','kind','addend','caller-word','callback-word','module-hash']:
        r,t,m=copy.deepcopy(row),copy.deepcopy(relocation),copy.deepcopy(modules);native=image
        if label=='cpu':r['processor']='arm9'
        elif label=='program':r['program']='dwc/utility.bin/move/child.srl'
        elif label=='module':r['module']='arm7-wram'
        elif label=='source-module':r['sourceModule']='main'
        elif label=='mode':r['mode']='thumb'
        elif label=='caller-address':r['address']=hex(int(r['address'],0)+4)
        elif label=='caller-hash':r['targetSha256']='0'*64
        elif label=='origin':t['offset']+=4
        elif label=='symbol':t['symbol']='native_host_arm7_arm_027ea9ac'
        elif label=='kind':t['type']=1
        elif label=='addend':t['explicitAddend']=4
        elif label=='module-hash':m['arm7-main']['sha256']='0'*64
        else:
            native=bytearray(image);at=(0x027e9e24 if label=='caller-word'else 0x027ea9a8)-0x027e0000;native[at]^=1;native=bytes(native)
        try:qualify(r,t,native,m)
        except ValueError as error:results.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError(('Unqualified callback substitution admitted',label))
    declaration='void native_host_arm7_arm_027ea9a8(void *arg);'
    for label,text in [('return-type',declaration.replace('void native','unsigned long native')),('argument-type',declaration.replace('void *arg','unsigned short *arg')),('data-confusion','extern unsigned long native_host_arm7_arm_027ea9a8[3];')]:
        try:source_type(text)
        except ValueError as error:results.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong actual callback C declaration admitted')
    return dict(status='passed',sourceCredit=0,calleeCredit=0,positive=positive,negativeControls=results,actualLeafAndTypedPointerABI=abi())


def abi():
    from wave20261106_arm7_wl_driver_timing_source_first_build import FLAGS,COMPILER
    if WORK!=ROOT/'work/w6wdt/callback':raise ValueError('Private callback ABI scope changed')
    WORK.mkdir(parents=True,exist_ok=True);pin=read_json(CERTIFICATE);image=(ROOT/pin['binary']).read_bytes();native=image[0x027ea9a8-0x027e0000:0x027ea9b4-0x027e0000];results=[];negative=[]
    def compile_source(label,body):
        folder=WORK/label;folder.mkdir(parents=True,exist_ok=True);source=folder/'probe.c';obj=folder/'probe.o';source.write_text(body);argv=[str(COMPILER),*FLAGS,'-requireprotos','-w','error','-c',str(source),'-o',str(obj)];p=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
        if p.returncode:raise ValueError(('Actual C99 callback ABI compilation failed',p.stdout,p.stderr))
        return folder,obj
    def body(obj,name):
        with obj.open('rb')as stream:
            elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==name);return elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']]
    def run(code,value):
        vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_TI925T);vm.mem_map(0x02000000,0x800000);vm.mem_write(0x027ea9a8,code);before=bytes((i*37+value)&255 for i in range(32));vm.mem_write(0x02014000,before);vm.reg_write(R.UC_ARM_REG_CPSR,0xa0000010)
        initial=[0xabc00000+i for i in range(15)];initial[0]=0x0201400c;initial[13]=0x027fc000;initial[14]=0x02013000
        for reg,word in zip(C.REGISTERS,initial):vm.reg_write(reg,word)
        vm.emu_start(0x027ea9a8,0x02013000,count=8);after=bytes(vm.mem_read(0x02014000,32));expected=bytearray(before);expected[12:16]=bytes(4);gpr=[vm.reg_read(reg)for reg in C.REGISTERS]
        if after!=bytes(expected)or gpr[0]!=initial[0]or gpr[1]!=0 or gpr[2:]!=initial[2:]or vm.reg_read(R.UC_ARM_REG_PC)!=0x02013000 or vm.reg_read(R.UC_ARM_REG_CPSR)!=0xa0000010:raise ValueError('Actual callback pointed-u32 zero/preserved-neighbor/GPR/SP/flags contract differs')
        return dict(before=before.hex(),after=after.hex(),r0=gpr[0],cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),actualReturn=True)
    folder,obj=compile_source('leaf','void leaf(void *);\nvoid leaf(void *arg){*(unsigned long*)arg=0;}\n');compiled=body(obj,'leaf')
    if compiled!=native or relocation_rows(obj,'leaf'):raise ValueError('Actual typed ordinary C callback leaf differs from full original twelve bytes')
    for value in [0,1,85,170,255]:results.append(dict(native=run(native,value),freshC=run(compiled,value)))
    for label,text in [('halfword','*(unsigned short*)arg=0;'),('wrong-value','*(unsigned long*)arg=1;'),('neighbor','*((unsigned long*)arg+1)=0;')]:
        _,bad=compile_source(label,'void leaf(void *);\nvoid leaf(void *arg){'+text+'}\n')
        try:run(body(bad,'leaf'),165)
        except ValueError as error:negative.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong actual callback C ABI/body admitted')
    symbol=pin['symbol'];folder,obj=compile_source('pointer','typedef void(*Callback)(void*);\nvoid '+symbol+'(void*);\nCallback pointer(void);\nCallback pointer(void){return '+symbol+';}\n');relocations=relocation_rows(obj,'pointer')
    if len(relocations)!=1 or relocations[0]['symbol']!=symbol or relocations[0]['type']!=2:raise ValueError('Actual typed C callback pointer has different ABS32 identity')
    with obj.open('rb')as stream:flags=ELFFile(stream)['e_flags']
    anchor=folder/'anchor.o';binding_object(symbol,'arm',flags,anchor);lcf=folder/'unit.lcf';lcf.write_text('MEMORY{CALL: ORIGIN=0x02012000 > caller.bin\nBIND: ORIGIN=0x027ea9a8 > anchor.bin}\nSECTIONS{.caller:{probe.o(.text)}>CALL\n.binding:{anchor.o(.text)}>BIND}\n');linked=folder/'linked.elf';p=subprocess.run([str(LINKER),'-nostdlib','-nodeadstrip','-interworking','-proc','arm7tdmi','-main','pointer',str(lcf),str(obj),str(anchor),'-o',str(linked)],cwd=folder,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if p.returncode or sha256(LINKER)!=LINKER_HASH or((folder/'anchor.bin').exists()and(folder/'anchor.bin').stat().st_size):raise ValueError(('Genuine typed zero-code ARM callback pointer link failed',p.stdout,p.stderr))
    with linked.open('rb')as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());s=next(s for s in symbols if s.name==symbol)
        if s['st_info']['type']!='STT_FUNC'or s['st_value']!=0x027ea9a8 or s['st_size']or not any(t.name=='$a'and t['st_value']==0x027ea9a8 and t['st_shndx']==s['st_shndx']for t in symbols):raise ValueError('Actual linked callback ELF mode/type/zero-code differs')
    code=(folder/'caller.bin').read_bytes();vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_TI925T);vm.mem_map(0x02000000,0x20000);vm.mem_write(0x02012000,code);vm.reg_write(R.UC_ARM_REG_CPSR,0x10);vm.reg_write(R.UC_ARM_REG_SP,0x0201f000);vm.reg_write(R.UC_ARM_REG_LR,0x02013000);vm.emu_start(0x02012000,0x02013000,count=16)
    if vm.reg_read(R.UC_ARM_REG_R0)!=0x027ea9a8 or vm.reg_read(R.UC_ARM_REG_PC)!=0x02013000:raise ValueError('Genuine typed ARM callback literal/tag differs')
    return dict(status='passed',sourceCredit=0,calleeCredit=0,actualNativeAndFreshLeafReturns=10,pairedLeafRuns=results,genuineTypedPointerReturn=hex(vm.reg_read(R.UC_ARM_REG_R0)),zeroCodeBinding=True,negativeActualC=negative,limits=['Only the exact original twelve-byte zero-word callback and diagnostic typed-pointer caller execute; no imported callback body executes in production caller fixtures, no callee/storage/source credit and no global/native-inventory modification.'])


if __name__=='__main__':
    from wave20261106_arm7_wl_driver_timing_source_first_build import LANE
    from link_arm7_bulk_20261030 import namespace
    c=next(c for c in read_json(LANE/'native-certificate.json')['functions']if int(c['address'],0)==0x027e9d88);w=next(w for w in c['originalBindingWitnesses']if w['sourceSymbol']=='TimeoutDummy');row=dict(c,sourceModule='arm7-main');rel=dict(symbol=w['renamed'],type=2,format='SHT_RELA',explicitAddend=0,offset=int(w['witness']['origin'],0)-int(c['address'],0));modules,functions=namespace('');result=controls(row,rel,(ROOT/c['binary']).read_bytes(),modules);write_json(LANE/'callback-qualification-proposal.json',result);print(dict(status=result['status'],negativeControls=len(result['negativeControls']),sha256=sha256(LANE/'callback-qualification-proposal.json')))
