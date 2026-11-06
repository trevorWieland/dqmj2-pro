import re
import match_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import measured_module
import match_main_oam_reference296_closed_20261101 as builder


def main():
    output = ROOT / 'evidence/attempts/main-arrange760-typed-storage-20261102.json'
    assert not output.exists()
    original = ROOT / 'nonmatching/main/20261102-arrange760-ordinary-clz/native_main_02036538.c'
    text = original.read_text(encoding='utf-8')
    seed = next(r for r in read_json(ROOT / 'evidence/attempts/main-nitrosystem-masked-candidates-20261101.json')['candidates']
        if r['identity']['address'] == '0x2036538' and r['profile'] == 'base4p')
    _, image, _ = measured_module('main')
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    helper = next(decoder.disasm(image[0x36538 + 176:0x36538 + 180], 0x02036538 + 176)).operands[0].imm
    text = re.sub(r'\bOBJSizeToShape\b', f'native_fn_{helper:08x}', text)
    target = int.from_bytes(image[0x36538 + 748:0x36538 + 752], 'little')
    pattern = r'const static ObjectSize objs\[4\]\[4\]\s*=\s*\{.*?\};'
    text, count = re.subn(pattern, f'extern const ObjectSize native_data_main_{target:08x}[4][4];', text, flags=re.S)
    assert count == 1
    text = re.sub(r'\bobjs\b', f'native_data_main_{target:08x}', text)
    source = ROOT / 'nonmatching/main/20261102-arrange760-typed-storage/native_main_02036538.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(text, encoding='utf-8')
    builder.WORK = ROOT / 'work/main-arrange760-typed-storage-20261102'
    result = dict(sourceCredit=0, source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
        ordinaryCClz=True, originalStaticDataCredit=0, helper=hex(helper), table=hex(target), nativeReturns=0)
    try:
        row, proof, body = builder.build(source, source.stem, True)
        result.update(genuineExact=True, compiledEntry=row, genuineLinkProof=proof, linkedBytes=len(body))
    except Exception as error:
        result.update(genuineExact=False, errorType=type(error).__name__, refusal=str(error))
    write_json(output, result)
    print(dict(genuineExact=result['genuineExact'], sourceCredit=0, ordinaryCSourceLines=len(text.splitlines())))


if __name__ == '__main__':
    main()
