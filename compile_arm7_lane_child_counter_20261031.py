from pathlib import Path
import match_arm7
import utility_code
import utility_runtime
import match_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json


def main():
    address=0x037FDDCC
    spec=next(row for row in utility_code.candidates() if row['module']=='utility-child-arm7-wram' and row['address']==address)
    source=ROOT/'nonmatching/arm7-bulk/20261031/lane-child-counter76/native_utility_child_arm7_wram_037fddcc.c'
    origin=dict(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),name='native_utility_child_arm7_wram_037fddcc')
    compiler=ROOT/'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe'
    flags=match_runtime.FLAGS[:]
    flags[flags.index('-proc')+1]='arm7tdmi'
    directory=ROOT/'work/arm7-bulk-20261030/lane-child-counter76/037fddcc'
    directory.mkdir(parents=True,exist_ok=True)
    match_runtime.WORK=directory/'isolated-runtime'
    attempt,compiled=crossreuse_utility_c.compile_origin(origin,compiler,flags,directory)
    if compiled is None:
        raise ValueError(attempt)
    derived,masks,body=compiled
    with (ROOT/derived['probeObject']).open('rb') as stream:
        elf=ELFFile(stream)
        symbol=next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name==origin['name'])
        section,offset=symbol['st_shndx'],symbol['st_value']
    raw=(ROOT/spec['binary']).read_bytes()
    original=raw[address-spec['base']:address-spec['base']+spec['bytes']]
    entry=dict(origin,program=utility_runtime.PROGRAM,processor='arm7',module='utility-child-arm7-wram',mode='arm',address=hex(address),bytes=spec['bytes'],
        binary=spec['binary'],base=spec['base'],inputModuleSha256=spec['inputModuleSha256'],targetSha256=match_arm7.sha(original),
        compiler=compiler.relative_to(ROOT).as_posix(),compilerSha256=sha256(compiler),compilerFlags=flags,
        object=derived['probeObject'],objectSha256=derived['probeObjectSha256'],sectionIndex=section,sectionOffset=offset,
        relocations=[dict(row,format='SHT_RELA',explicitAddend=row['addend'],originalEncodedWord=body[row['offset']:row['offset']+4].hex()) for row in derived['relocations']])
    proof=linker.validate(entry,directory/'link')
    write_json(directory/'report.json',dict(entry=entry,proof=proof,sourceCredit=0,compiledBytes=len(body)))
    print(dict(compiledBytes=len(body),exactLinkedBytes=proof['exactLinkedBytes'],sourceCredit=0))


if __name__=='__main__':
    main()
