import shutil
from pathlib import Path
import match_runtime as compiler
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/main-gecom352-matching-20261102'
REPORT = ROOT / 'evidence/matches/main-gecom352-20261102.json'
CAMPAIGNS = ['evidence/attempts/main-gecom352-section-view-v2-20261102.json']


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    metadata, image, _ = measured_module('main')
    assert metadata['sha256'] == 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    seeds = {}
    for name in CAMPAIGNS:
        for row in read_json(ROOT / name)['results']:
            if row['genuineExact']: seeds[int(row['identity']['address'], 0)] = row
    assert len(seeds) == 3 and sum(r['identity']['bytes'] for r in seeds.values()) == 352
    rows = []
    for address, seed in sorted(seeds.items()):
        original = ROOT / seed['source']
        assert sha256(original) == seed['sourceSha256']
        source = ROOT / 'src/runtime/20261102_gecom352' / original.name
        source.parent.mkdir(parents=True, exist_ok=True)
        if source.exists(): assert source.read_bytes() == original.read_bytes()
        else: shutil.copyfile(original, source)
        text = source.read_text(encoding='utf-8')
        assert len(text.splitlines()) <= 500 and '#include' not in text
        assert not any(t in text for t in ['/*', '//', 'asm ', '__asm', 'va_list', 'J2pUnknown'])
        previous = seed['compiledEntry']
        flags = previous['compilerFlags']
        old = compiler.FLAGS
        try:
            compiler.FLAGS = list(flags)
            compiler.WORK = WORK / source.stem / 'compile'
            result, _ = compiler.compare(source, 'main', flags[0][2:], flags[flags.index('-inline') + 1],
                compiler=ROOT / previous['compilerPath'])
            assert len(result) == 1 and not result[0].get('compileFailed')
            row = result[0]
            assert row['compilerFlags'] == flags and row['compilerSha256'] == previous['compilerSha256']
            proof = validate(row, qualified_bindings(row), WORK / source.stem / 'link')
        finally:
            compiler.FLAGS = old
        assert row['bytes'] == seed['identity']['bytes']
        row.update(sourceLanguage='C', exactBytes=row['bytes'], sourceOnlyCompilerInput=True,
            originalObjectScaffolding=False, genuineLinkComparison=freeze_link(proof),
            ordinaryLogicSource=True, nativeBehavioralReturns=0,
            sourceWordRank='original32-bit-long' if 'typedef unsigned long u32;' in text else 'explicit32-bit-int',
            evidenceClass='Complete ordinary C compiler and genuine linked-byte comparison; semantics unqualified')
        rows.append(row)
    write_json(REPORT, dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=rows, matchedFunctions=len(rows), matchedBytes=sum(r['bytes'] for r in rows),
        actualNativeFunctionReturns=0, inferredGameplaySemantics=False,
        sourceOrigin=dict(campaigns=[dict(path=name, sha256=sha256(ROOT / name)) for name in CAMPAIGNS],
            publicReferenceRevision='d636fb5d2b212e8736f09859fff447be2bd0ac85', gameSdkRevisionEstablished=False,
            typedAddressQualifiedFunctionsAndData=True, generatedDisassemblyOrEncodedExecutableInput=False),
        reproductionCommand='python match_main_gecom352_20261102.py',
        limitations=[
            'Complete source functions and relocation roles match; no native behavioral returns or gameplay semantics are asserted',
            'Per-unit compiler and flags are independently measured; no profile generalized',
            'VRAM storage remains complete typed original externs with zero additional data credit',
            'Original callees/hardware/data have zero additional source credit; boundary/interface audits and module acceptance are separate gates',
            'No complete Windows/Android game, rendering, ordinary scene reachability or source-only ROM claim']))
    print(dict(genuineOrdinaryCFunctions=len(rows), genuineInitializedBytes=sum(r['bytes'] for r in rows),
        actualNativeFunctionReturns=0, moduleAcceptancePending=True))


if __name__ == '__main__':
    main()
