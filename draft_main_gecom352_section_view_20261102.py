import re
import match_runtime as compiler
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings


def main():
    output = ROOT / 'evidence/attempts/main-gecom352-section-view-20261102.json'
    assert not output.exists()
    previous = read_json(ROOT / 'evidence/attempts/main-gecom-declaration-closure-v2-20261102.json')['results']
    _, image, _ = measured_module('main')
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    results = []
    for seed in previous:
        address = int(seed['identity']['address'], 0)
        source = ROOT / seed['source']
        assert sha256(source) == seed['sourceSha256']
        text = source.read_text(encoding='utf-8')
        aliases, base = {seed['referenceFunction']: f'native_main_{address:08x}'}, None
        for rel in seed['relocations']:
            native = image[address - 0x02000000 + rel['offset']:address - 0x02000000 + rel['offset'] + 4]
            if rel['type'] == 1:
                ins = next(decoder.disasm(native, address + rel['offset']))
                aliases[rel['symbol']] = f'native_fn_{ins.operands[0].imm & ~1:08x}'
            else:
                assert rel['type'] == 2 and rel['symbol'] == '.bss' and rel['explicitAddend'] == 0
                target = int.from_bytes(native, 'little')
                assert base is None or base == target
                base = target
        assert base is not None
        text, count = re.subn(r'static NNSG3dGeBuffer \* NNS_G3dGeBuffer = \(\(void \*\)0\)\s*;', '', text)
        assert count == 1
        text = re.sub(r'static volatile int NNS_G3dFlagGXDmaAsync = 0;', '', text)
        text = text.replace('NNS_G3dGeBuffer', f'native_data_main_{base:08x}.buffer')
        text = text.replace('NNS_G3dFlagGXDmaAsync', f'native_data_main_{base:08x}.asyncFlag')
        marker = '} NNSG3dGeBuffer;'
        assert marker in text
        text = text.replace(marker, marker + '\ntypedef struct { NNSG3dGeBuffer *buffer; volatile int asyncFlag; } OriginalGecomState;\nextern OriginalGecomState native_data_main_' + f'{base:08x};', 1)
        for name, alias in aliases.items(): text = re.sub(r'\b' + re.escape(name) + r'\b', alias, text)
        target = ROOT / f'nonmatching/main/20261102-gecom-section-view/native_main_{address:08x}.c'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')
        result = dict(identity=seed['identity'], source=target.relative_to(ROOT).as_posix(), sourceSha256=sha256(target),
            storageBase=hex(base), bufferOffset=0, flagOffset=4, sourceDataCredit=0, sourceCredit=0)
        before = compiler.FLAGS
        try:
            flags = seed['compilerFlags']
            compiler.FLAGS = flags
            compiler.WORK = ROOT / f'work/main-gecom352-section-view/{address:08x}/compile'
            rows, _ = compiler.compare(target, 'main', flags[0][2:], flags[flags.index('-inline') + 1],
                compiler=ROOT / seed['compiler'])
            assert len(rows) == 1 and not rows[0].get('compileFailed')
            row = rows[0]
            proof = validate(row, qualified_bindings(row), ROOT / f'work/main-gecom352-section-view/{address:08x}/link')
            result.update(genuineExact=True, compiledEntry=row, genuineLinkProof=proof)
        except Exception as error:
            result.update(genuineExact=False, errorType=type(error).__name__, refusal=str(error))
        finally: compiler.FLAGS = before
        results.append(result)
    write_json(output, dict(sourceCredit=0, results=results, actualNativeFunctionReturns=0))
    print(dict(candidates=len(results), genuineExactFunctions=sum(r['genuineExact'] for r in results),
        genuineBytes=sum(r['identity']['bytes'] for r in results if r['genuineExact']), sourceCredit=0))


if __name__ == '__main__':
    main()
