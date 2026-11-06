import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path
import match_arm7_main_spi276_20261101 as compiler
import arm7_main_spi_write536_native_20261101 as native
from project import ROOT,sha256,write_json
from elftools.elf.elffile import ELFFile
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-main-spi-write536-functional'
WORK=ROOT/'work/arm7-bulk-20261030/spi-write536-functional'
REPORT=ROOT/'evidence/arm7/main-spi-write536-functional-20261101.json'
PINS=SOURCE/'generator-pins.json'

def real_link_receipt(row,directory,expected):
    linker=compiler.linker;directory=directory/'real-link';objects=[directory/'caller.o',*sorted(directory.glob('anchor*.o'))];lcf=directory/'unit.lcf';output=directory/'functional-linked.elf'
    if sha256(linker.LINKER)!=linker.LINKER_HASH:raise ValueError('Pinned linker differs')
    if linker.relocation_rows(ROOT/row['object'],row['name'])!=linker.relocation_rows(objects[0],row['name']):raise ValueError('Split object changed encoded relocations/addends')
    command=[str(linker.LINKER),'-nostdlib','-nodeadstrip','-interworking','-proc','arm7tdmi','-main',row['name'],str(lcf),*map(str,objects),'-o',str(output)]
    result=subprocess.run(command,cwd=directory,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode:raise ValueError('Explicit real functional link failed: '+result.stdout+result.stderr)
    with output.open('rb')as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());own=next(x for x in symbols if x.name==row['name']);section=elf.get_section(own['st_shndx']);body=(directory/'caller.bin').read_bytes()
        if own['st_value']!=int(row['address'],0)or own['st_size']!=268 or body!=expected:raise ValueError('Actual functional ELF code/address/size differs')
        target=next(x for x in symbols if x.name=='native_host_arm7_arm_027f54f0')
        if target['st_value']!=0x027f54f0 or target['st_size']!=0 or not any(x.name=='$a'and x['st_value']==0x027f54f0 for x in symbols):raise ValueError('Qualified zero-code ARM helper binding changed')
    anchor_bytes=0;anchor_reserved=0
    for anchor in objects[1:]:
        with anchor.open('rb')as stream:
            elf=ELFFile(stream)
            for section in elf.iter_sections():
                if section['sh_flags']&2:
                    if section['sh_type']!='SHT_NOBITS':anchor_bytes+=section['sh_size']
                    else:anchor_reserved+=section['sh_size']
        if anchor.with_suffix('.bin').exists()and anchor.with_suffix('.bin').stat().st_size:raise ValueError('Functional binding anchor acquired initialized bytes')
    if anchor_bytes:raise ValueError('Functional anchor contains initialized source/callee code')
    return dict(linker=linker.LINKER.relative_to(ROOT).as_posix(),linkerSha256=linker.LINKER_HASH,actualExecutedArgv=command,actualCwd=str(directory),exitCode=result.returncode,stdout=result.stdout,stderr=result.stderr,lcf=lcf.relative_to(ROOT).as_posix(),lcfSha256=sha256(lcf),objects=[dict(path=o.relative_to(ROOT).as_posix(),sha256=sha256(o))for o in objects],linkedElf=output.relative_to(ROOT).as_posix(),linkedElfSha256=sha256(output),compiledFunctionSha256=hashlib.sha256(body).hexdigest(),unchangedEncodedRelocationsAndAddends=True,helperIdentity=dict(processor='arm7',program='',module='arm7-main',mode='arm',address='0x27f54f0',bytes=36),zeroCodeAnchorBytes=anchor_bytes,anchorNobitsReservationBytes=anchor_reserved,elfExternalOutputSectionMetadata=dict(section=section.name,initializedSectionFileBytes=section['sh_size'],linkedSymbolBytes=268,actualLcfOutput='caller.bin'),sourceCredit=0)

def projection(value):
    fields=('rawResult','effectiveCount','signedLoopBound','transferredBytes','nested','rawRegisters','cpsr','nonCodeRamSha256','stackSha256','ioSha256','inputSha256','suppliedHalfwords')
    return dict({k:value[k]for k in fields},orderedPortWrites=[w for w in value['orderedWrites']if w[0]in(native.CONTROL,native.DATA)],orderedReads=value['orderedReads'])

