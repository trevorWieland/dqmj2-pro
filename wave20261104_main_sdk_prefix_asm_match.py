import hashlib
import re
import shutil
from pathlib import Path
import wave20261104_main_sdk_prefix_match as F
import wave20261104_main_sdk_prefix_asm_origin as O
from project import ROOT,configuration,read_json,write_json,sha256
from recover_linked_runtime import qualified_bindings
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-sdk-prefix/original-asm'
WORK = ROOT / 'work/w4sp/a/p'
INPUT = LANE / 'inputs.json'
MUTATIONS = {
    'CP_SaveContext':('and r12, r12, #0x0003','and r12, r12, #0x0001','Drop the divider mode high bit from the saved hardware context'),
    'CPi_RestoreContext':('strh r3, [r1, #0x2b0 - 0x290 ]','strh r2, [r1, #0x2b0 - 0x290 ]','Restore the divider mode value into the square-root control register'),
    'init_cp15':('mcr p15, 0, r0, c7, c5, 0','mcr p15, 0, r0, c7, c6, 0','Replace instruction-cache invalidation with a second data-cache invalidation'),
    '_start':('mov r0, #0x13','mov r0, #0x1f','Select system mode instead of supervisor mode for initial banked-stack setup'),
    'OS_InitContext':('add newpc, newpc, #4','add newpc, newpc, #8','Store an incorrect program-counter bias in the thread context'),
    'OS_SaveContext':('mov r0, #1','mov r0, #0','Remove the saved nonzero resumed-return value'),
    'OS_LoadContext':('msr spsr_fsxc, r1','msr cpsr_fsxc, r1','Write the live status register rather than the exception-return saved status'),
    'OSi_SetExContext':('mrs r2, SPSR','mrs r2, CPSR','Capture current processor status instead of the interrupted status register'),
    'OSi_ExceptionHandler':('and r1, r1, #0x1f','and r1, r1, #0x0f','Mask away the processor-mode high bit during exception dispatch')
}


def checked_source(item):
    for pin in [dict(path=item['source'],sha256=item['sourceSha256']),*item['sourceDependencies']]:
        path=ROOT/pin['path'];text=path.read_text()
        assert sha256(path)==pin['sha256'] and len(text.splitlines())<=500
        assert '/*' not in text and '//' not in text and all(line==line.rstrip() for line in text.splitlines())
        assert not re.search(r'\b(?:__asm|__asm__|J2pUnknownVaList|va_list|size_t)\b',text)
        if path.suffix=='.h':assert '#include' not in text
    source=ROOT/item['source'];prefix=source.read_text().split('{',1)[0]
    assert len(re.findall(r'\basm\b',prefix))==1
    assert item['sourceLanguage']=='assembly'
    assert item['assemblyJustification']['classification']=='verified-original-SDK-assembly'
    assert item['assemblyJustification']['ordinaryLogicAssemblyExceptions']==0
    assert '-lang' in item['flags'] and item['flags'][item['flags'].index('-lang')+1]=='c99'
    assert not any(flag=='-i' or flag.startswith('-D') for flag in item['flags'])
    return source


