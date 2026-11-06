from project import ROOT,sha256
import link_runtime_unit as L
from recover_linked_runtime import qualified_bindings
from elftools.elf.elffile import ELFFile
import wave20261106_game_main_arm_next_compiler as compiler
from wave20261106_game_main_arm_next_fifth_bindings import verify_original


def build(source,directory,negative=False):
    rows,unused=compiler.compare(source,directory/'c')
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError(('Caller compile failed',rows))
    row=rows[0];row.update(program='',sourceDependencies=[dict(path=source.with_name('initializer.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('initializer.h')))])
    bindings=qualified_bindings(row)
    if not negative:row['originalNamespaceWitnesses']=verify_original(row,bindings)
    try:proof=L.validate(row,bindings,directory/'l')
    except ValueError as error:
        if not negative or not error.args or not isinstance(error.args[0],dict):raise
        proof=dict(exactCallerBytes=False,comparison=error.args[0])
    if negative and proof['exactCallerBytes']:raise ValueError('Whole-C semantic error unexpectedly matched')
    body=(directory/'l/caller.bin').read_bytes()
    with (directory/'l/linked.elf').open('rb') as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());entry=next(s for s in symbols if s.name==row['name'])
        if entry['st_value']!=int(row['address'],0) or entry['st_size']!=row['compiledBytes'] or len(body)!=row['compiledBytes']:raise ValueError('Genuine linked caller boundary differs')
        if not any(s.name=='$a' and s['st_value']==entry['st_value'] for s in symbols):raise ValueError('Genuine linked ARM mapping absent')
    if L.relocation_rows(ROOT/row['object'],row['name'])!=L.relocation_rows(directory/'l/caller.o',row['name']):raise ValueError('Caller splitting changed original relocation payloads')
    row.update(nativeSymbolEntries=bindings,realLink=proof)
    return row,body