def main():
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        p=(ROOT/item['path']).resolve()
        if not p.is_relative_to(ROOT)or not p.is_file()or sha256(p)!=item['sha256']:raise ValueError('Current writer hypothesis/runtime/input missing or changed')
    ownership=compiler.ownership();profile=json.loads((SOURCE/'profile.json').read_text());dep=profile['existingSourceDependency'];old,old_link,helper=compiler.compile_unit(dep,ROOT/dep['source'],WORK/'helper');original=(ROOT/dep['binary']).read_bytes();native_helper=original[native.HELPER-native.BASE:native.HELPER-native.BASE+36];results=[]
    if helper!=native_helper:raise ValueError('Fresh existing helper does not match')
    for seed in profile['units']:
        row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/seed['address'][2:],strict=False);entry=int(seed['address'],0);own=original[entry-native.BASE:entry-native.BASE+268]
        if len(body)!=268 or body==own or link['matchingBytes']!=252:raise ValueError('Frozen inexact writer comparison changed; no automatic match promotion')
        receipt=real_link_receipt(row,WORK/seed['address'][2:],body);records=[];original_visits=set();source_visits=set();frame_order_differences=0;helper_returns=0;counts=[]
        for index,case in enumerate(native.cases()):
            first=native.execute(original,entry,own,native_helper,case,index);second=native.execute(original,entry,body,helper,case,index)
            if not first['functionalModelPassed']or not first['nativeStackWriteOrderPassed']or not second['functionalModelPassed']or projection(first)!=projection(second):raise ValueError('Original/typed source supported functional domain differs')
            frame_order_differences+=first['orderedWrites']!=second['orderedWrites'];helper_returns+=first['actualNestedReturns']+second['actualNestedReturns'];original_visits.update(first['visitedOwn']);source_visits.update(second['visitedOwn']);counts.append(first['transferredBytes']);records.append(dict(case=case,original=first,source=second))
        if len(records)!=652 or helper_returns!=1232 or original_visits!=set(range(entry,entry+260,4))or source_visits!=set(range(entry,entry+260,4)):raise ValueError('Complete supported writer code/case/return scope differs')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/seed['address'][2:]/'records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));unsupported=[]
        for phase in range(9):
            base=next(x for x in native.cases()if x['address']==0 and x['count']==4);case=dict(base,stuck=phase);first=native.execute(original,entry,own,native_helper,case,0,budget=2000,allow_no_return=True);second=native.execute(original,entry,body,helper,case,0,budget=2000,allow_no_return=True)
            if first!=second or first['actualOwnReturn']or not first['stuckPhaseReached']:raise ValueError('Writer busy phase did not produce equal bounded nonreturn')
            unsupported.append(dict(phase=phase,execution=first,postStateCredit=0,supportedErrorPathCredit=0))
        row.update(genuineLink=link,explicitRealLink=receipt,compiledCompleteBytes=268,exactByteMatch=False,functionMatched=False,sourceCredit=0,matchedByteCredit=0,providerReplacements=[],supportedVectors=652,actualOriginalAndCompiledOwnReturns=1304,existingSourceHelperReturnsSeparateZeroCredit=1232,sourcePrivateFrameWriteOrderDifferences=frame_order_differences,maximumSupportedTransferredBytes=max(counts),rawRegistersAndFlagsCompared=True,entireMainRamComparedAfterExcludingOnlyChangedCallerCodeRange=True,orderedPortWritesAndAllReadsCompared=True,finalPrivateFrameAndAllInputIoBytesCompared=True,privateFrameStoreOrderExcludedOnlyFromFunctionalProjection=True,noConcurrencyOrInterruptObserverClaim=True,unsupported=unsupported,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0));results.append(row)
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),sourceCredit=0,matchedByteCredit=0,functionMatched=False,wholeModuleMatched=False,romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',results=results,existingSourceHelper=dict(old,realLink=old_link,sourceCredit=0,byteCredit=0),runtimeOwnership=ownership,pinnedInputs=pins,totalActualOwnReturns=2608,totalExistingSourceHelperReturnsSeparateZeroCredit=2464,fullRawMachineEquivalenceClaim=False,conditionalSemantics=dict(clamp='Unsigned wrapped(address+count-1)>>8 greater than address>>8 clamps to u16(256-lowByte)',streamLoop='Signed32(effectiveCount-1); negative bound skips intermediate bytes but still transmits input0',countZero='Returns full input word and touches no ports'),limitations=['Original-code bytes differ252/268; not accepted reconstructed source','Private stack-store order differs after first supported step; no asynchronous observer/concurrency equivalence claim','Input page capacity and finite polls are synthetic supported preconditions','No physical chip/address-policy, completion, scene or portability inference'])
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),ownReturns=2608,helperReturnsSeparate=2464,sourceCredit=0)),flush=True)
if __name__=='__main__':main()
