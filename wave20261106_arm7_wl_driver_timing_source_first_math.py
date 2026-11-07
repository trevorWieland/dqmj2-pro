import copy
import os
import subprocess
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from elftools.elf.elffile import ELFFile
from project import ROOT,read_json,write_json,sha256
from link_runtime_unit import binding_object,relocation_rows,LINKER,LINKER_HASH
from wave20261106_arm7_wl_driver_timing_source_first_build import LANE,WORK,COMPILER,FLAGS
CERTIFICATE=LANE/'math-certificate.json'
CERTIFICATE_SHA='8d0ae116938e2e090a47c8e529da85aa0d3467f08612463f289039e9fc35a03c'


def verify(row,rel,binding,record=None,image=None):
    if sha256(CERTIFICATE)!=CERTIFICATE_SHA:raise ValueError('Immutable exact ARM7 compiler helper certificate changed')
    records=read_json(CERTIFICATE)['helpers'];expected=[r for r in records if r['callerAddress']==row['address']and r['symbol']==rel['symbol']]
    if len(expected)!=1:raise ValueError('No qualified exact original ARM7 compiler helper site/name')
    expected=expected[0];record=expected if record is None else record
    if record!=expected:raise ValueError('Qualified compiler helper original identity/profile/witness differs')
    if (row.get('sourceModule'),row['program'],row['processor'],row['module'],row['mode'],row['name'],row['targetSha256'],row['compiler'],row['compilerSha256'],row['compilerFlags'])!=('arm7-main','','arm7','arm7-main','arm',record['callerName'],record['callerSpanSha256'],record['compiler'],record['compilerSha256'],record['compilerFlags']):raise ValueError('Exact original caller sourceModule/CPU/program/ARM/profile differs')
    if (binding['program'],binding['processor'],binding['module'],binding['mode'],binding['kind'],binding['address'])!=('','arm7','arm7-wram','arm','function',record['address']):raise ValueError('Exact original ARM7-wram compiler helper target/mode differs')
    if hex(int(row['address'],0)+rel['offset'])!=record['origin']or rel['type']!=1 or rel['format']!='SHT_RELA'or rel['explicitAddend']!=-8:raise ValueError('Exact original emitted helper BL origin/addend differs')
    raw=(ROOT/record['binary']).read_bytes()if image is None else image;layout=next(m for m in read_json(ROOT/'evidence/arm7/runtime-layout.json')['modules']if m['name']=='arm7-wram');offset=int(record['address'],0)-int(layout['base'],0)
    if C.sha(raw)!=record['inputModuleSha256']or raw[offset:offset+record['entryWitnessBytes']].hex()!=record['entryWitnessHex']or C.sha(raw[offset:offset+record['entryWitnessBytes']])!=record['entryWitnessSha256']:raise ValueError('Exact original ARM7-wram image/entry witness changed')
    caller=(ROOT/row['binary']).read_bytes();origin=int(record['origin'],0)-row['base'];word=caller[origin:origin+4]
    if word.hex()!=record['originalCallHex']or int.from_bytes(word,'little')>>24!=0xeb:raise ValueError('Actual original ARM BL helper word differs')
    displacement=int.from_bytes(word,'little')&0xffffff;displacement-=0x1000000 if displacement&0x800000 else 0
    if int(record['origin'],0)+8+displacement*4!=int(record['address'],0):raise ValueError('Actual original ARM helper branch destination differs')
    return dict(status='passed',sourceCredit=0,certificateSha256=CERTIFICATE_SHA,originalCaller=record['callerAddress'],origin=record['origin'],originalHex=record['originalCallHex'],provider=record['symbol'],address=record['address'],sourceModule='arm7-main',processor='arm7',module='arm7-wram',mode='arm')


