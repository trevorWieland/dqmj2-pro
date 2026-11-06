import os
import subprocess
import match_runtime as C
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,read_json
from link_runtime_unit import binding_object,LINKER,LINKER_HASH,relocation_rows
from wave20261106_arm7_pm_mic_next_first_build import SOURCE,LANE,WORK,FLAGS,COMPILER

NAME='native_host_arm7_arm_038059ac'
DECLARATION='void (*const pointer)(void)='+NAME+';'


def actual(label,declaration):
    folder=WORK/'callback-abi'/label;folder.mkdir(parents=True,exist_ok=True);headers=sorted((SOURCE/'03805784').glob('*.h'))
    for header in headers:(folder/header.name).write_bytes(header.read_bytes())
    source=folder/'probe.c';obj=folder/'probe.o';prefix=''.join('#include "'+p.name+'"\n'for p in headers);source.write_text(prefix+declaration+'\n');argv=[str(COMPILER),*FLAGS,'-requireprotos','-w','error','-c',str(source),'-o',str(obj)];process=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(('Actual typed C99 callback probe rejected',process.stdout,process.stderr))
    if source.read_text()!=prefix+DECLARATION+'\n':raise ValueError('Actual source pointer type/sole original callable initializer differs')
    with obj.open('rb')as stream:
        elf=ELFFile(stream);flags=elf['e_flags'];symbols=list(elf.get_section_by_name('.symtab').iter_symbols());pointer=next(s for s in symbols if s.name=='pointer');section=elf.get_section(pointer['st_shndx']);undefined=next(s for s in symbols if s.name==NAME)
        if pointer['st_info']['type']!='STT_OBJECT'or pointer['st_size']!=4 or undefined['st_shndx']!='SHN_UNDEF'or undefined['st_info']['type']!='STT_NOTYPE'or any(s['sh_size']for s in elf.iter_sections()if s['sh_flags']&6==6):raise ValueError('Fresh compiler pointer/function declaration acquired code/storage/type mismatch')
        records=[]
        for item in elf.iter_sections():
            if item['sh_type']not in ['SHT_REL','SHT_RELA']or item['sh_info']!=pointer['st_shndx']:continue
            table=elf.get_section(item['sh_link'])
            for relocation in item.iter_relocations():records.append((item['sh_type'],relocation['r_offset']-pointer['st_value'],relocation['r_info_type'],table.get_symbol(relocation['r_info_sym']).name,relocation['r_addend']if item['sh_type']=='SHT_RELA'else None))
        if records!=[('SHT_RELA',0,2,NAME,0)]:raise ValueError('Actual typed compiler pointer relocation/addend differs')
    anchor=folder/'anchor.o';binding_object(NAME,'arm',flags,anchor);lcf=folder/'pointer.lcf';lcf.write_text('MEMORY { CALL: ORIGIN = 0x02020000 > pointer.bin\nBIND: ORIGIN = 0x038059ac > anchor.bin }\nSECTIONS { .pointer: { probe.o('+section.name+') } > CALL\n.binding: { anchor.o(.text) } > BIND }\n');linked=folder/'linked.elf';command=[str(LINKER),'-nostdlib','-nodeadstrip','-interworking','-proc','arm7tdmi','-main','pointer',str(lcf),str(obj),str(anchor),'-o',str(linked)];process=subprocess.run(command,cwd=folder,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode or sha256(LINKER)!=LINKER_HASH or(folder/'pointer.bin').read_bytes()!=(0x038059ac).to_bytes(4,'little')or((folder/'anchor.bin').exists()and(folder/'anchor.bin').stat().st_size):raise ValueError(('Actual zero-code ARM callback link differs',process.stdout,process.stderr))
    with linked.open('rb')as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());symbol=next(s for s in symbols if s.name==NAME)
        if symbol['st_info']['type']!='STT_FUNC'or symbol['st_value']!=0x038059ac or symbol['st_size']or not any(s.name=='$a'and s['st_value']==0x038059ac and s['st_shndx']==symbol['st_shndx']for s in symbols):raise ValueError('Actual original callback ELF function/mode identity differs')
    return dict(status='passed',sourceCredit=0,sourceSha256=sha256(source),objectSha256=sha256(obj),linkedElfSha256=sha256(linked),initializedPointerBytes=4,initializedCallbackCodeBytes=0,calleeSourceCredit=0,actualCompilerRelocations=records,actualLinkedWord='0x38059ac')


def execute(rows):
    row=next(r for r in rows if r['address']=='0x3805784');relocations=[r for r in row['relocations']if r['symbol']==NAME]
    if len(relocations)!=1 or relocations[0]['offset']!=540 or row['nativeSymbolEntries'][NAME]!={'program':'','processor':'arm7','module':'arm7-wram','mode':'arm','kind':'function','address':'0x38059ac','boundarySource':'measured-runtime-map-Ghidra-entry; caller-boundary-audit-separate'}:raise ValueError('Exact single original MIC callback site/namespace differs')
    positive=actual('positive',DECLARATION);bad=[]
    for label,declaration in [('wrong-signature','u32 (*const pointer)(void)=(u32(*)(void))'+NAME+';'),('null-target','void (*const pointer)(void)=0;'),('two-objects','void (*const pointer[2])(void)={'+NAME+','+NAME+'};'),('data-instead','const u32 pointer=(u32)'+NAME+';')]:
        try:actual(label,declaration)
        except ValueError as error:bad.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong typed callback/data ABI admitted')
    return dict(status='passed',sourceCredit=0,originalOrigin='0x38059a0',originalLiteral=(ROOT/row['binary']).read_bytes()[int(row['address'],0)-row['base']+540:int(row['address'],0)-row['base']+544].hex(),positive=positive,negativeControls=bad,limits=['One genuine compiler-emitted const function-pointer object and the exact original same-program ARM7-wram ARM entry; no IRQ body execution, alternate entry, callee/storage/source credit or shared resolver change.'])
