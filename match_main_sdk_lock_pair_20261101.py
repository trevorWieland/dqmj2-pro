import hashlib
import json
import re
import sys
from pathlib import Path
import match_runtime
import crossreuse_utility_c
import recover_linked_runtime
import link_runtime_unit
import main_sdk_lock_pair_native_20261101 as fixture
import main_sdk_lock_pair_boundaries_20261101 as boundary
from elftools.elf.elffile import ELFFile
from project import ROOT,write_json

WORK=ROOT/'work/main-sdk-aux/20261101/lock-pair-final'
PROFILE=ROOT/'nonmatching/main-sdk-aux/20261101/lock-pair-final/closure.json'
PROFILE_SHA='07910298da5cb92e6553bdc8ecad28fd9e4a92ad293835cd8de7a01e57e92c40'
PINS=PROFILE.with_name('generator-pins.json')
PIN_SHA='68a632345d423bf482d27f660d868772f6d5a42f0edd53ba5fab57cab57f1d7b'
REPORT=ROOT/'evidence/matches/main-sdk-lock-pair-20261101.json'
ROM='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_inputs():
    import unicorn
    import elftools
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4'or elftools.__version__!='0.33':
        raise ValueError('Pinned main SDK execution runtime differs')
    if digest(PROFILE.read_bytes())!=PROFILE_SHA or digest(PINS.read_bytes())!=PIN_SHA or digest((ROOT/'inputs/game.nds').read_bytes())!=ROM:
        raise ValueError('Frozen main SDK source/runtime/build profile differs')
    pins=json.loads(PINS.read_text())['files']
    for row in pins:
        path=(ROOT/row['path']).resolve()
        if not path.is_relative_to(ROOT)or digest(path.read_bytes())!=row['sha256']:
            raise ValueError('Main SDK source/input closure changed: '+row['path'])
    profile=json.loads(PROFILE.read_text())
    accepted=json.loads((ROOT/profile['acceptedSnapshot']).read_text())['functions']
    for pin in profile['matches']:
        start=int(pin['address'],0)
        for row in accepted:
            address=int(row['address'],0)if isinstance(row['address'],str)else row['address']
            if row['program']==''and row['module']=='main'and row['mode']=='arm'and start<address+(row.get('bytes')or 1)and address<start+pin['bytes']:
                raise ValueError('Main SDK proposed span overlaps existing accepted source')
    return pins


def source_closure(pin):
    source=ROOT/pin['source']
    declarations=[dict(path=pin['source'],sha256=pin['sourceSha256']),*pin['sourceDependencies']]
    for row in declarations:
        path=(ROOT/row['path']).resolve()
        if not path.is_relative_to(source.parent.resolve())or digest(path.read_bytes())!=row['sha256']:
            raise ValueError('Actual main SDK C/include changed or escaped own directory')
        text=path.read_text()
        if len(text.splitlines())>500 or '/*'in text or '//'in text or re.search(r'\b(?:asm|__asm|INCBIN)\b',text):
            raise ValueError('Main SDK source must remain bounded comment-free ordinary C')
    includes=[(source.parent/name).resolve()for name in re.findall(r'^#include "([^"<>]+)"$',source.read_text(),re.M)]
    if {p.relative_to(ROOT).as_posix()for p in includes}!={r['path']for r in pin['sourceDependencies']}:
        raise ValueError('Main SDK complete quoted include closure differs')


