from project import ROOT, write_json, sha256
import match_main_oam_reference296_closed_20261101 as builder


def main():
    output = ROOT / 'evidence/attempts/main-sdk-global-externs-20261102.json'
    assert not output.exists(), 'Preserve first global-ownership experiment'
    builder.WORK = ROOT / 'work/main-sdk-global-externs-20261102'
    results = []
    for address in [0x0202E69C, 0x0202E6CC]:
        original = ROOT / f'nonmatching/main/20261102-sdk-remaining-breadth/native_main_{address:08x}.c'
        text = original.read_text(encoding='utf-8')
        declaration = 'NNSG3dGlb native_data_main_020edf90;'
        assert text.count(declaration) == 2 and text.rstrip().endswith(declaration)
        text = text.rstrip()[:-len(declaration)] + '\n'
        assert 'extern ' + declaration in text
        source = ROOT / f'nonmatching/main/20261102-sdk-external-global/native_main_{address:08x}.c'
        source.parent.mkdir(parents=True, exist_ok=True)
        assert not source.exists()
        source.write_text(text, encoding='utf-8')
        result = dict(source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
            identity=dict(module='main', mode='arm', address=hex(address), bytes=48), sourceCredit=0,
            originalDefinitionPreserved=original.relative_to(ROOT).as_posix(),
            globalRemainsFullyTypedExternal=True, globalSourceDataCredit=0)
        try:
            row, proof, body = builder.build(source, source.stem, True)
            result.update(genuineExact=True, compiledEntry=row, genuineLinkProof=proof, genuineLinkedBytes=len(body))
        except Exception as error:
            result.update(genuineExact=False, errorType=type(error).__name__, refusal=str(error))
        results.append(result)
    write_json(output, dict(sourceCredit=0, results=results, originalModuleBssOwnershipUnchanged=True,
        logicBodyChanged=False, newDataDefinitionsSupplied=False))
    print(dict(functions=2, genuineExactFunctions=sum(r['genuineExact'] for r in results),
        genuineExactBytes=sum(r.get('genuineLinkedBytes', 0) for r in results), sourceCredit=0))


if __name__ == '__main__':
    main()
