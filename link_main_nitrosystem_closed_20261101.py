import concurrent.futures
from pathlib import Path
import match_runtime
from elftools.elf.elffile import ELFFile
import link_main_nitrosystem_breadth_20261101 as linker
from link_runtime_unit import relocation_rows,measured_module
from project import ROOT,read_json,write_json,sha256

INPUT=ROOT/'work/main-nitrosystem-closed-20261101/report.json'
WORK=ROOT/'work/main-nitrosystem-closed-links-20261101'


def main():
    assert not (WORK/'report.json').exists()
    originals={}
    for row in read_json(ROOT/'work/main-nitrosystem-links-20261101/report.json')['results']:
        if row['genuineLinkedExact']:originals.setdefault(row['identity']['address'],row)
    queue=[]
    for closed in read_json(INPUT)['results']:
        if closed.get('exitCode')!=0:continue
        row=dict(originals[closed['identity']['address']]);row.update(referenceSource=closed['source'],
            sourceSha256=closed['sourceSha256'],object=closed['object'],objectSha256=closed['objectSha256'],
            compilerFlags=closed['compilerFlags'],profile=row['profile']+'-closed')
        relocations=relocation_rows(ROOT/closed['object'],closed['referenceFunction'])
        with(ROOT/closed['object']).open('rb')as stream:
            elf=ELFFile(stream);symbols={symbol.name:symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols()}
            for relocation in relocations:
                symbol=symbols[relocation['symbol']]
                relocation.update(sourceSymbolType=symbol['st_info']['type'],sourceSymbolBinding=symbol['st_info']['bind'],sourceSymbolSection=symbol['st_shndx'])
        row['relocations']=relocations;queue.append(row)
    linker.WORK=WORK;functions=linker.namespace();metadata,image,_=measured_module('main')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
        results=list(pool.map(linker.link,[(index,row,functions,image)for index,row in enumerate(queue)]))
    exact=[row for row in results if row['genuineLinkedExact']]
    write_json(WORK/'report.json',dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),
        inputSha256=sha256(INPUT),sourceCredit=0,results=results,headerInputs=0,unchangedNormalArm9LinkerPolicy=True,
        genuineClosedCandidateFunctions=len(exact),genuineClosedCandidateInitializedBytes=sum(row['identity']['bytes']for row in exact),
        actualTypeCallerBoundaryAndNativeProofsStillRequired=True))
    print(dict(closedCandidates=len(queue),genuineExactFunctions=len(exact),
        candidateBytes=sum(row['identity']['bytes']for row in exact),sourceCredit=0))


if __name__=='__main__':
    main()
