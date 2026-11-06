import copy
import os
import subprocess
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from elftools.elf.elffile import ELFFile
from project import ROOT,read_json,write_json,sha256
from link_runtime_unit import binding_object,relocation_rows,LINKER,LINKER_HASH
from wave20261106_arm7_wm_residual_next_second_build import LANE,WORK,COMPILER,FLAGS
CERTIFICATE=LANE/'compiler-helper-certificate.json'
CERTIFICATE_SHA='336c4eeb493d50608a54c1d4112215a0f1cd63a8402a981668e035c0efd5426a'


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
    if C.sha(raw)!=record['inputModuleSha256']or raw[offset:offset+4].hex()!=record['entryWitnessHex']or C.sha(raw[offset:offset+4])!=record['entryWitnessSha256']:raise ValueError('Exact original ARM7-wram image/entry witness changed')
    caller=(ROOT/row['binary']).read_bytes();origin=int(record['origin'],0)-row['base'];word=caller[origin:origin+4]
    if word.hex()!=record['originalCallHex']or int.from_bytes(word,'little')>>24!=0xeb:raise ValueError('Actual original ARM BL helper word differs')
    displacement=int.from_bytes(word,'little')&0xffffff;displacement-=0x1000000 if displacement&0x800000 else 0
    if int(record['origin'],0)+8+displacement*4!=int(record['address'],0):raise ValueError('Actual original ARM helper branch destination differs')
    return dict(status='passed',sourceCredit=0,certificateSha256=CERTIFICATE_SHA,originalCaller=record['callerAddress'],origin=record['origin'],originalHex=record['originalCallHex'],provider=record['symbol'],address=record['address'],sourceModule='arm7-main',processor='arm7',module='arm7-wram',mode='arm')


