import re
from project import ROOT, write_json, sha256
import match_main_oam_reference296_closed_20261101 as builder


def main():
    output = ROOT / 'evidence/attempts/main-scene284-store-paths-v2-20261102.json'
    assert not output.exists()
    original = ROOT / 'generated/recovery/20261101-large-profile-breadth21/arm-0203db28.c'
    text = original.read_text(encoding='utf-8')
    text = text.replace('    s8 var_r1;\n', '')
    text = text.replace('        var_r1 = 0x31;', '        native_data_020f6054.field_a = 0x31;')
    text = text.replace('        var_r1 = 2;', '        native_data_020f6054.field_a = 2;')
    text = text.replace('    native_data_020f6054.field_a = var_r1;\n', '')
    function = text[text.index('u32 native_main_0203db28'):]
    for name in set(re.findall(r'extern \w+ (native_fn_\w+)\(\);', text)):
        empty = re.search(r'\b' + name + r'\(\s*\)', function)
        signature = 'void' if empty else 'u32'
        text = re.sub(r'(extern \w+ ' + name + r')\(\);', r'\1(' + signature + ');', text)
    source = ROOT / 'nonmatching/main/20261102-scene284-store-paths-v2/native_main_0203db28.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(text, encoding='utf-8')
    builder.WORK = ROOT / 'work/main-scene284-store-paths-v2-20261102'
    result = dict(sourceCredit=0, source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
        hypothesisOnly=True, nativeReturns=0, interfaceReviewComplete=False)
    try:
        row, proof, body = builder.build(source, source.stem, True)
        result.update(genuineExact=True, compiledEntry=row, genuineLinkProof=proof, linkedBytes=len(body))
    except Exception as error:
        result.update(genuineExact=False, errorType=type(error).__name__, refusal=str(error))
    write_json(output, result)
    print(dict(genuineExact=result['genuineExact'], sourceCredit=0))


if __name__ == '__main__':
    main()