def controls(rows):
    positive=[];bad=[]
    for row in rows:
        for rel in row['relocations']:
            if rel['symbol']not in ['_u32_div_f','_ll_udiv']:continue
            binding=row['nativeSymbolEntries'][rel['symbol']];positive.append(verify(row,rel,binding));record=next(r for r in read_json(CERTIFICATE)['helpers']if r['symbol']==rel['symbol']and r['callerAddress']==row['address'])
            for label,owner,key,value in [('sourceModule','row','sourceModule','main'),('CPU','binding','processor','arm9'),('program','binding','program','dwc/utility.bin/move/child.srl'),('module','binding','module','main'),('mode','binding','mode','thumb'),('target-plus4','binding','address',hex(int(binding['address'],0)+4)),('provider-name','rel','symbol','_s32_div_f'if rel['symbol']=='_u32_div_f'else '_u32_div_f'),('source-CPU','row','processor','arm9'),('origin-plus4','rel','offset',rel['offset']+4),('entry-hash','record','entryWitnessSha256','0'*64),('profile-hash','row','compilerSha256','0'*64)]:
                parts={n:copy.deepcopy(v)for n,v in [('row',row),('rel',rel),('binding',binding),('record',record)]};parts[owner][key]=value
                try:verify(**parts)
                except ValueError as error:bad.append(dict(provider=rel['symbol'],case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Wrong exact ARM7 compiler helper identity admitted')
    if len(positive)!=3:raise ValueError('Exact three original compiler helper sites required')
    return dict(status='passed',sourceCredit=0,positive=positive,negativeControls=bad,actualCompilerAndOriginalNativeABI=abi())


def abi():
    directory=WORK/'math-abi';directory.mkdir(parents=True,exist_ok=True);results=[];module=next(m for m in read_json(ROOT/'evidence/arm7/runtime-layout.json')['modules']if m['name']=='arm7-wram');base=int(module['base'],0);image=(ROOT/module['binary']).read_bytes();records=read_json(CERTIFICATE)['helpers']
    for width in [32,64]:
        name='_u32_div_f'if width==32 else'_ll_udiv';record=next(r for r in records if r['symbol']==name);target=int(record['address'],0);folder=directory/str(width);folder.mkdir(parents=True,exist_ok=True);typ='unsigned long'if width==32 else'unsigned long long';source=folder/'probe.c';source.write_text(typ+' probe('+typ+','+typ+');\n'+typ+' probe('+typ+' a,'+typ+' b){return a/b;}\n');obj=folder/'probe.o';command=[str(COMPILER),*FLAGS,'-requireprotos','-w','error','-c',str(source),'-o',str(obj)];p=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
        if p.returncode:raise ValueError(('Fresh actual typed division ABI compilation failed',p.stdout,p.stderr))
        relocations=relocation_rows(obj,'probe')
        if len(relocations)!=1 or relocations[0]['symbol']!=name or relocations[0]['type']not in [1,2]:raise ValueError('Actual unsigned word-width/operator emits different compiler helper')
        with obj.open('rb')as stream:flags=ELFFile(stream)['e_flags']
        anchor=folder/'anchor.o';binding_object(name,'arm',flags,anchor);lcf=folder/'unit.lcf';lcf.write_text('MEMORY {CALL: ORIGIN=0x02012000 > caller.bin\nBIND: ORIGIN='+hex(target)+' > anchor.bin}\nSECTIONS{.caller:{probe.o(.text)}>CALL\n.binding:{anchor.o(.text)}>BIND}\n');linked=folder/'linked.elf';p=subprocess.run([str(LINKER),'-nostdlib','-nodeadstrip','-interworking','-proc','arm7tdmi','-main','probe',str(lcf),str(obj),str(anchor),'-o',str(linked)],cwd=folder,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
        if p.returncode or sha256(LINKER)!=LINKER_HASH or((folder/'anchor.bin').exists()and(folder/'anchor.bin').stat().st_size):raise ValueError(('Actual ARM7 division helper genuine link failed',p.stdout,p.stderr))
        with linked.open('rb')as stream:
            elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());function=next(s for s in symbols if s.name==name)
            if function['st_info']['type']!='STT_FUNC'or function['st_value']!=target or function['st_size']or not any(s.name=='$a'and s['st_value']==target and s['st_shndx']==function['st_shndx']for s in symbols):raise ValueError('Actual native ARM7 arithmetic helper type/mode/zero-code target differs')
        cases=[(0,1),(1,1),(0xffffffff,1),(0xffffffff,65535),(0x80000001,3),(0x80000000,2),(1000,33)]if width==32 else[(0,1),(1,1),(0xffffffffffffffff,1),(0xffffffffffffffff,65535),(0x1234567890abcdef,1000),(0xffffffffffffffff,0x100000001),(33514*0xffffffff//64,1000)];runs=[];body=(folder/'caller.bin').read_bytes()
        for a,b in cases:
            vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_TI925T);vm.mem_map(0x02000000,0x800000);vm.mem_map(0x037f8000,0x20000);vm.mem_write(base,image);vm.mem_write(0x02012000,body);vm.reg_write(R.UC_ARM_REG_CPSR,0x10);args=[a,b]if width==32 else[a&0xffffffff,a>>32,b&0xffffffff,b>>32]
            for reg,value in zip(C.REGISTERS,args):vm.reg_write(reg,value)
            vm.reg_write(R.UC_ARM_REG_SP,0x027fc000);vm.reg_write(R.UC_ARM_REG_LR,0x02013000);saved={r:0x98760000+i for i,r in enumerate(C.REGISTERS[4:12])};pcs=[]
            for reg,value in saved.items():vm.reg_write(reg,value)
            def hook(uc,address,length,user):
                if address==0x02013000:return
                if not(0x02012000<=address<0x02012000+len(body)or base<=address<base+len(image))or uc.reg_read(R.UC_ARM_REG_CPSR)&32:raise ValueError('Original arithmetic helper escaped its actual ARM7-wram module/mode')
                pcs.append(address)
            vm.hook_add(unicorn.UC_HOOK_CODE,hook);vm.emu_start(0x02012000,0x02013000,count=4000);actual=vm.reg_read(R.UC_ARM_REG_R0)|(vm.reg_read(R.UC_ARM_REG_R1)<<32 if width==64 else 0)
            if vm.reg_read(R.UC_ARM_REG_PC)!=0x02013000 or vm.reg_read(R.UC_ARM_REG_SP)!=0x027fc000 or actual!=a//b or target not in pcs or any(vm.reg_read(reg)!=value for reg,value in saved.items()):raise ValueError('Actual original helper and unsigned32/64 quotient/callee-saved ABI differ')
            runs.append(dict(a=a,b=b,returned=actual,originalHelperInstructions=sum(base<=pc<base+len(image)for pc in pcs)))
        results.append(dict(provider=name,processor='arm7',module='arm7-wram',mode='arm',typedWidth=width,actualCompilerRelocations=relocations,sourceSha256=sha256(source),objectSha256=sha256(obj),linkedElfSha256=sha256(linked),actualReturns=len(runs),cases=runs))
    return dict(status='passed',sourceCredit=0,helperCredit=0,actualNativeOriginalHelperReturns=sum(r['actualReturns']for r in results),probes=results,limits=['Separate fresh typed-C probes execute actual original ARM7-wram arithmetic code to measured returns. No ARM9 alias, helper source/storage/body credit or executable implementation input. Production selected-caller fixtures intercept imports and execute0 provider bodies.'])


if __name__=='__main__':
    rows=read_json(WORK/'per-entry-pilot-results.json')['rows'];result=controls(rows);write_json(LANE/'math-qualification.json',result);print(dict(status=result['status'],sites=len(result['positive']),negativeControls=len(result['negativeControls']),actualReturns=result['actualCompilerAndOriginalNativeABI']['actualNativeOriginalHelperReturns']))

