import json
import os
import subprocess
from pathlib import Path
import link_arm7_bulk_20261030 as linker
from project import ROOT,sha256
from elf_units import split_symbol
from elftools.elf.elffile import ELFFile
from link_runtime_unit import binding_object,relocation_rows


def build(seed,text,directory,bindings):
    directory.mkdir(parents=True,exist_ok=True);source=directory/'draft.c';source.write_text(text,encoding='utf-8');argv=[str(ROOT/seed['compiler']),*seed['compilerFlags'],'-c',str(source),'-o',str(directory/'compiled.o')];result=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode:raise ValueError(result.stdout+result.stderr)
    obj=directory/'compiled.o';caller=directory/'caller.o'
    with obj.open('rb')as stream:
        elf=ELFFile(stream);flags=elf['e_flags'];symbol=next(x for x in elf.get_section_by_name('.symtab').iter_symbols()if x.name==seed['name']);size=symbol['st_size'];split_symbol(elf,seed['name'],caller)
    if relocation_rows(obj,seed['name'])!=relocation_rows(caller,seed['name']):raise ValueError('Diagnostic split modified actual wrong-C relocations')
    memories=[f"CALL: ORIGIN = {int(seed['address'],0):#x} > caller.bin"];sections=['.caller: { caller.o(.text) } > CALL'];objects=[caller];assignments=[];anchors=[]
    for index,(name,binding)in enumerate(sorted(bindings.items())):
        target=int(binding['address'],0)
        if binding['kind']=='function':
            anchor=directory/('anchor'+str(index)+'.o');binding_object(name,binding['mode'],flags,anchor);objects.append(anchor);memories.append(f'BIND{index}: ORIGIN = {target:#x} > anchor{index}.bin');sections.append(f'.binding{index}: {{ anchor{index}.o(.text) }} > BIND{index}');anchors.append(dict(symbol=name,initializedCodeBytes=0,sourceCredit=0))
        else:assignments.append(name+' = '+hex(target)+';')
    lcf=directory/'draft.lcf';lcf.write_text('MEMORY {\n'+'\n'.join(memories)+'\n}\nSECTIONS {\n'+'\n'.join(sections+assignments)+'\n}\n');linked=directory/'linked.elf';command=[str(linker.LINKER),'-nostdlib','-nodeadstrip','-interworking','-proc','arm7tdmi','-main',seed['name'],str(lcf),*map(str,objects),'-o',str(linked)];result=subprocess.run(command,cwd=directory,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode:raise ValueError(result.stdout+result.stderr)
    body=(directory/'caller.bin').read_bytes()
    with linked.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(x for x in elf.get_section_by_name('.symtab').iter_symbols()if x.name==seed['name'])
        if symbol['st_value']!=int(seed['address'],0)or symbol['st_size']!=size or len(body)!=size:raise ValueError('Wrong-C standalone linked extent differs')
    return body,dict(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),compiledBytes=size,object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),actualCompilerArgv=argv,actualCompilerCwd=str(ROOT),actualLinkerArgv=command,actualLinkerCwd=str(directory),linkedElfSha256=sha256(linked),linkedBodySha256=sha256(directory/'caller.bin'),unchangedWrongCRelocations=True,bindings=bindings,zeroCodeAnchors=anchors,diagnosticOnlyBypassesSourceAdmission=False,sourceAdmissionNotRequested=True,existingValidatedAddressesUsedOnlyAsFunctionalHypothesisInputs=True,sourceCredit=0)
