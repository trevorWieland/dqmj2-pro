import argparse
import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path
import match_runtime
import crossreuse_utility_c
import qualified_arm7_card_scope_20261031 as qualified
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json
PROFILE=ROOT/'nonmatching/arm7-bulk/20261031/lane-card-abi16-1252-final/closure.json'
WORK=ROOT/'work/arm7-bulk-20261030/lane-card-abi16-1252'


def worker(address):
    pin=next(row for row in json.loads(PROFILE.read_text())['matches'] if int(row['address'],0)==address)
    directory=WORK/f'{address:08x}';directory.mkdir(parents=True,exist_ok=True)
    match_runtime.WORK=directory/'isolated-runtime'
    for item in [dict(path=pin['source'],sha256=pin['sourceSha256']),*pin['sourceDependencies']]:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Shared source closure differs')
    attempt,compiled=crossreuse_utility_c.compile_origin(pin,ROOT/pin['compiler'],pin['compilerFlags'],directory)
    row=dict(address=pin['address'],sourceSha256=pin['sourceSha256'],attempt=attempt,sourceCredit=0)
    if compiled:
        derived,masks,body=compiled;row['compiledBytes']=len(body)
        raw=(ROOT/pin['binary']).read_bytes();native=raw[address-pin['base']:address-pin['base']+pin['bytes']]
        covered={offset+i for offset,unused in masks for i in range(4)}
        row['matchingOutsideRelocations']=sum(body[i]==native[i] for i in range(min(len(body),len(native))) if i not in covered)
        row['comparableBytes']=sum(i not in covered for i in range(min(len(body),len(native))))
        if len(body)==pin['bytes'] and row['matchingOutsideRelocations']==row['comparableBytes']:
            with (ROOT/derived['probeObject']).open('rb') as stream:
                elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name==pin['name'])
                section,offset=symbol['st_shndx'],symbol['st_value']
            entry=dict(pin,object=derived['probeObject'],objectSha256=derived['probeObjectSha256'],sectionIndex=section,sectionOffset=offset,
                relocations=[dict(r,format='SHT_RELA',explicitAddend=r['addend'],originalEncodedWord=body[r['offset']:r['offset']+4].hex()) for r in derived['relocations']])
            row['entry']=entry
            try:row['realLink']=qualified.validate(entry,directory/'real-link')
            except Exception as error:row['linkFailure']=str(error)
    write_json(directory/'report.json',row)


def invoke(address):
    directory=WORK/f'{address:08x}';directory.mkdir(parents=True,exist_ok=True)
    result=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker',hex(address)],cwd=ROOT,capture_output=True,text=True,timeout=300)
    (directory/'worker.stdout.txt').write_text(result.stdout,encoding='utf-8');(directory/'worker.stderr.txt').write_text(result.stderr,encoding='utf-8')
    if result.returncode:return dict(address=hex(address),failure=result.stderr,sourceCredit=0)
    return json.loads((directory/'report.json').read_text())


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',type=lambda x:int(x,0));args=parser.parse_args()
    if args.worker is not None:worker(args.worker);return
    addresses=[int(row['address'],0) for row in json.loads(PROFILE.read_text())['matches']]
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for row in pool.map(invoke,addresses):
            results.append(row);print(json.dumps(dict(address=row['address'],compiled=row.get('compiledBytes'),exact=row.get('realLink',{}).get('exactLinkedBytes'),failure=row.get('failure',row.get('linkFailure')))),flush=True)
    write_json(WORK/'report.json',dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),profileSha256=sha256(PROFILE),results=results,sourceCredit=0))


if __name__=='__main__':main()
