import re
from project import ROOT, write_json, sha256
from slice_reference_sdk_entities_v3_20261102 import functions, slice_closed
import match_main_oam_reference296_closed_20261101 as builder


def main():
    output = ROOT / 'evidence/attempts/main-arrange760-ordinary-clz-20261102.json'
    assert not output.exists()
    raw = ROOT / 'work/main-sdk-visibility-v4-20261102/preprocess/deps-reference-NitroSystem-d636fb5d2b212e8736f09859fff447be2bd0ac85-libraries-g2d-src-g2d_CharCanvas-base4p/expanded.i'
    text = raw.read_text(encoding='utf-8')
    seed = 'NNS_G2dArrangeOBJ1D'
    for row in sorted(functions(text), key=lambda r: r['start'], reverse=True):
        header = text[row['start']:row['opening']]
        if row['name'] == seed or re.search(r'\binline\b', header): continue
        text = text[:row['start']] + re.sub(r'\bstatic\s+', '', header).rstrip() + ';\n' + text[row['end']:]
    text, selection = slice_closed(text, [seed])
    records = functions(text)
    clz = next(r for r in records if r['name'] == 'MATH_CountLeadingZerosInline')
    replacement = '''static inline u32 MATH_CountLeadingZerosInline(u32 x)
{
    u32 n = 0;
    if (!x) return 32;
    if (!(x & 0xffff0000UL)) { n += 16; x <<= 16; }
    if (!(x & 0xff000000UL)) { n += 8; x <<= 8; }
    if (!(x & 0xf0000000UL)) { n += 4; x <<= 4; }
    if (!(x & 0xc0000000UL)) { n += 2; x <<= 2; }
    if (!(x & 0x80000000UL)) ++n;
    return n;
}'''
    text = text[:clz['start']] + replacement + text[clz['end']:]
    text = text.replace(seed, 'native_main_02036538')
    assert not re.search(r'\b(?:asm|__asm|__asm__)\b', text)
    source = ROOT / 'nonmatching/main/20261102-arrange760-ordinary-clz/native_main_02036538.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(text, encoding='utf-8')
    builder.WORK = ROOT / 'work/main-arrange760-ordinary-clz-20261102'
    result = dict(sourceCredit=0, source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
        rawExpandedSourceSha256=sha256(raw), actualNativeFunctionReturns=0, originalAsmRemoved=True)
    try:
        row, proof, body = builder.build(source, source.stem, True)
        result.update(genuineExact=True, compiledEntry=row, genuineLinkProof=proof, linkedBytes=len(body))
    except Exception as error:
        result.update(genuineExact=False, errorType=type(error).__name__, refusal=str(error))
    write_json(output, result)
    print(dict(sourceLines=len(text.splitlines()), genuineExact=result['genuineExact'], sourceCredit=0))


if __name__ == '__main__':
    main()