def controls(rows):
    positive=[];bad=[]
    for row in rows:
        for rel in row['relocations']:
            if rel['symbol']not in ['_u32_div_f','_s32_div_f']:continue
            binding=row['nativeSymbolEntries'][rel['symbol']];positive.append(verify(row,rel,binding));record=next(r for r in read_json(CERTIFICATE)['helpers']if r['symbol']==rel['symbol'])
            for label,owner,key,value in [('sourceModule','row','sourceModule','main'),('CPU','binding','processor','arm9'),('program','binding','program','dwc/utility.bin/move/child.srl'),('module','binding','module','main'),('mode','binding','mode','thumb'),('target-plus4','binding','address',hex(int(binding['address'],0)+4)),('provider-name','rel','symbol','_s32_div_f'if rel['symbol']=='_u32_div_f'else '_u32_div_f'),('source-CPU','row','processor','arm9'),('origin-plus4','rel','offset',rel['offset']+4),('entry-hash','record','entryWitnessSha256','0'*64),('profile-hash','row','compilerSha256','0'*64)]:
                parts={n:copy.deepcopy(v)for n,v in [('row',row),('rel',rel),('binding',binding),('record',record)]};parts[owner][key]=value
                try:verify(**parts)
                except ValueError as error:bad.append(dict(provider=rel['symbol'],case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Wrong exact ARM7 compiler helper identity admitted')
    if len(positive)!=2:raise ValueError('Exact two original compiler helper sites required')
    return dict(status='passed',sourceCredit=0,positive=positive,negativeControls=bad,actualCompilerAndOriginalNativeABI=abi())


def abi():
    directory=WORK/'math-abi';directory.mkdir(parents=True,exist_ok=True);results=[];layout=read_json(ROOT/'evidence/arm7/runtime-layout.json');wram=next(m for m in layout['modules']if m['name']=='arm7-wram');start=int(wram['base'],0);image=(ROOT/wram['binary']).read_bytes();records=read_json(CERTIFICATE)['helpers']
    for signed in [False,True]:
        record=next(r for r in records if r['symbol']==('_s32_div_f'if signed else '_u32_div_f'));target=int(record['address'],0)
        for remainder in [False,True]:
            folder=directory/('signed'if signed else 'unsigned')/('remainder'if remainder else 'quotient');folder.mkdir(parents=True,exist_ok=True);typ='s32'if signed else'u32';source=folder/'probe.c';source.write_text('typedef unsigned long u32;\ntypedef signed long s32;\n'+typ+' probe('+typ+','+typ+');\n'+typ+' probe('+typ+' a,'+typ+' b){return a'+('%'if remainder else'/')+'b;}\n');obj=folder/'probe.o';command=[str(COMPILER),*FLAGS,'-requireprotos','-w','error','-c',str(source),'-o',str(obj)];p=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
            if p.returncode:raise ValueError(('Actual typed C99 compiler ABI witness failed',p.stdout,p.stderr))
            relocations=relocation_rows(obj,'probe')
            if len(relocations)!=1 or relocations[0]['symbol']!=record['symbol']:raise ValueError('Actual signedness/operator emits a different helper ABI')
            with obj.open('rb')as stream:
                elf=ELFFile(stream);flags=elf['e_flags'];symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name=='probe');size=symbol['st_size']
            anchor=folder/'anchor.o';binding_object(record['symbol'],'arm',flags,anchor);lcf=folder/'probe.lcf';lcf.write_text('MEMORY { CALL: ORIGIN = 0x02012000 > caller.bin\nBIND: ORIGIN = '+hex(target)+' > anchor.bin }\nSECTIONS { .caller: { probe.o(.text) } > CALL\n.binding: { anchor.o(.text) } > BIND }\n');linked=folder/'linked.elf';argv=[str(LINKER),'-nostdlib','-nodeadstrip','-interworking','-proc','arm7tdmi','-main','probe',str(lcf),str(obj),str(anchor),'-o',str(linked)];p=subprocess.run(argv,cwd=folder,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
            if p.returncode or sha256(LINKER)!=LINKER_HASH or((folder/'anchor.bin').exists()and(folder/'anchor.bin').stat().st_size):raise ValueError(('Actual unchanged compiler-helper ABI link failed',p.stdout,p.stderr))
            with anchor.open('rb')as stream:
                anchorElf=ELFFile(stream)
                if [(s['sh_type'],s['sh_size'],s['sh_flags'])for s in anchorElf.iter_sections()if s['sh_flags']&2]!=[('SHT_NOBITS',4,6)]:raise ValueError('Diagnostic helper anchor differs from original zero-initialized-code binding object')
            with linked.open('rb')as stream:
                linkedElf=ELFFile(stream);symbols=list(linkedElf.get_section_by_name('.symtab').iter_symbols());function=next(s for s in symbols if s.name==record['symbol'])
                if function['st_info']['type']!='STT_FUNC'or function['st_value']!=target or function['st_size']or not any(s.name=='$a'and s['st_value']==target and s['st_shndx']==function['st_shndx']for s in symbols):raise ValueError('Actual diagnostic helper ARM/STT_FUNC/zero-code target differs')
            body=(folder/'caller.bin').read_bytes();cases=[(0,1),(-1,1),(-7,3),(7,-3),(-7,-3),(-2147483648,1),(2147483647,65535)]if signed else[(0,1),(1,1),(0xffffffff,1),(0xffffffff,65535),(0x80000001,3),(0x80000000,2),(1000,33)];runs=[]
            for a,b in cases:
                vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_TI925T);vm.mem_map(0x02000000,0x800000);vm.mem_map(0x037f8000,0x20000);vm.mem_write(start,image);vm.mem_write(0x02012000,body);vm.reg_write(R.UC_ARM_REG_CPSR,0x10);vm.reg_write(R.UC_ARM_REG_R0,a&0xffffffff);vm.reg_write(R.UC_ARM_REG_R1,b&0xffffffff);vm.reg_write(R.UC_ARM_REG_SP,0x027fc000);vm.reg_write(R.UC_ARM_REG_LR,0x02013000);pcs=[];saved={r:0x98760000+i for i,r in enumerate(C.REGISTERS[4:12])}
                for register,value in saved.items():vm.reg_write(register,value)
                def hook(uc,address,length,user):
                    if address==0x02013000:return
                    if not(0x02012000<=address<0x02012000+len(body)or start<=address<start+len(image))or uc.reg_read(R.UC_ARM_REG_CPSR)&32:raise ValueError('Original ARM7 compiler helper escaped exact ARM/module ABI probe')
                    pcs.append(address)
                vm.hook_add(unicorn.UC_HOOK_CODE,hook);vm.emu_start(0x02012000,0x02013000,count=3000);q=(abs(a)//abs(b))*(-1 if(a<0)!=(b<0)else 1)if signed else a//b;expected=(a-q*b if remainder else q)&0xffffffff
                if vm.reg_read(R.UC_ARM_REG_PC)!=0x02013000 or vm.reg_read(R.UC_ARM_REG_SP)!=0x027fc000 or vm.reg_read(R.UC_ARM_REG_R0)!=expected or target not in pcs or any(vm.reg_read(r)!=v for r,v in saved.items()):raise ValueError('Actual original ARM7 helper and typed quotient/remainder/callee-saved ABI differ')
                runs.append(dict(a=a,b=b,returned=expected,actualOriginalHelperInstructions=sum(start<=x<start+len(image)for x in pcs)))
            results.append(dict(provider=record['symbol'],typedReturn=typ,operator='%'if remainder else'/',sourceSha256=sha256(source),objectSha256=sha256(obj),linkedElfSha256=sha256(linked),linkedCallerSha256=C.sha(body),cases=runs,actualReturns=len(runs)))
    return dict(status='passed',sourceCredit=0,actualNativeOriginalHelperReturns=sum(r['actualReturns']for r in results),probes=results,limits=['These separate typed compiler ABI probes execute only diagnostic callers and actual original ARM7-wram arithmetic bytes. They reconstruct/credit no helper source or body extent. Production caller fixtures separately execute zero imported bodies. No object/symbol/relocation rewrite or global ARM9 alias fallback.'])


if __name__=='__main__':
    from wave20261106_arm7_wm_residual_next_second_build import build_all
    rows,outputs=build_all(WORK/'math-check');result=controls(rows);write_json(LANE/'math-controls.json',result);print(dict(originalSites=len(result['positive']),negatives=len(result['negativeControls']),actualNativeHelperReturns=result['actualCompilerAndOriginalNativeABI']['actualNativeOriginalHelperReturns']),flush=True)
