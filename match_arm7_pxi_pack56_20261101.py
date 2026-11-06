import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import match_runtime
import link_arm7_bulk_20261030 as linker
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256,write_json
import arm7_pxi_pair152_native_20261101 as native
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-pxi-pack56-final'
WORK=ROOT/'work/arm7-bulk-20261030/lane-pxi-pack56-final'
REPORT=ROOT/'evidence/matches/arm7-pxi-pack56-20261101.json'
PINS=SOURCE/'generator-pins.json'
def compile_unit(seed,source,directory,strict=True):
    directory.mkdir(parents=True,exist_ok=True);obj=directory/'compiled.o';compiler=ROOT/seed['compiler']
    if sha256(compiler)!=seed['compilerSha256']:raise ValueError('Compiler differs')
    for dep in seed['sourceDependencies']:
        if sha256(ROOT/dep['path'])!=dep['sha256']:raise ValueError('Complete declared header differs')
    flags=seed['compilerFlags'];argv=[str(compiler),*flags,'-c',str(source),'-o',str(obj)]
    result=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode:raise ValueError(result.stdout+result.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==seed['name']);start=symbol['st_value']&~1;size=symbol['st_size'];body=elf.get_section(symbol['st_shndx']).data()[start:start+size];relocations=[]
        for section in elf.iter_sections():
            if section['sh_type']not in('SHT_REL','SHT_RELA')or section['sh_info']!=symbol['st_shndx']:continue
            symbols=elf.get_section(section['sh_link'])
            for rel in section.iter_relocations():
                offset=rel['r_offset']-start
                if 0<=offset<size:relocations.append(dict(offset=offset,type=rel['r_info_type'],symbol=symbols.get_symbol(rel['r_info_sym']).name,format=section['sh_type'],explicitAddend=rel['r_addend']if section['sh_type']=='SHT_RELA'else None,originalEncodedWord=body[offset:offset+4].hex()))
    row=dict(seed,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),compiledBytes=size,relocations=relocations,object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),sectionIndex=symbol['st_shndx'],sectionOffset=start,command=argv,cwd=str(ROOT),exitCode=0,stdout=result.stdout,stderr=result.stderr)
    try:link=linker.validate(row,directory/'real-link')
    except ValueError as error:
        import ast
        if strict:raise
        link=ast.literal_eval(str(error))
        if not isinstance(link,dict)or not all(k in link for k in('nativeBytes','linkedBytes','matchingBytes')):raise ValueError('Unqualified wrong-source linker failure')
    return row,link,(directory/'real-link/caller.bin').read_bytes()
def main():
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Required typed PXI source/runtime/module/reference differs')
    profile=json.loads((SOURCE/'profile.json').read_text());units=[]
    for key in('newUnit','existingSelectedSourceDependency'):
        seed=profile[key];units.append(compile_unit(seed,ROOT/seed['source'],WORK/key))
    row,link,body=units[0];old,old_link,old_body=units[1];original=(ROOT/row['binary']).read_bytes();own=original[0x6410:0x6448];send=original[0x6448:0x64a8]
    rebuilt=bytearray(original);rebuilt[0x6410:0x6448]=body;rebuilt[0x6448:0x64a8]=old_body
    if bytes(rebuilt)!=original:raise ValueError('Complete fresh new and existing-source closure differs')
    records=[];visited={};invariant={}
    for case in native.cases():
        first=native.execute(original,own,send,case);second=native.execute(original,body,old_body,case)
        if first!=second or not first['modelPassed']:raise ValueError('Original/fresh source closure raw state or independent packed/status/stack/port model differs')
        projection=dict(first,orderedWrites=first['orderedWrites'][1:]);key=(case['group'],case['state'])
        if key in invariant and invariant[key]!=projection:raise ValueError('Incoming R3 changed final machine state or post-padding effects')
        invariant[key]=projection;records.append(dict(case=case,execution=first))
        for name,addresses in first['visited'].items():visited.setdefault(name,set()).update(addresses)
    expected={hex(native.ENTRY):set(range(native.ENTRY,native.ENTRY+56,4)),hex(native.SENDER):set(range(native.SENDER,native.SENDER+92,4)),hex(native.DISABLE):set(range(native.DISABLE,native.DISABLE+20,4)),hex(native.RESTORE):set(range(native.RESTORE,native.RESTORE+24,4))}
    if visited!=expected or len(records)!=1536 or len(invariant)!=384:raise ValueError('Complete own/dependency/branch/R3 coverage differs')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));trace_info=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)
    unsupported=[]
    for p,s in[(own,send),(body,old_body)]:
        value=native.execute(original,p,s,native.cases()[0],budget=1,allow_no_return=True)
        if value['actualOuterReturn']or value['actualNestedReturns']:raise ValueError('Prefix acquired a return')
        unsupported.append(value)
    symbols={name:hex(int(value['address'],0))for name,value in link['bindings'].items()}
    row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols=symbols,nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,
        sourceAbiContract=dict(physicalArgumentWords=3,fullyAssignedBitfieldsBeforeWordRead=True,compatibleWordMessageClosure=True,semanticFourthArgumentRequired=False,nativeTransientScratchR3ReadRecorded=True),
        oracle=dict(vectors=1536,actualOriginalAndCompiledReturns=3072,actualOuterReturns=3072,existingSourceLinkedSenderReturnsSeparateZeroCredit=3072,originalIrqReturnsSeparateZeroCredit=4096,completeCodeBytesVisited=56,literalBytes=0,sourceLinkedExistingSender=True,
            incomingR3VariationGroups=384,variationsPerGroup=4,transientFirstPaddingWritePreservedButExcludedFromSemanticR3Invariance=True,independentFullMappedMemoryStackOrderedEffectsAndPackedWordModel=True,rawRegistersFlagsStackModeAndMappedMemoryCompared=True,allThreeSenderResults=[0,-2,-1],providerReplacements=[],syntheticInitialControlHalfwords=[0,2,0x4000],physicalPeripheralExecution=False,trace=trace_info,unsupportedPrefixes=unsupported,maxInstructionsPerRun=2000,wholeSceneOrHardwareContextProven=False))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-wram',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=[row],nativeSymbols=symbols,
        sourceLinkedExistingDependency=dict(compilerResult=old,realLink=old_link,existingSourceSelectionPreserved=True,additionalFunctionOrByteCredit=0),
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted({Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins})],pinnedGeneratorAndRuntimeDependencies=pins,
        matchedInitializedBytes=56,matchedCodeBytes=56,generatedLiteralBytes=0,newOrdinaryFunctionCount=1,actualOuterReturns=3072,actualExistingSourceSenderReturnsSeparateZeroCredit=3072,actualOriginalIrqReturnsSeparateZeroCredit=4096,
        initializedDenominatorDelta=0,originalDataHelperAssemblyOrExtentCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),ownReturns=3072,existingSourceSenderReturnsSeparate=3072,irqReturnsSeparate=4096)),flush=True)
if __name__=='__main__':main()
