import shutil
from pathlib import Path
import match_runtime as compiler
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/main-sbc2480-matching-20261102'
REPORT = ROOT / 'evidence/matches/main-sbc2480-20261102.json'


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    metadata, image, _ = measured_module('main')
    assert metadata['sha256'] == 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    report = read_json(ROOT / 'evidence/attempts/main-sbc2480-external-storage-20261102.json')
    seeds = {int(r['identity']['address'], 0): r for r in report['results'] if r['genuineExact']}
    env = read_json(ROOT / 'evidence/attempts/main-sbc-environment-section-view-20261102.json')
    seeds[0x02031800] = env
    rows = []
    for address, seed in sorted(seeds.items()):
        original = ROOT / seed['source']
        assert sha256(original) == seed['sourceSha256']
        folder = ROOT / f'src/runtime/20261102_sbc2480/{address:08x}'
        folder.mkdir(parents=True, exist_ok=True)
        source, header = folder / original.name, folder / 'types.h'
        for old, new in [(original, source), (original.parent / 'types.h', header)]:
            if new.exists(): assert new.read_bytes() == old.read_bytes()
            else: shutil.copyfile(old, new)
            text = new.read_text(encoding='utf-8')
            assert len(text.splitlines()) <= 500 and not any(t in text for t in ['/*', '//', 'asm ', '__asm'])
        previous = seed['compiledEntry']
        flags, old_flags = previous['compilerFlags'], compiler.FLAGS
        try:
            compiler.FLAGS = list(flags)
            compiler.WORK = WORK / f'{address:08x}' / 'compile'
            result, _ = compiler.compare(source, 'main', flags[0][2:], flags[flags.index('-inline') + 1],
                compiler=ROOT / previous['compilerPath'])
            assert len(result) == 1 and not result[0].get('compileFailed')
            row = result[0]
            row['sourceDependencies'] = [dict(path=header.relative_to(ROOT).as_posix(), sha256=sha256(header))]
            proof = validate(row, qualified_bindings(row), WORK / f'{address:08x}' / 'link')
        finally: compiler.FLAGS = old_flags
        row.update(sourceLanguage='C', exactBytes=row['bytes'], sourceOnlyCompilerInput=True,
            originalObjectScaffolding=False, genuineLinkComparison=freeze_link(proof),
            nativeBehavioralReturns=0, originalStaticStorageSourceDataCredit=0,
            evidenceClass='Complete ordinary C and genuine linked-byte comparison; behavioral/hardware semantics unqualified')
        rows.append(row)
    assert len(rows) == 3 and sum(r['bytes'] for r in rows) == 2480
    write_json(REPORT, dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=rows, matchedFunctions=3, matchedBytes=2480, actualNativeFunctionReturns=0,
        originalStorageContext=dict(billboardInitializersIndependentlyEqualOriginalStorage=True,
            environmentOriginal16ByteExtent='0x020dd690..0x020dd69f', words=[42, 0, 42, 0],
            accessedLastTwoWords='0x020dd698..0x020dd69f', additionalDataCredit=0),
        reproductionCommand='python match_main_sbc2480_20261102.py',
        limitations=[
            'Only complete ordinary C caller spans, headers and relocations are qualified; zero native behavioral returns or rendering evidence',
            'Original static graphics command storage is external scaffolding with zero data credit; its data words are not executable source',
            'The environment mapper retains the measured larger original section view to preserve compiler addressing; no byte patching or linker exception',
            'Headers and bodies are separated below500 formatted lines each with repository-local explicit dependencies',
            'Module/ROM acceptance and ordinary scene reachability remain separate; no complete Windows/Android game claim']))
    print(dict(genuineOrdinaryCFunctions=3, genuineInitializedBytes=2480,
        actualNativeFunctionReturns=0, sourceDataCredit=0, moduleAcceptancePending=True))


if __name__ == '__main__':
    main()
