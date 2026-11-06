import json
from pathlib import Path
from project import ROOT,sha256
REFERENCE=ROOT/'provenance/arm7-host-pxi-pack-three-word-context-20261101.json'
REFERENCE_SHA='f99714c19dfc62d65e67b7424db94a943f0f123897f7c264f14493bb4bec3a77'
def apply(child,program):
    if program:return dict(applied=False,reason='Qualified host contract never applies to child program namespace',sourceCredit=0)
    if sha256(REFERENCE)!=REFERENCE_SHA:raise ValueError('Three-word context reference changed')
    ref=json.loads(REFERENCE.read_text());report=json.loads((ROOT/ref['proofReport']).read_text());row=report['matches'][0]
    for key in('processor','program','module','mode','address','bytes','source','sourceSha256','inputModuleSha256','targetSha256'):
        if row[key]!=ref[key]:raise ValueError('Complete qualified source/native context identity differs')
    if row['sourceDependencies']!=ref['sourceDependencies']or sha256(ROOT/row['source'])!=ref['sourceSha256']:raise ValueError('Typed three-input source closure differs')
    for item in ref['sourceDependencies']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Complete compatible source header differs')
    if sha256(ROOT/ref['proofGenerator'])!=ref['proofGeneratorSha256']or report['generatorSha256']!=ref['proofGeneratorSha256']:raise ValueError('Actual typed/native proof generator differs')
    module=ROOT/row['binary'];raw=module.read_bytes();offset=int(ref['address'],0)-row['base']
    import hashlib
    if sha256(module)!=ref['inputModuleSha256']or hashlib.sha256(raw[offset:offset+56]).hexdigest()!=ref['targetSha256']:raise ValueError('Measured host function/module changed')
    abi=row['sourceAbiContract'];oracle=row['oracle']
    if abi['physicalArgumentWords']!=3 or abi['semanticFourthArgumentRequired']or not abi['fullyAssignedBitfieldsBeforeWordRead']or not abi['nativeTransientScratchR3ReadRecorded']:raise ValueError('Three semantic inputs require exact scratch/bitfield qualification')
    if oracle['actualOriginalAndCompiledReturns']!=3072 or oracle['incomingR3VariationGroups']!=384 or oracle['variationsPerGroup']!=4 or not oracle['transientFirstPaddingWritePreservedButExcludedFromSemanticR3Invariance']:raise ValueError('Complete actual return/scratch variation witness differs')
    if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']:raise ValueError('Source-only complete genuine native byte gate differs')
    child.ARGUMENTS['arm7'][0x037fe410]=3
    return dict(applied=True,reference=REFERENCE.relative_to(ROOT).as_posix(),referenceSha256=REFERENCE_SHA,processor='arm7',program='',module='arm7-wram',address='0x37fe410',mode='arm',bytes=56,semanticWords=3,transientPhysicalScratchReadPreserved=True,sourceCredit=0)