def negative(item,source,directory):
    directory.mkdir(parents=True,exist_ok=True)
    before,after,meaning=MUTATIONS[item['referenceFunction']]
    text=source.read_text();assert text.count(before)==1,(item['referenceFunction'],before)
    wrong=directory/source.name;wrong.write_text(text.replace(before,after))
    for pin in item['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/Path(pin['path']).name)
    row=F.compile_source(item,wrong,directory)
    try:F.L.validate(row,qualified_bindings(row),directory/'link')
    except ValueError as error:
        failure=error.args[0]
        assert isinstance(failure,dict) and failure['nativeBytes']==failure['linkedBytes']==item['bytes']
        assert failure['matchingBytes']<item['bytes']
        return dict(kind='Meaningful same-extent original assembly source operand mutation',before=before,after=after,semanticConsequence=meaning,rejectedByFullGenuineLinkComparison=True,comparison=failure,wrongSourceSha256=sha256(wrong),wrongObjectSha256=row['objectSha256'],instructionOrObjectPatched=False,sourceOrBehaviorCredit=0)
    raise ValueError('Mutated original assembler source unexpectedly matched')


def main():
    inputs=read_json(INPUT)
    for pin in inputs['files']:assert sha256(ROOT/pin['path'])==pin['sha256'],pin['path']
    metadata,image,unused=F.L.measured_module('main')
    assert inputs['romSha256']==configuration()['romSha256'] and metadata['sha256']==inputs['moduleSha256']
    matches,controls,layouts,origins=[],[],[],[]
    for item in inputs['entries']:
        source=checked_source(item);directory=WORK/format(int(item['address'],0),'08x')
        origins.append(dict(address=item['address'],**O.verify(item,source,directory/'published-origin')))
        row=F.compile_source(item,source,directory/'source')
        assert row['relocations']==item['priorRelocations'] and row['compiledBytes']==item['bytes']
        row['sourceDependencies']=item['sourceDependencies'];bindings=qualified_bindings(row)
        assert bindings==item['qualifiedDependencies']
        proof=F.L.validate(row,bindings,directory/'source/link')
        body=(directory/'source/link/caller.bin').read_bytes();address=int(item['address'],0)
        assert body==image[address-0x02000000:address-0x02000000+item['bytes']]
        layouts.append(dict(address=item['address'],**F.layout_checks(item,source,directory/'layout')))
        controls.append(dict(address=item['address'],**negative(item,source,directory/'negative')))
        controls.extend(dict(address=item['address'],**value) for value in F.binding_controls(row,directory/'binding'))
        row.update(program='',realLink=proof,manualRelocationComparison=dict(exact=row['exactAfterDeclaredRelocation'],matchingBytes=row['matchingBytes']),exactAfterDeclaredRelocation=proof['exactCallerBytes'],matchingBytes=item['bytes'],matchingBytesScope='Complete genuinely linked native function extent',sourceLanguage='assembly',assemblyJustification=item['assemblyJustification'],ordinaryCBytes=0,justifiedAssemblyBytes=item['bytes'],justifiedAssemblyRanges=[dict(program='',processor='arm9',module='main',mode='arm',address=item['address'],offset=0,bytes=item['bytes'])],qualifiedDependencies=bindings,nativeSymbolEntries=bindings,originalObjectScaffolding=False,sourceOnlyCompilerInput=True,referenceFunction=item['referenceFunction'],actualNativeFunctionReturns=0,calleeCodeOrSourceCredit=0)
        matches.append(row);print('proved original SDK asm',item['address'],item['bytes'],item['referenceFunction'],flush=True)
    assert len(matches)==9 and sum(r['bytes'] for r in matches)==1184
    closure=code_closure([Path(__file__).name])
    report=dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=metadata['sha256'],processor='arm9',module='main',program='',allPassed=True,matches=matches,matchedFunctions=len(matches),matchedBytes=1184,ordinaryCBytes=0,justifiedAssemblyBytes=1184,actualNativeFunctionReturns=0,hardwareOrExceptionExecutionCredit=0,nativeCalleeSourceCredit=0,ordinaryLogicAssemblyExceptions=0,sourceOnlyCompilerInputs=True,originalStorageSourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],typedLayoutChecks=layouts,negativeEvidence=controls,publishedStatementOrigin=origins,freshCompileObjectsAndLinkedReportsEveryRun=True,limits=['Only these nine explicitly published original SDK CPU/context/exception/reset primitives use justified assembly; ordinary matrix/memory/game algorithms are excluded.','Complete original extents, original object relocations/addends/H bits, genuine pinned MW links and fresh published-source preprocessing/token identity are proved.','No physical hardware, reset/IRQ/exception execution, native callee or game behavior credit is claimed.','The published SDK source is comparative evidence; it does not identify this modified game SDK revision or original authorship.','Shared module/ROM acceptance remains coordinator owned.'])
    write_json(LANE/'match.json',report);print(dict(functions=9,bytes=1184,ordinaryC=0,justifiedASM=1184,controls=len(controls)),flush=True)


if __name__=='__main__':main()
