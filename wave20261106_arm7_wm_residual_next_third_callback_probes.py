import os
import re
import subprocess
from project import ROOT,read_json,sha256
from elftools.elf.elffile import ELFFile
from link_runtime_unit import binding_object,LINKER,LINKER_HASH
from wave20261106_arm7_wm_residual_next_third_build import SOURCE,WORK,LANE,COMPILER,FLAGS


def compile_source(source,obj):
    return subprocess.run([str(COMPILER),*FLAGS,'-requireprotos','-w','error','-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))


def execute(rows):
    certificates=read_json(LANE/'callback-certificate.json')['callbacks'];results=[]
    for record in certificates:
        if any(r['symbol']==record['symbol']for r in results):continue
        row=next(r for r in rows if r['address']==record['callerAddress']);tag=format(int(row['address'],0),'08x');folder=WORK/'callback-types'/record['symbol'];folder.mkdir(parents=True,exist_ok=True);headers={p.name:p.read_text()for p in(SOURCE/tag).glob('*.h')}
        for name,text in headers.items():(folder/name).write_text(text)
        source=folder/'pointer.c';source.write_text('\n'.join('#include "'+name+'"'for name in sorted(headers))+'\nconst OSVAlarmHandler witness='+record['symbol']+';\n');obj=folder/'pointer.o';process=compile_source(source,obj)
        if process.returncode:raise ValueError(('Actual owned C99 function-pointer initializer rejected',record['symbol'],process.stdout,process.stderr))
        with obj.open('rb')as stream:
            elf=ELFFile(stream);flags=elf['e_flags'];symbols=list(elf.get_section_by_name('.symtab').iter_symbols());witness=next(s for s in symbols if s.name=='witness');section=elf.get_section(witness['st_shndx']);relocations=[]
            if witness['st_info']['type']!='STT_OBJECT'or witness['st_size']!=4 or section['sh_type']!='SHT_PROGBITS'or any(s['sh_size']for s in elf.iter_sections()if s['sh_flags']&4):raise ValueError('Actual typed pointer object has wrong storage/type or executable code')
            for relSection in elf.iter_sections():
                if relSection['sh_type']!='SHT_RELA'or relSection['sh_info']!=witness['st_shndx']:continue
                table=elf.get_section(relSection['sh_link'])
                for rel in relSection.iter_relocations():relocations.append(dict(offset=rel['r_offset'],kind=rel['r_info_type'],addend=rel['r_addend'],symbol=table.get_symbol(rel['r_info_sym']).name))
            if relocations!=[dict(offset=0,kind=2,addend=0,symbol=record['symbol'])]:raise ValueError('Actual immutable C function-pointer ABS32 witness differs')
            sectionName=section.name
        anchor=folder/'anchor.o';binding_object(record['symbol'],'arm',flags,anchor);lcf=folder/'pointer.lcf';lcf.write_text('MEMORY { DATA: ORIGIN = 0x02012000 > pointer.bin\nFUNC: ORIGIN = '+record['address']+' > anchor.bin }\nSECTIONS { .pointer: { pointer.o('+sectionName+') } > DATA\n.binding: { anchor.o(.text) } > FUNC }\n');linked=folder/'linked.elf';command=[str(LINKER),'-nostdlib','-nodeadstrip','-interworking','-proc','arm7tdmi','-main','witness',str(lcf),str(obj),str(anchor),'-o',str(linked)];process=subprocess.run(command,cwd=folder,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
        if process.returncode or sha256(LINKER)!=LINKER_HASH or(folder/'pointer.bin').read_bytes()!=bytes.fromhex(record['originalLiteralHex'])or((folder/'anchor.bin').exists()and(folder/'anchor.bin').stat().st_size):raise ValueError(('Actual typed pointer genuine ARM7 link differs',process.stdout,process.stderr))
        with linked.open('rb')as stream:
            elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());target=next(s for s in symbols if s.name==record['symbol'])
            if target['st_info']['type']!='STT_FUNC'or target['st_size']or target['st_value']!=int(record['address'],0)or not any(s.name=='$a'and s['st_shndx']==target['st_shndx']and s['st_value']==target['st_value']for s in symbols):raise ValueError('Actual linked function-pointer target is not exact zero-code ARM/STT_FUNC')
        negatives=[];pattern=re.compile(r'(?m)^([ \t]*(?:[A-Za-z_]\w*[ \t*]+)+)'+re.escape(record['symbol'])+r'([ \t]*\([^;{}]*\)[ \t]*;)');found=[name for name,text in headers.items()if pattern.search(text)]
        if not found:raise ValueError('Actual callback function declarations absent from owned header closure')
        for label,replacement in [('data-object','extern u32 '+record['symbol']+';'),('wrong-call-signature','extern void '+record['symbol']+'(void);')]:
            for name,text in headers.items():(folder/name).write_text(pattern.sub(replacement,text)if name in found else text)
            bad=folder/(label+'.o');bad.unlink(missing_ok=True);process=compile_source(source,bad)
            if process.returncode==0 or bad.exists():raise ValueError('Wrong actual C data/function/callback signature admitted')
            negatives.append(dict(case=label,rejected=True,exitCode=process.returncode,stdout=process.stdout))
        for name,text in headers.items():(folder/name).write_text(text)
        results.append(dict(symbol=record['symbol'],sourceSha256=sha256(source),objectSha256=sha256(obj),actualFunctionPointerObjectBytes=4,actualOriginalUnchangedRelocations=relocations,genuineLinkedPointerHex=(folder/'pointer.bin').read_bytes().hex(),linkedElfSha256=sha256(linked),targetMode='arm',targetELFType='STT_FUNC',initializedCalleeCodeBytes=0,negativeControls=negatives))
    return dict(status='passed',sourceCredit=0,uniqueCallbackTargets=len(results),witnesses=results,limits=['Fresh actual owned headers and -lang c99/-requireprotos/-w error function-pointer initializers; actual STT_OBJECT4/R_ARM_ABS32+0 genuinely links to exact original zero-code ARM/STT_FUNC targets. These diagnostic pointer objects/storage and imported callback bodies receive0 source credit.'])
