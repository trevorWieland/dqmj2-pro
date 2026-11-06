import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path
import match_arm7_main_spi276_20261101 as compiler
import arm7_child_poll44_functional_native_20261101 as native
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-child-poll44-mask'
WORK=ROOT/'work/arm7-bulk-20261030/child-poll44-functional'
REPORT=ROOT/'evidence/arm7/child-poll44-functional-20261101.json'
PINS=ROOT/'nonmatching/arm7-bulk/20261101/lane-child-poll44-functional/generator-pins.json'


def main():
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Current bounded-poll hypothesis/runtime/input closure differs')
    seed=json.loads((SOURCE/'seed.json').read_text());row,comparison,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/'caller',strict=False);original=(ROOT/seed['binary']).read_bytes();own=original[native.ENTRY-native.BASE:native.ENTRY-native.BASE+44]
    if len(body)!=44 or comparison!=dict(nativeBytes=44,linkedBytes=44,matchingBytes=36):raise ValueError('Bounded poll inexactness changed; no automatic credit')
    directory=WORK/'caller/real-link';lcf=directory/'unit.lcf';obj=directory/'caller.o';output=directory/'functional.elf';linker=compiler.linker
    if sha256(linker.LINKER)!=linker.LINKER_HASH or linker.relocation_rows(ROOT/row['object'],row['name'])!=linker.relocation_rows(obj,row['name']):raise ValueError('Pinned linker or unchanged source relocations differ')
    argv=[str(linker.LINKER),'-nostdlib','-nodeadstrip','-interworking','-proc','arm7tdmi','-main',row['name'],str(lcf),str(obj),'-o',str(output)];result=subprocess.run(argv,cwd=directory,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode or(directory/'caller.bin').read_bytes()!=body:raise ValueError('Explicit real functional link failed')
    with output.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(x for x in elf.get_section_by_name('.symtab').iter_symbols()if x.name==row['name'])
        if symbol['st_value']!=native.ENTRY or symbol['st_size']!=44:raise ValueError('Actual functional link entry/size differs')
    records=[];visited=set();limits=0;counts=set()
    for index,case in enumerate(native.cases()):
        first=native.execute(original,own,case,index);second=native.execute(original,body,case,index)
        if first!=second or not first['modelPassed']:raise ValueError('Original/source bounded poll CPU/memory/read/flag model differs')
        records.append(dict(case=case,execution=first));visited.update(first['visited']);limits+=first['limitExhausted'];counts.add(first['readCount'])
    if len(records)!=346 or visited!=set(range(native.ENTRY,native.ENTRY+40,4))or max(counts)!=4000:raise ValueError('Full bounded poll case/code/read-cap domain differs')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/'records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),sourceCredit=0,pinnedInputs=pins,matchedByteCredit=0,functionMatched=False,wholeModuleMatched=False,sourceReconstructionComplete=False,identity=dict(processor='arm7',program=seed['program'],module=seed['module'],mode='arm',address=seed['address'],bytes=44),row=row,genuineNativeComparison=comparison,explicitRealLink=dict(linkerSha256=linker.LINKER_HASH,actualExecutedArgv=argv,actualCwd=str(directory),exitCode=result.returncode,linkedElf=output.relative_to(ROOT).as_posix(),linkedElfSha256=sha256(output),lcf=lcf.relative_to(ROOT).as_posix(),lcfSha256=sha256(lcf),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),linkedCodeSha256=hashlib.sha256(body).hexdigest(),unchangedEncodedRelocationsAndAddends=True,anchorsAndCalleeCredit=0),vectors=len(records),actualOriginalAndCompiledOwnReturns=2*len(records),actualNestedReturns=0,actualBoundExhaustedOuterReturns=2*limits,readCounts=sorted(counts),allOwnInstructionsVisited=True,fullRawRegistersFlagsAndOrderedReadsAndMappedFrameIoCompared=True,nonCodeRamComparisonExcludesOnlyOwned44ByteCodeInEvidenceCopy=True,initialInstructionOrderDiffers=True,physicalHardwareTimingProven=False,supportedPeripheralContract=dict(readBytes=2,address='0x480819c',testedMaximumReadCount=4000,rawReturnValues=[0,128],limitExhaustionIsAnActualReturnNotErrorClaim=True),sourceControlDomain=dict(noIncomingArguments=True,remainingInitialValue=4000,decrementOnlyAfterZeroMask=True,readyAssignedBeforeEveryFeasibleSourceRead=True,sourceReadDominanceReason='Entry initializes remaining to4000 and each reached loop assigns ready before either break or finite decrement to0; no feasible entry path skips all iterations',readDominanceDoesNotGeneralizeToOtherUninitializedDeclarations=True),trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0),limitations=['Only initial MOV/literal-LDR order differs;36/44 native bytes, zero source credit','Per-read supplied input contract does not prove physical timing or concurrent observers','No historical public return/error or scene meaning','No namespace/data-policy changes or assembly admission']);write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),actualOwnReturns=report['actualOriginalAndCompiledOwnReturns'],boundExhaustedReturns=report['actualBoundExhaustedOuterReturns'],sourceCredit=0)),flush=True)
if __name__=='__main__':main()
