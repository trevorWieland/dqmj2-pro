import ast
from pathlib import Path
import match_runtime
import crossreuse_utility_c
import recover_linked_runtime
import link_runtime_unit
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256


def build(pin,directory,strict=True):
    directory=(ROOT/directory).resolve()
    if not directory.is_relative_to(ROOT):raise ValueError('Heap compile directory escapes repository')
    directory.mkdir(parents=True,exist_ok=True)
    for item in [dict(path=pin['source'],sha256=pin['sourceSha256']),*pin['sourceDependencies']]:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or sha256(path)!=item['sha256']:
            raise ValueError('Current heap source/include closure differs')
        source=path.read_text()
        if len(source.splitlines())>500 or '/*'in source or '//'in source:
            raise ValueError('Heap source policy differs')
    compiler=ROOT/pin['compiler']
    if sha256(compiler)!=pin['compilerSha256']:raise ValueError('Pinned heap compiler differs')
    match_runtime.WORK=directory/'isolated-compiler'
    attempt,compiled=crossreuse_utility_c.compile_origin(pin,compiler,pin['compilerFlags'],directory)
    if compiled is None:raise ValueError('Heap C did not compile: '+str(attempt))
    derived,unused,body=compiled
    with(ROOT/derived['probeObject']).open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==pin['name'])
        section,offset=symbol['st_shndx'],symbol['st_value']&~1
    entry=dict(pin,object=derived['probeObject'],objectSha256=derived['probeObjectSha256'],sectionIndex=section,sectionOffset=offset,
        compiledBytes=len(body),relocations=[dict(row,target=hex(match_runtime.symbol_address(row['symbol'])),format='SHT_RELA',
            explicitAddend=row['addend'],originalEncodedWord=body[row['offset']:row['offset']+4].hex())for row in derived['relocations']])
    bindings=recover_linked_runtime.qualified_bindings(entry);mismatch=None;proof=None
    try:proof=link_runtime_unit.validate(entry,bindings,directory/'genuine-link')
    except ValueError as error:
        try:mismatch=ast.literal_eval(str(error))
        except(ValueError,SyntaxError):raise error
        if not isinstance(mismatch,dict)or mismatch.get('caller')!=pin['name']or 'matchingBytes'not in mismatch:raise error
        if strict:raise error
    linked=directory/'genuine-link/caller.bin'
    if not linked.is_file():raise ValueError('Fresh genuine heap linked body missing')
    code=linked.read_bytes()
    if len(code)!=len(body):raise ValueError('Fresh compiler/linker heap body sizes differ')
    return entry,bindings,proof,mismatch,code
