import re
from project import ROOT, read_json, write_json, sha256
import match_main_oam_reference296_closed_20261101 as builder


def main():
    output = ROOT / 'evidence/attempts/main-animation-hints292-preflight-20261102.json'
    assert not output.exists(), 'Preserve the first compiler experiment'
    builder.WORK = ROOT / 'work/main-animation-hints292-preflight-20261102'
    own = {0x0202EA64: 'updateHintVec_', 0x0202FA04: 'updateHintVec_',
        0x0202EBC0: 'NNS_G3dRenderObjRemoveAnmObj'}
    results = []
    archive = ROOT / 'evidence/attempts/main-sdk-visibility-v4-candidate-archive-20261102.json'
    for row in read_json(archive)['rows']:
        address = int(row['identity']['address'], 0)
        if address not in own: continue
        original = ROOT / row['candidate']
        assert sha256(original) == row['sourceSha256']
        text = original.read_text(encoding='utf-8')
        text = re.sub(r'\b' + own[address] + r'\b', f'native_main_{address:08x}', text)
        text = re.sub(r'\bremoveLink_\b', 'native_fn_0202eb4c', text)
        text = text.replace('typedef unsigned long u32;', 'typedef unsigned int u32;')
        text = text.replace('typedef signed long s32;', 'typedef signed int s32;')
        text = text.replace('1 << (i & 31)', '1U << (i & 31)')
        assert len(text.splitlines()) <= 500 and '/*' not in text and '//' not in text
        source = ROOT / f'src/runtime/20261102_animation_hints292/native_main_{address:08x}.c'
        source.parent.mkdir(parents=True, exist_ok=True)
        assert not source.exists()
        source.write_text(text, encoding='utf-8')
        try:
            compiled, proof, body = builder.build(source, source.stem, True)
            results.append(dict(passed=True, source=source.relative_to(ROOT).as_posix(),
                sourceSha256=sha256(source), compiledEntry=compiled, genuineLinkProof=proof,
                genuineLinkedBytes=len(body), definedUnsignedHintShift=True))
        except Exception as error:
            results.append(dict(passed=False, source=source.relative_to(ROOT).as_posix(),
                errorType=type(error).__name__, refusal=str(error)))
    write_json(output, dict(sourceCredit=0, results=results, nativeProofAndAcceptancePending=True))
    print(dict(candidates=len(results), genuineFunctions=sum(r['passed'] for r in results),
        genuineBytes=sum(r.get('genuineLinkedBytes', 0) for r in results), sourceCredit=0))


if __name__ == '__main__':
    main()
