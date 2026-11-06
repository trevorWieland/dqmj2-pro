from project import ROOT,sha256
import wave20261106_socl_continuation_next_twelfth_compiler as compiler
import link_runtime_unit as L
from recover_linked_runtime import qualified_bindings,relocation_only_candidate
from wave20261106_socl_continuation_next_twelfth_bindings import verify_original
from elftools.elf.elffile import ELFFile


import re


def dependencies(source):
    seen=set();pending=[source];root=source.parent.resolve()
    while pending:
        path=pending.pop().resolve()
        if path in seen:continue
        if not path.is_relative_to(root):raise ValueError('SDK include escaped selected unit')
        seen.add(path);text=path.read_text()
        if re.search(r'^\s*#\s*include\s*<',text,re.M):raise ValueError('Implicit system include in closed SDK source')
        pending.extend(path.parent/name for name in re.findall(r'^\s*#\s*include\s*"([^"<>]+)"',text,re.M))
    return [dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p)) for p in sorted(seen) if p!=source.resolve()]


def build(source, directory, negative=False):
    previous_work=compiler.C.WORK
    try:
        rows, unused = compiler.compare(source, directory / 'c')
    finally:compiler.C.WORK=previous_work
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('Caller compile failed', rows))
    row = rows[0]
    row.update(program='', sourceDependencies=dependencies(source))
    if not negative:relocation_only_candidate(row)
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
        if not any(s.name == '$t' and s['st_value'] == entry['st_value'] for s in symbols):
            raise ValueError('Genuine linked Thumb mapping absent')
    if L.relocation_rows(ROOT / row['object'], row['name']) != L.relocation_rows(directory / 'l/caller.o', row['name']):
        raise ValueError('Caller splitting changed original relocation payloads')
    row.update(nativeSymbolEntries=bindings, realLink=proof, compiler=row['compilerPath'])
    if not negative:row.update(prelinkMatchingBytes=row['matchingBytes'],prelinkExactAfterDeclaredRelocation=row['exactAfterDeclaredRelocation'],matchingBytes=row['bytes'],exactAfterDeclaredRelocation=True,outputSha256=sha256(directory/'l/caller.bin'),realLinkInterworkingRequired=True)
    return row, body

