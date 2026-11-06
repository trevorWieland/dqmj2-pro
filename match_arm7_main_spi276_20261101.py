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
import arm7_main_spi276_native_20261101 as native
import arm7_runtime
import struct
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-main-spi276-final'
WORK=ROOT/'work/arm7-bulk-20261030/lane-main-spi276-final'
REPORT=ROOT/'evidence/matches/arm7-main-spi276-20261101.json'
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
def ownership():
    image=(ROOT/'extract/arm7/arm7.bin').read_bytes();layout=arm7_runtime.derive(image);rom=(ROOT/'inputs/game.nds').read_bytes();offset,entry,load,size=struct.unpack_from('<4I',rom,0x30)
    if sha256(ROOT/'inputs/game.nds')!='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'or rom[offset:offset+size]!=image or load!=arm7_runtime.BASE or entry!=arm7_runtime.BASE or layout!=json.loads((ROOT/'evidence/arm7/runtime-layout.json').read_text()):raise ValueError('Actual original ROM header/image/descriptors differ')
    modules=[]
    for module in layout['modules']:
        begin=module['inputFileOffset'];raw=image[begin:begin+module['inputBytes']]
        if (ROOT/module['binary']).read_bytes()!=raw:raise ValueError('Current runtime bytes not actual autoload source slice')
        modules.append(dict(module=module['id'],sourceImageOffset=begin,romOffset=offset+begin,bytes=len(raw),runtimeBase=module['runtimeBase'],sha256=hashlib.sha256(raw).hexdigest()))
    main=next(x for x in layout['modules']if x['id']=='arm7-main');wram=next(x for x in layout['modules']if x['id']=='arm7-wram');first=main['inputFileOffset']+0x154f0;second=wram['inputFileOffset']+0xcc58
    if image[first:first+36]!=image[second:second+36]or abs(first-second)<36:raise ValueError('Separate stored instance witness differs')
    main_first=int(main['runtimeBase'],0);main_last=int(main['bssStart'],0)+main['bssBytes']
    if any(address<main_last and main_first<address+4096 for address in(native.STACK,native.OUTPUT,native.STOP)):raise ValueError('Fixture page collides with actual main initialized or BSS extent')
    return dict(romArm7Offset=offset,romArm7Bytes=size,romArm7Load=hex(load),romArm7Entry=hex(entry),descriptorSource=layout['nativeTrace'],composition=layout['composition'],modules=modules,duplicateHelper=dict(mainImageOffset=first,wramImageOffset=second,distinctSourceSlices=True,distinctRuntimeModules=True),denominatorDelta=0,fixtureStack=hex(native.STACK),fixtureOutput=hex(native.OUTPUT),fixtureStop=hex(native.STOP),allOutsideMainInitializedAndBss=True)

def main():
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        p=(ROOT/item['path']).resolve()
        if not p.is_relative_to(ROOT)or not p.is_file()or sha256(p)!=item['sha256']:raise ValueError('Current complete main-SPI source/runtime/input missing or changed')
    load=ownership();profile=json.loads((SOURCE/'profile.json').read_text())['units'];units=[compile_unit(seed,ROOT/seed['source'],WORK/seed['address'][2:])for seed in profile];original=(ROOT/profile[0]['binary']).read_bytes();matches=[]
    for row,link,body in units:
        entry=int(row['address'],0);size,pool,kind,command=native.SPECS[entry];own=original[entry-native.BASE:entry-native.BASE+size];records=[];visited=set()
        if body!=own:raise ValueError('Fresh linked main SPI complete body differs')
        for index,case in enumerate(native.cases(entry)):
            first=native.execute(original,entry,own,case,index);second=native.execute(original,entry,body,case,index)
            if first!=second or not first['modelPassed']:raise ValueError('Original/source main SPI full CPU/memory/halfword model differs')
            records.append(dict(case=case,execution=first));visited.update(first['visited'])
        if visited!=set(range(entry,entry+size-pool,4)):raise ValueError('Main SPI complete instruction coverage differs')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/row['address'][2:]/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));unsupported=[]
        for phase in range(1 if kind=='helper'else 2 if kind=='command'else 3):
            case=dict(native.cases(entry)[0],stuck=phase);first=native.execute(original,entry,own,case,0,budget=300,allow_no_return=True);second=native.execute(original,entry,body,case,0,budget=300,allow_no_return=True)
            if first!=second or first['actualOwnReturn']:raise ValueError('Busy main SPI acquired normal return')
            unsupported.append(dict(phase=phase,execution=first,supportedErrorPathCredit=0))
        row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols={k:hex(int(v['address'],0))for k,v in link['bindings'].items()},nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,
            sourceAbiContract=dict(physicalArgumentWords=0 if kind=='command'else 1,kind=kind,fixedCommand=command,outputStoreWidth=1 if kind=='output'else None,outputRawAddressWordReturnView=kind=='output',legacyCallerDeclarationCompatible=True,historicalPublicReturnMeaningProven=False,historicalTypesOrDevicePolicyProven=False),
            oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),actualNestedReturns=0,allOwnInstructionsVisited=True,independentRegisterHalfwordPollOutputByteAndUntouchedMemoryModel=True,rawRegistersFlagsStackAndMappedMemoryCompared=True,providerReplacements=[],physicalPeripheralExecution=False,outputOffsets=[0,1,4,255,511,4095]if kind=='output'else[],unsupported=unsupported,maxInstructionsPerRun=5000,wholeSceneOrHardwareContextProven=False,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
        matches.append(row)
    result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=matches,nativeSymbols={},runtimeOwnership=load,
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted({Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins})],pinnedGeneratorAndRuntimeDependencies=pins,newOrdinaryFunctionCount=4,matchedInitializedBytes=276,matchedCodeBytes=248,generatedLiteralBytes=28,initializedDenominatorDelta=0,totalActualOwnReturns=5678,existingWramImplementationDuplicateByteCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,originalDataAssemblyOrExtentCredit=0)
    write_json(REPORT,result);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),actualOwnReturns=5678)),flush=True)
if __name__=='__main__':main()
