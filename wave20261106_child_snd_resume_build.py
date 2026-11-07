import utility_runtime
import wave20261102_child_link as legacy
from elftools.elf.elffile import ELFFile
from link_runtime_unit import LINKER,LINKER_HASH,relocation_rows
from project import ROOT,sha256
from wave20261106_child_snd_resume_paths import assert_compile
from wave20261106_child_snd_resume_compiler import compare
from wave20261106_child_snd_resume_bindings import qualify
from wave20261106_child_snd_resume_embedded import link as embedded_link


def build(source,directory,negative=False):
    assert_compile(source,directory);row,unused=compare(source,directory/'c')
    if row.get('compileFailed'):raise ValueError(('Actual typed SND caller failed compile',row))
    if not negative and(row['compiledBytes']!=196 or not row['exactAfterDeclaredRelocation']):raise ValueError('Full original source caller did not match')
    canonical,bindings,witnesses=qualify(row);old_lookup=legacy.canonical;old_run=legacy.subprocess.run;attempts=[]
    def observe(command,*args,**kwargs):
        process=old_run(command,*args,**kwargs)
        if command and str(command[0])==str(LINKER):attempts.append(dict(command=command,cwd=str(kwargs.get('cwd')),exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
        return process
    try:
        legacy.canonical=lambda:canonical;legacy.subprocess.run=observe
        try:proof=legacy.validate(row,directory/'l')
        except ValueError as error:
            if not negative or len(attempts)!=1 or attempts[0]['exitCode']!=0 or not error.args or not isinstance(error.args[0],dict)or error.args[0].get('equal')is not False:raise
            proof=dict(exactCallerBytes=False,comparison=error.args[0],linkerAttempt=attempts[0],linkerSha256=LINKER_HASH)
    finally:legacy.canonical=old_lookup;legacy.subprocess.run=old_run
    flat=(directory/'l/caller.bin').read_bytes();proof=embedded_link(row,proof,directory/'l',flat)
    for object_path in[ROOT/row['object'],directory/'l/caller.o']:
        with object_path.open('rb')as stream:
            elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==row['name']);section=elf.get_section(symbol['st_shndx'])
            if(symbol['st_info']['type'],symbol['st_size'],section['sh_type'],section['sh_flags'])!=('STT_FUNC',row['compiledBytes'],'SHT_PROGBITS',6):raise ValueError('Actual original/split executable source function contract differs')
    if relocation_rows(ROOT/row['object'],row['name'])!=relocation_rows(directory/'l/caller.o',row['name']):raise ValueError('Actual source relocation types/addends/words changed')
    if negative and proof['exactCallerBytes']:raise ValueError('Wrong source remained exact')
    row.update(nativeSymbolEntries=bindings,realLink=proof,originalNamespaceWitnesses=dict(witnesses=witnesses,programCpuModuleModeAndOriginalBranchesChecked=True,calleeCodeAndStorageCredit=0))
    return row,flat
