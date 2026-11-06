import argparse
import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path
import match_arm7
import match_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
import qualified_arm7_card_scope_20261031 as qualified
import re
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261031/lane-card-frontier988-v3'
WORK=ROOT/'work/arm7-bulk-20261030/lane-card-frontier988-v3'
ADDRESSES=(0x03802e0c,0x03802f04,0x03802ffc,0x038032b8)


def worker(address):
    from prove_arm7_lane_card_callbacks_scope_20261031 import select
    sizes={0x03802e0c:156,0x03802f04:152,0x03802ffc:116,0x038032b8:564}
    binary='extract/arm7/runtime/arm7-wram.bin'
    if address<0x038029d8:select((ROOT/binary).read_bytes(),address,'arm',sizes[address])
    spec=dict(module='arm7-wram',address=address,bytes=sizes[address],base=0x037f8000,binary=binary,originalScopeOnly=True)
    accepted=ROOT/'evidence/verification/accepted-cohort80-identities-20261031.json'
    if any(row['processor']=='arm7' and not row['program'] and row['module']=='arm7-wram'
        and int(str(row['address']),0)<address+spec['bytes'] and address<int(str(row['address']),0)+row['bytes']
        for row in json.loads(accepted.read_text())['functions']):
        raise ValueError('Prospective channel source overlaps current accepted identities')
    source=SOURCE/f'native_arm7_wram_{address:08x}.c'
    origin=dict(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),name=source.stem)
    binary=ROOT/spec['binary']
    native=binary.read_bytes()[address-spec['base']:address-spec['base']+spec['bytes']]
    outcomes=[]
    for version,level in (('base',2),('base',3),('base',4),('sp1p5',2)):
        flags=match_runtime.FLAGS[:]
        flags[0]='-O'+str(level)
        flags[flags.index('-proc')+1]='arm7tdmi'
        flags[flags.index('-inline')+1]='all'
        flags+=['-ipa','file','-lang','c99','-opt','space','-gccext,on']
        compiler=ROOT/f'tools/mwccarm/mwccarm/2.0/{version}/mwccarm.exe'
        directory=WORK/f'{address:08x}'/f'{version}-O{level}-space'
        directory.mkdir(parents=True,exist_ok=True)
        match_runtime.WORK=directory/'isolated-runtime'
        attempt,compiled=crossreuse_utility_c.compile_origin(origin,compiler,flags,directory)
        row=dict(compiler=compiler.relative_to(ROOT).as_posix(),compilerSha256=sha256(compiler),compilerFlags=flags,attempt=attempt,sourceCredit=0)
        if compiled:
            derived,masks,body=compiled
            covered={offset+i for offset,unused in masks for i in range(4)}
            compared=[i for i in range(min(len(body),len(native))) if i not in covered]
            exact=len(body)==len(native) and all(body[i]==native[i] for i in compared)
            row.update(compiledBytes=len(body),matchingOutsideRelocations=sum(body[i]==native[i] for i in compared),
                comparableBytes=len(compared),relocationOnlyCandidate=exact,derived=derived)
            if exact:
                with (ROOT/derived['probeObject']).open('rb') as stream:
                    elf=ELFFile(stream)
                    symbol=next(item for item in elf.get_section_by_name('.symtab').iter_symbols() if item.name==origin['name'])
                    section,offset=symbol['st_shndx'],symbol['st_value']
                entry=dict(origin,program='',processor='arm7',module='arm7-wram',mode='arm',address=hex(address),bytes=spec['bytes'],
                    sourceDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p)) for p in SOURCE.glob('*.h')],
                    binary=spec['binary'],base=spec['base'],inputModuleSha256=sha256(binary),targetSha256=linker.digest(native),
                    compiler=compiler.relative_to(ROOT).as_posix(),compilerSha256=sha256(compiler),compilerFlags=flags,
                    object=derived['probeObject'],objectSha256=derived['probeObjectSha256'],sectionIndex=section,sectionOffset=offset,
                    relocations=[dict(item,format='SHT_RELA',explicitAddend=item['addend'],originalEncodedWord=body[item['offset']:item['offset']+4].hex()) for item in derived['relocations']])
                row['entry']=entry
                try:
                    entry['qualifiedCanonicalScope']=dict(qualified.REFERENCE)
                    row['realLink']=qualified.validate(entry,directory/'real-link')
                except Exception as error:
                    row['linkFailure']=str(error)
        outcomes.append(row)
    result=dict(address=hex(address),bytes=spec['bytes'],source=origin,outcomes=outcomes,acceptedExportSha256=sha256(accepted),
        drafted=True,compilable=any('compiledBytes' in row for row in outcomes),
        genuineExactCandidates=sum(row.get('realLink',{}).get('exactLinkedBytes',False) for row in outcomes),sourceCredit=0)
    write_json(WORK/f'{address:08x}'/'report.json',result)


def invoke(address):
    directory=WORK/f'{address:08x}'
    directory.mkdir(parents=True,exist_ok=True)
    process=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker',hex(address)],cwd=ROOT,capture_output=True,text=True,timeout=300)
    (directory/'worker.stdout.txt').write_text(process.stdout)
    (directory/'worker.stderr.txt').write_text(process.stderr)
    if process.returncode:
        return dict(address=hex(address),failure=process.stderr,sourceCredit=0)
    return json.loads((directory/'report.json').read_text())


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--worker',type=lambda value:int(value,0))
    args=parser.parse_args()
    if args.worker is not None:
        worker(args.worker)
        return
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(invoke,ADDRESSES):
            results.append(result)
            print(json.dumps(dict(address=result['address'],drafted=result.get('drafted'),compilable=result.get('compilable'),
                genuineExactProfiles=result.get('genuineExactCandidates'),failure=result.get('failure'))),flush=True)
    write_json(WORK/'report.json',dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),results=results,
        hypothesisFunctions=len(ADDRESSES),nativeBytes=988,sourceCredit=0,
        limitation='Three ordinary C hypotheses compile independently under bounded profiles; exact unit candidates still require complete native/ABI/boundary/control proofs'))


if __name__=='__main__':
    main()