def build(pin):
    source_closure(pin)
    compiler=ROOT/pin['compiler']
    if digest(compiler.read_bytes())!=pin['compilerSha256']:
        raise ValueError('Pinned main SDK compiler differs')
    directory=WORK/pin['address'];directory.mkdir(parents=True,exist_ok=True)
    match_runtime.WORK=directory/'isolated-compiler'
    attempt,compiled=crossreuse_utility_c.compile_origin(pin,compiler,pin['compilerFlags'],directory)
    if compiled is None:raise ValueError(attempt)
    derived,masks,body=compiled
    if len(body)!=pin['bytes']:raise ValueError('Full SDK C size differs')
    with(ROOT/derived['probeObject']).open('rb')as stream:
        elf=ELFFile(stream);symbol=next(row for row in elf.get_section_by_name('.symtab').iter_symbols()if row.name==pin['name'])
        section,offset=symbol['st_shndx'],symbol['st_value']&~1
    entry=dict(pin,object=derived['probeObject'],objectSha256=derived['probeObjectSha256'],sectionIndex=section,sectionOffset=offset,
        relocations=[dict(row,target=hex(match_runtime.symbol_address(row['symbol'])),format='SHT_RELA',explicitAddend=row['addend'],
            originalEncodedWord=body[row['offset']:row['offset']+4].hex())for row in derived['relocations']],
        sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,compiledBytes=len(body),matchingBytes=len(body),
        wholeModuleLinked=False,originalDataSourceCredit=0)
    bindings=recover_linked_runtime.qualified_bindings(entry)
    proof=link_runtime_unit.validate(entry,bindings,directory/'real-link')
    return dict(entry,realMainLink=proof,exactAfterDeclaredRelocation=proof['exactCallerBytes'],exactAfterRealMwLink=proof['exactCallerBytes'],
        nativeSymbolEntries=bindings,nativeSymbols={name:int(item['address'],0)for name,item in bindings.items()},boundaries=boundary.boundaries(entry),
        executableInstructionBytes=pin['bytes'],generatedLiteralBytes=0,nativeCalleeSourceCredit=0,
        sourceAbiContract={'physicalArgumentWords':4,'recordArgumentIsPointer':True,'recordMinimumCViewBytes':8,'observedRecordBytes':6,
            'originalObjectExtentOrPaddingClaimed':False,'idAndSwapWordBits':32,'ownerStoreBits':16,'selectorTest':'full-word nonzero',
            'callback':'u32(void); ignored return, original ARM no-input CPSR callbacks qualified',
            'return':'raw-u32; release sentinelFFFFFFFE, acquire full previous swap word'},
        sourceOnlyCompilerInput={'source':pin['source'],'sha256':pin['sourceSha256'],'includes':pin['sourceDependencies'],
            'originalCodeCompilerInput':False},compileCommand=[str(compiler),*pin['compilerFlags'],'-c',str(ROOT/pin['source']),'-o',str(ROOT/derived['probeObject'])],
        compileCwd=str(ROOT))


def proof():
    verify_inputs();rows=[build(pin)for pin in json.loads(PROFILE.read_text())['matches']]
    bodies={int(row['address'],0):(WORK/row['address']/'real-link/caller.bin').read_bytes()for row in rows}
    oracle=fixture.oracle(bodies)
    for row in rows:
        row['oracle']=dict(oracle,ownedEntry=row['address'],actualOriginalAndCompiledReturns=oracle['actualOwnReturnCounts'][row['address']],
            actualSharedSuiteOriginalAndCompiledReturns=oracle['actualOriginalAndCompiledReturns'],sharedSuiteCountsMustNotBeSummedPerRow=True)
    bindings={}
    for row in rows:
        for name,binding in row['nativeSymbolEntries'].items():
            if name in bindings and bindings[name]!=binding:raise ValueError('Conflicting qualified main SDK callee identity')
            bindings[name]=binding
    return {'matches':rows,'nativeSymbolEntries':bindings,'nativeSymbols':{n:int(v['address'],0)for n,v in bindings.items()},
        'matchedInitializedBytes':224,'matchedInstructionBytes':224,'generatedLiteralBytes':0,'newOrdinaryFunctionCount':2,
        'newInitializedCoverageBytes':224,'originalHelperOrCallbackSourceCredit':0,'originalDataOrExtentOrPaddingCredit':0,
        'ordinaryAssemblyOrBlobCredit':0,'wholeModuleLinked':False,'sourceReconstructionComplete':False,
        'nativeStateModel':oracle,'initializedDenominatorDelta':0}


def main():
    pins=verify_inputs();report=proof()
    names=sorted({Path(__file__).name,PROFILE.relative_to(ROOT).as_posix(),PINS.relative_to(ROOT).as_posix()}|{r['path']for r in pins})
    report.update(schemaVersion=1,generator=Path(__file__).name,generatorSha256=digest(Path(__file__).read_bytes()),
        generatorSources=[dict(path=n,sha256=digest((ROOT/n).read_bytes()))for n in names],pinnedGeneratorAndRuntimeDependencies=pins,
        romSha256=ROM,processor='arm9',program='',module='main')
    write_json(REPORT,report)
    print(json.dumps({'report':REPORT.relative_to(ROOT).as_posix(),'sha256':digest(REPORT.read_bytes()),'functions':2,'newSourceBytes':224,
        'ownReturns':report['nativeStateModel']['actualOriginalAndCompiledReturns'],'helperAndCallbackCredit':0}),flush=True)


if __name__=='__main__':
    main()
