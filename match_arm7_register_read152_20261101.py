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
import arm7_register_read152_native_20261101 as native
import arm7_register_transfer36_functional_native_20261101 as direct
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-register-read152-final'
WORK=ROOT/'work/arm7-bulk-20261030/lane-register-read152-final'
REPORT=ROOT/'evidence/matches/arm7-register-read152-20261101.json'
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
        p=(ROOT/item['path']).resolve()
        if not p.is_relative_to(ROOT)or not p.is_file()or sha256(p)!=item['sha256']:raise ValueError('Required complete register-read source/runtime/module missing or changed')
    profile=json.loads((SOURCE/'profile.json').read_text())['units'];units=[compile_unit(seed,ROOT/seed['source'],WORK/seed['address'][2:])for seed in profile];helper,reader=units;original=(ROOT/profile[0]['binary']).read_bytes();own_helper=original[0xcc58:0xcc7c];own_reader=original[0xcc7c:0xccf0]
    if int.from_bytes(own_helper[-4:],'little')!=0x040001c2 or tuple(int.from_bytes(own_reader[o:o+4],'little')for o in(100,104,108,112))!=(0x040001c0,0x8202,0x8002,0x040001c2):raise ValueError('Actual original code/literal/register role witness differs')
    rebuilt=bytearray(original);rebuilt[0xcc58:0xcc7c]=helper[2];rebuilt[0xcc7c:0xccf0]=reader[2]
    if bytes(rebuilt)!=original:raise ValueError('Complete source-linked register pair differs')
    records=[];visited=set();nested=set()
    for index,case in enumerate(native.cases()):
        first=native.execute(original,own_reader,own_helper,case,index);second=native.execute(original,reader[2],helper[2],case,index)
        if first!=second or not first['modelPassed']:raise ValueError('Original/compiled reader/helper raw state and independent bus/frame/return model differ')
        records.append(dict(case=case,execution=first));visited.update(first['visitedOwn']);nested.update(first['visitedNested'])
    direct_records=[];direct_visited=set()
    for index,case in enumerate(direct.cases()):
        first=direct.execute(original,own_helper,case,index);second=direct.execute(original,helper[2],case,index)
        if first!=second or not first['modelPassed']:raise ValueError('Direct original/compiled helper full raw ABI/status/data model differs')
        direct_records.append(dict(case=case,execution=first));direct_visited.update(first['internal']['visitedOwnInstructionOffsets'])
    if len(records)!=580 or len(direct_records)!=2385 or visited!=set(range(native.ENTRY,native.ENTRY+100,4))or nested!=set(range(native.HELPER,native.HELPER+32,4))or direct_visited!=set(range(0,32,4)):raise ValueError('Complete code/direct-word/byte/bus-domain coverage differs')
    def trace(rows,path):
        raw=(json.dumps(rows,sort_keys=True,separators=(',',':'))+'\n').encode();path.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));return dict(path=path.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(path),gzipMtime=0)
    read_trace=trace(records,WORK/'reader-records.json.gz');direct_trace=trace(direct_records,WORK/'direct-helper-records.json.gz');unsupported=[]
    for name,case,budget in [('stuck-before',dict(native.cases()[0],stuck='Before'),300),('stuck-nested',dict(native.cases()[0],stuck='Nested'),300),('stuck-final',dict(native.cases()[0],stuck='Final'),300),('one-instruction',native.cases()[0],1)]:
        first=native.execute(original,own_reader,own_helper,case,0,budget=budget,allow_no_return=True);second=native.execute(original,reader[2],helper[2],case,0,budget=budget,allow_no_return=True)
        if first!=second or first['actualOwnReturn']:raise ValueError('Bounded reader path acquired outer return credit')
        unsupported.append(dict(name=name,originalAndCompiled=first,supportedErrorPathCredit=0,additionalNestedReturnCredit=0))
    matches=[];symbols={}
    for index,(row,link,body)in enumerate(units):
        local={name:hex(int(value['address'],0))for name,value in link['bindings'].items()};symbols.update(local);is_helper=index==0
        row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols=local,nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,
            sourceAbiContract=dict(physicalArgumentWords=1,wordSelectorExplicitlyMaskedToByte=True,result='clear-bit control halfword'if is_helper else'received halfword & 255',historicalTypesProven=False),
            oracle=dict(vectors=2965 if is_helper else 580,actualOriginalAndCompiledReturns=5930 if is_helper else 1160,directOriginalAndCompiledReturns=4770 if is_helper else 1160,nestedSourceLinkedOwnReturns=1160 if is_helper else 0,otherOwnedEntryReturnCreditDuplicated=False,
                completeCodeBytesVisited=32 if is_helper else 100,literalBytes=4 if is_helper else 16,sourceLinkedOwnedPair=True,providerReplacements=[],independentFullMemoryStackHalfwordStoreAndReturnModel=True,rawRegistersFlagsStackModeAndMappedMemoryCompared=True,
                fixedMmioAddressRoles=dict(control='0x40001c0',data='0x40001c2',width=2,actualOriginalPointerLiteralAndComputedAddressWitness=True,noArbitraryCodeWordOrDataAdmission=True),
                syntheticReadBoundary=dict(controlPhases=['Before','Nested','Final'],width=2,receivedWordInput=True,allLowByteSelectorsAndReceivedValuesCovered=True,physicalPeripheralExecution=False),readerTrace=read_trace,directHelperTrace=direct_trace,unsupported=unsupported,maxInstructionsPerRun=5000,wholeSceneOrHardwareContextProven=False))
        matches.append(row)
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-wram',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=matches,nativeSymbols=symbols,
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted({Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins})],pinnedGeneratorAndRuntimeDependencies=pins,
        matchedInitializedBytes=152,matchedCodeBytes=132,generatedLiteralBytes=20,newOrdinaryFunctionCount=2,totalActualOwnedReturns=7090,helperOwnReturns=5930,readerOwnReturns=1160,initializedDenominatorDelta=0,originalDataHelperAssemblyOrExtentCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),helperReturns=5930,readerReturns=1160)),flush=True)
if __name__=='__main__':main()
