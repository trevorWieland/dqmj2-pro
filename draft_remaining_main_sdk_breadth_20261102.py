import re
import match_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import measured_module
import match_main_oam_reference296_closed_20261101 as builder


def main():
    output = ROOT / 'evidence/attempts/main-sdk-remaining-breadth-20261102.json'
    assert not output.exists(), 'Preserve original breadth campaign'
    archive = ROOT / 'evidence/attempts/main-sdk-visibility-v4-candidate-archive-20261102.json'
    snapshot = ROOT / 'evidence/verification/accepted-cohort143-identities-v2-20261101.json'
    accepted = {(r['module'], r['address']) for r in read_json(snapshot)['functions']}
    reserved = {0x02034248, 0x02034320, 0x02034388, 0x0202EA64, 0x0202FA04, 0x0202EBC0}
    _, image, _ = measured_module('main')
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    builder.WORK = ROOT / 'work/main-sdk-remaining-breadth-20261102'
    results = []
    for row in read_json(archive)['rows']:
        identity = row['identity']
        address = int(identity['address'], 0)
        if ('main', address) in accepted or address in reserved: continue
        original = ROOT / row['candidate']
        assert sha256(original) == row['sourceSha256']
        text = original.read_text(encoding='utf-8')
        aliases = {row['name']: f'native_main_{address:08x}'}
        for relocation in row['genuineLinkProof']['originalRelocations']:
            offset, kind = relocation['offset'], relocation['type']
            native = image[address - 0x02000000 + offset:address - 0x02000000 + offset + 4]
            if kind in [1, 28, 29]:
                instruction = next(decoder.disasm(native, address + offset))
                assert instruction.operands[0].type == 2
                target = instruction.operands[0].imm & ~1
                alias = f'native_fn_{target:08x}'
            elif kind == 2:
                assert relocation['format'] == 'SHT_RELA'
                target = (int.from_bytes(native, 'little') - relocation['explicitAddend']) & 0xFFFFFFFF
                alias = f'native_data_main_{target:08x}'
            else: raise AssertionError(relocation)
            assert relocation['symbol'] not in aliases or aliases[relocation['symbol']] == alias
            aliases[relocation['symbol']] = alias
        for name, alias in aliases.items():
            text = re.sub(r'\b' + re.escape(name) + r'\b', alias, text)
        text = text.replace('typedef unsigned long u32;', 'typedef unsigned int u32;')
        text = text.replace('typedef signed long s32;', 'typedef signed int s32;')
        assert len(text.splitlines()) <= 500 and not any(t in text for t in ['/*', '//', 'asm ', '__asm'])
        source = ROOT / f'nonmatching/main/20261102-sdk-remaining-breadth/native_main_{address:08x}.c'
        source.parent.mkdir(parents=True, exist_ok=True)
        assert not source.exists()
        source.write_text(text, encoding='utf-8')
        result = dict(identity=identity, source=source.relative_to(ROOT).as_posix(),
            sourceSha256=sha256(source), sourceCredit=0, referenceName=row['name'],
            functionAliases=aliases, sourceLanguage='C', nativeExecutionReturns=0)
        try:
            compiled, proof, body = builder.build(source, source.stem, True)
            result.update(genuineExact=True, compiledEntry=compiled, genuineLinkProof=proof,
                genuineLinkedBytes=len(body))
        except Exception as error:
            result.update(genuineExact=False, errorType=type(error).__name__, refusal=str(error))
        results.append(result)
    write_json(output, dict(sourceCredit=0, inputSnapshot=snapshot.relative_to(ROOT).as_posix(),
        inputSnapshotSha256=sha256(snapshot), referenceArchiveSha256=sha256(archive), results=results,
        allOutputsPendingSourceInterfaceBoundaryAndModuleAcceptance=True, actualFunctionReturns=0))
    print(dict(draftedFunctions=len(results), draftedInitializedBytes=sum(r['identity']['bytes'] for r in results),
        genuineExactFunctions=sum(r['genuineExact'] for r in results),
        genuineExactBytes=sum(r.get('genuineLinkedBytes', 0) for r in results), sourceCredit=0))


if __name__ == '__main__':
    main()
