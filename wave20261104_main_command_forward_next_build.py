from project import ROOT,sha256
import wave20261104_main_command_forward_compiler as compiler
import link_runtime_unit as L
from recover_linked_runtime import qualified_bindings
from wave20261104_main_command_forward_next_bindings import verify_original
from elftools.elf.elffile import ELFFile


def build(source, directory, negative=False):
    rows, unused = compiler.compare(source, directory / 'c')
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('Caller compile failed', rows))
    row = rows[0]
    row.update(program='', sourceDependencies=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))])
    if not negative and not row.get('exactAfterDeclaredRelocation'):
        raise ValueError(('C shape is unqualified', row.get('compiledBytes'), row.get('bytes'), row.get('matchingBytes')))
    bindings = qualified_bindings(row)
    if not negative:
        row['originalNamespaceWitnesses'] = verify_original(row, bindings)
    attempts=[]
    original_run=L.subprocess.run
    def observe(command,*args,**kwargs):
        process=original_run(command,*args,**kwargs)
        if command and str(command[0])==str(L.LINKER):
            attempts.append(dict(command=command,cwd=str(kwargs.get('cwd')),exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
        return process
    try:
        L.subprocess.run=observe
        try:
            proof=L.validate(row,bindings,directory/'l')
        except ValueError as error:
            if not negative or not error.args or not isinstance(error.args[0],dict):raise
            if len(attempts)!=1 or attempts[0]['exitCode']!=0:raise ValueError('Negative caller did not genuinely link successfully')
            proof=dict(exactCallerBytes=False,comparison=error.args[0],linkerAttempt=attempts[0],linkerSha256=L.LINKER_HASH)
    finally:
        L.subprocess.run=original_run
    if negative and proof['exactCallerBytes']:
        raise ValueError('Whole-C wrong status unexpectedly matched')
    body = (directory / 'l/caller.bin').read_bytes()
    with (directory / 'l/linked.elf').open('rb') as stream:
        elf = ELFFile(stream)
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        entry = next(s for s in symbols if s.name == row['name'])
        if entry['st_value'] != int(row['address'], 0) or entry['st_size'] != row['compiledBytes'] or len(body) != row['compiledBytes']:
            raise ValueError('Genuine linked caller boundary differs')
        if not any(s.name == '$a' and s['st_value'] == entry['st_value'] for s in symbols):
            raise ValueError('Genuine linked ARM mapping absent')
    if L.relocation_rows(ROOT / row['object'], row['name']) != L.relocation_rows(directory / 'l/caller.o', row['name']):
        raise ValueError('Caller splitting changed original relocation payloads')
    row.update(nativeSymbolEntries=bindings, realLink=proof, compiler=row['compilerPath'])
    return row, body

