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
import arm7_register_flag80_native_20261101 as native
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-register-flag80-final'
WORK=ROOT/'work/arm7-bulk-20261030/lane-register-flag80-final'
REPORT=ROOT/'evidence/matches/arm7-register-flag80-20261101.json'
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
        if not p.is_relative_to(ROOT)or not p.is_file()or sha256(p)!=item['sha256']:raise ValueError('Required complete flag source/runtime/module missing or changed')
    profile=json.loads((SOURCE/'profile.json').read_text());dependencies=[compile_unit(seed,ROOT/seed['source'],WORK/'dependencies'/seed['address'][2:])for seed in profile['dependencies']];units=[compile_unit(seed,ROOT/seed['source'],WORK/seed['address'][2:])for seed in profile['units']];original=(ROOT/profile['units'][0]['binary']).read_bytes();source_dependencies=[];compiled_lower={};all_symbols={}
    for row,link,body in dependencies:
        address=int(row['address'],0);compiled_lower[address]=body;source_dependencies.append(dict(row,realLink=link,sourceCredit=0,byteCredit=0,freshlySourceCompiledAndLinked=True));all_symbols.update({k:hex(int(v['address'],0))for k,v in link['bindings'].items()})
    matches=[];all_records=[]
    for row,link,body in units:
        entry=int(row['address'],0);compiled=dict(compiled_lower);compiled[entry]=body;native_bodies={address:original[address-native.BASE:address-native.BASE+len(code)]for address,code in compiled.items()};records=[];visits={hex(address):set()for address in compiled}
        if any(compiled[a]!=native_bodies[a]for a in compiled):raise ValueError('Whole fresh flag/reader/writer/helper source chain differs')
        for index,case in enumerate(native.cases()):
            first=native.execute(original,native_bodies,entry,case,index);second=native.execute(original,compiled,entry,case,index)
            if first!=second or not first['modelPassed']:raise ValueError('Original/compiled flag closure or independent full argument/frame/halfword model differs')
            records.append(dict(case=case,execution=first))
            for name,items in first['visits'].items():visits[name].update(items)
        pools={entry:0,native.READER:16,native.WRITER:12,native.HELPER:4}
        for address,code in compiled.items():
            if visits[hex(address)]!=set(range(address,address+len(code)-pools[address],4)):raise ValueError('Fresh source chain instruction coverage incomplete')
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/row['address'][2:]/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));unsupported=[]
        for phase in range(5):
            case=dict(native.cases()[0],stuck=phase);first=native.execute(original,native_bodies,entry,case,0,budget=500,allow_no_return=True);second=native.execute(original,compiled,entry,case,0,budget=500,allow_no_return=True)
            if first!=second or first['actualOwnReturn']:raise ValueError('Permanent busy chain acquired normal return')
            unsupported.append(dict(phase=phase,execution=first,additionalReturnCredit=0,supportedErrorPathCredit=0))
        local={k:hex(int(v['address'],0))for k,v in link['bindings'].items()};all_symbols.update(local);row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols=local,nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,
            sourceAbiContract=dict(physicalArgumentWords=1,maskWordConsumedWithoutNarrowing=True,readSelector=0,writeSelector=0,writeArgument='(receivedByte & ~mask) & 255'if entry==native.ENTRIES[1]else'receivedByte | mask',result='written low byte',historicalTypesOrDevicePolicyProven=False),
            oracle=dict(vectors=337,actualOriginalAndCompiledReturns=674,actualSourceReaderReturnsSeparateZeroCredit=674,actualSourceWriterReturnsSeparateZeroCredit=674,actualSourceHelperReturnsSeparateZeroCredit=1348,rawRegistersFlagsStackAndMappedMemoryCompared=True,independentWordArgumentHalfwordPortStackAndLowByteModel=True,allOwnAndDependencyInstructionsVisited=True,sourceLinkedDependenciesFreshlyBuilt=True,providerReplacements=[],physicalPeripheralExecution=False,busyPhases=5,unsupported=unsupported,maxInstructionsPerRun=5000,wholeSceneOrHardwareContextProven=False,
                trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)))
        matches.append(row)
    result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-wram',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=matches,nativeSymbols=all_symbols,sourceLinkedDependencies=source_dependencies,
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted({Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins})],pinnedGeneratorAndRuntimeDependencies=pins,newOrdinaryFunctionCount=2,matchedInitializedBytes=80,matchedCodeBytes=80,generatedLiteralBytes=0,initializedDenominatorDelta=0,sourceLinkedDependencyBytesSeparateZeroCredit=240,totalActualOwnReturns=1348,totalActualDependencyReturnsSeparateZeroCredit=5392,wholeModuleLinked=False,sourceReconstructionComplete=False,originalDataAssemblyOrExtentCredit=0)
    write_json(REPORT,result);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),actualOwnReturns=1348,actualDependencyReturnsSeparate=5392)),flush=True)
if __name__=='__main__':main()
