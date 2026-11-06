import json
from pathlib import Path
import match_arm7
import match_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json


def main():
    source=ROOT/'src/arm7/lane_20261031_word_dispatch92/native_arm7_main_027f6ec0.c'
    address=0x027F6EC0
    spec=next(row for row in match_arm7.candidates(1000000) if row['module']=='arm7-main' and row['address']==address)
    accepted=ROOT/'evidence/verification/accepted-cohort68-identities-20261031.json'
    for row in json.loads(accepted.read_text())['functions']:
        if row['program']=='' and row['processor']=='arm7' and row['module']=='arm7-main':
            first=int(row['address'],0)
            if first<address+92 and address<first+row['bytes']:
                raise ValueError('Fresh accepted identity overlaps prospective92-byte source')
    flags=match_runtime.FLAGS[:]
    flags[0]='-O2'
    flags[flags.index('-proc')+1]='arm7tdmi'
    flags[flags.index('-inline')+1]='all'
    flags+=['-ipa','file','-lang','c99','-opt','space']
    compiler=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
    directory=ROOT/'work/arm7-bulk-20261030/lane-word-dispatch92-prepare'
    directory.mkdir(parents=True,exist_ok=True)
    match_runtime.WORK=directory/'isolated-runtime'
    origin=dict(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),name='native_arm7_main_027f6ec0')
    attempt,compiled=crossreuse_utility_c.compile_origin(origin,compiler,flags,directory)
    if compiled is None:
        raise ValueError(attempt)
    derived,masks,body=compiled
    binary=ROOT/spec['binary']
    original=binary.read_bytes()[address-spec['base']:address-spec['base']+92]
    with (ROOT/derived['probeObject']).open('rb') as stream:
        elf=ELFFile(stream)
        own=next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name==origin['name'])
        section,offset=own['st_shndx'],own['st_value']
    pin=dict(origin,program='',processor='arm7',module='arm7-main',mode='arm',address=hex(address),bytes=92,codeBytes=92,
        binary=spec['binary'],base=spec['base'],inputModuleSha256=sha256(binary),targetSha256=linker.digest(original),
        compiler=compiler.relative_to(ROOT).as_posix(),compilerSha256=sha256(compiler),compilerFlags=flags,sourceDependencies=[])
    entry=dict(pin,object=derived['probeObject'],objectSha256=derived['probeObjectSha256'],sectionIndex=section,sectionOffset=offset,
        relocations=[dict(row,format='SHT_RELA',explicitAddend=row['addend'],originalEncodedWord=body[row['offset']:row['offset']+4].hex()) for row in derived['relocations']])
    proof=linker.validate(entry,directory/'real-link')
    destination=ROOT/'nonmatching/arm7-bulk/20261031/lane-word-dispatch92-final/closure.json'
    write_json(destination,dict(matches=[pin],acceptedIdentityExport=dict(path=accepted.relative_to(ROOT).as_posix(),sha256=sha256(accepted),overlap=False),
        preparer=Path(__file__).name,preparerSha256=sha256(__file__),currentSourceCredit=0))
    write_json(directory/'prepare.json',dict(entry=entry,realArm7Link=proof,sourceCredit=0))
    print(json.dumps(dict(profile=destination.relative_to(ROOT).as_posix(),sha256=sha256(destination),compiledBytes=len(body),
        exactLinkedBytes=proof['exactLinkedBytes'],sourceCredit=0)))


if __name__=='__main__':
    main()
