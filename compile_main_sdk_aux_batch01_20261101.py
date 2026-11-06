import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import match_runtime
import crossreuse_utility_c
import recover_linked_runtime
import link_runtime_unit
from elftools.elf.elffile import ELFFile
from project import ROOT,write_json

WORK=ROOT/'work/main-sdk-aux/20261101/batch01'
PROFILE=ROOT/'nonmatching/main-sdk-aux/20261101/batch01/source-queue.json'
TYPED=PROFILE.with_name('typed-lock-pair-profile.json')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def candidates():
    return [dict(row,variant=variant)for path,variant in [(PROFILE,'raw'),(TYPED,'typed-lock')]
        for row in json.loads(path.read_text())['matches']]


def build(pin,directory):
    directory.mkdir(parents=True,exist_ok=True)
    for row in [dict(path=pin['source'],sha256=pin['sourceSha256']),*pin['sourceDependencies']]:
        path=(ROOT/row['path']).resolve()
        if not path.is_relative_to(ROOT)or digest(path.read_bytes())!=row['sha256']:
            raise ValueError('Fresh SDK source/include changed')
        text=path.read_text()
        if len(text.splitlines())>500 or '/*'in text or '//'in text:
            raise ValueError('SDK candidate must be bounded comment-free ordinary C')
    compiler=ROOT/pin['compiler']
    if digest(compiler.read_bytes())!=pin['compilerSha256']:
        raise ValueError('Pinned main SDK compiler differs')
    match_runtime.WORK=directory/'isolated-compiler'
    attempt,compiled=crossreuse_utility_c.compile_origin(pin,compiler,pin['compilerFlags'],directory)
    if compiled is None:
        return {'identity':pin,'compilable':False,'attempt':attempt,'sourceCredit':0}
    derived,masks,body=compiled
    if len(body)!=pin['bytes']:
        return {'identity':pin,'compilable':True,'compiledBytes':len(body),'fullLinkedExact':False,'sourceCredit':0}
    with (ROOT/derived['probeObject']).open('rb')as stream:
        elf=ELFFile(stream)
        symbol=next(item for item in elf.get_section_by_name('.symtab').iter_symbols()if item.name==pin['name'])
        section,offset=symbol['st_shndx'],symbol['st_value']&~1
    entry=dict(pin,object=derived['probeObject'],objectSha256=derived['probeObjectSha256'],sectionIndex=section,sectionOffset=offset,
        relocations=[dict(row,target=hex(match_runtime.symbol_address(row['symbol'])),format='SHT_RELA',explicitAddend=row['addend'],
            originalEncodedWord=body[row['offset']:row['offset']+4].hex())for row in derived['relocations']],
        sourceLanguage='C',originalObjectScaffolding=False,nativeCalleeSourceCredit=0,wholeModuleLinked=False)
    bindings=recover_linked_runtime.qualified_bindings(entry)
    try:
        proof=link_runtime_unit.validate(entry,bindings,directory/'genuine-link')
    except ValueError as error:
        return {'identity':pin,'entry':entry,'compilable':True,'compiledBytes':len(body),'fullLinkedExact':False,
            'linkFailure':str(error),'sourceCredit':0}
    return {'identity':pin,'entry':entry,'compilable':True,'compiledBytes':len(body),'fullLinkedExact':proof['exactCallerBytes'],
        'realMainLink':proof,'qualifiedBindings':bindings,'sourceCredit':0,'independentNativeAbiAndStateProofStillRequired':True}


def worker(index):
    pin=candidates()[index]
    directory=WORK/(pin['variant']+'-'+pin['address'])
    result=build(pin,directory)
    write_json(directory/'compile.json',result)


def invoke(index,pin):
    directory=WORK/(pin['variant']+'-'+pin['address']);directory.mkdir(parents=True,exist_ok=True)
    command=[sys.executable,str(Path(__file__).resolve()),'--worker',str(index)]
    process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=180)
    (directory/'stdout.txt').write_text(process.stdout);(directory/'stderr.txt').write_text(process.stderr)
    if process.returncode:
        raise ValueError(process.stderr)
    return json.loads((directory/'compile.json').read_text())


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',type=int);options=parser.parse_args()
    if options.worker is not None:
        worker(options.worker);return
    rows=candidates()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
        futures=[pool.submit(invoke,index,row)for index,row in enumerate(rows)]
        results=[future.result()for future in futures]
    write_json(WORK/'compile-results.json',{'generator':Path(__file__).name,'generatorSha256':digest(Path(__file__).read_bytes()),
        'candidateDefinitions':len(rows),'uniqueNativeFunctions':4,'uniqueNativeBytes':500,'compilerSubprocesses':3,'results':results,
        'drafted':len(rows),'compilable':sum(row['compilable']for row in results),'genuinelyLinkedExact':sum(row['fullLinkedExact']for row in results),
        'sourceCredit':0,'acceptedSourceOrSharedStateChanged':False})
    print(json.dumps({'drafted':len(rows),'compilable':sum(row['compilable']for row in results),
        'genuinelyLinkedExact':sum(row['fullLinkedExact']for row in results),'uniqueNativeBytes':500,'sourceCredit':0}),flush=True)


if __name__=='__main__':
    main()
