import re
import match_runtime as compiler
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings


def main():
    output = ROOT / 'evidence/attempts/main-vram-global-interfaces-20261102.json'
    assert not output.exists()
    old = read_json(ROOT / 'evidence/attempts/main-sdk-visibility-v4-breadth-20261102.json')
    selected = {0x0203BD58, 0x0203BE54, 0x0203BFCC, 0x0203C00C, 0x0203C45C, 0x0203C4BC}
    _, image, _ = measured_module('main')
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    results = []
    for item in old['compilation']:
        seed = item.get('candidate')
        if not seed or int(seed['identity']['address'], 0) not in selected: continue
        if any(q['symbol'].startswith('.') for q in seed['relocations']): continue
        address = int(seed['identity']['address'], 0)
        original = ROOT / item['source']
        assert sha256(original) == item['sourceSha256']
        text = original.read_text(encoding='utf-8')
        aliases, promoted = {seed['referenceFunction']: f'native_main_{address:08x}'}, []
        for rel in seed['relocations']:
            native = image[address - 0x02000000 + rel['offset']:address - 0x02000000 + rel['offset'] + 4]
            if rel['type'] == 1:
                ins = next(decoder.disasm(native, address + rel['offset']))
                target = ins.operands[0].imm & ~1
                alias = f'native_fn_{target:08x}'
            elif rel['type'] == 2:
                target = (int.from_bytes(native, 'little') - rel['explicitAddend']) & 0xFFFFFFFF
                is_function = rel['sourceSymbolType'] == 'STT_FUNC' or rel['symbol'] in [
                    'NNS_GfdAllocFrmTexVram', 'NNS_GfdFreeFrmTexVram']
                alias = f'native_fn_{target & ~1:08x}' if is_function else f'native_data_main_{target:08x}'
            else: raise AssertionError(rel)
            name = rel['symbol']
            if name == seed['referenceFunction']: continue
            assert name not in aliases or aliases[name] == alias
            aliases[name] = alias
            if rel.get('sourceSymbolBinding') == 'STB_LOCAL' and rel.get('sourceSymbolType') == 'STT_OBJECT' and name not in promoted:
                pattern = r'\bstatic\s+([^;{}=]*?\b' + re.escape(name) + r'(?:\s*\[[^\]]*\])?)\s*(?:=\s*\{.*?\})?\s*;'
                text, count = re.subn(pattern, lambda m: 'extern ' + m[1] + ';', text, flags=re.S)
                assert count == 1, (name, count)
                promoted.append(name)
        for name, alias in aliases.items(): text = re.sub(r'\b' + re.escape(name) + r'\b', alias, text)
        folder = ROOT / f'nonmatching/main/20261102-vram-global-interfaces/{address:08x}-{item["profile"]}'
        folder.mkdir(parents=True, exist_ok=True)
        source = folder / f'native_main_{address:08x}.c'
        source.write_text(text, encoding='utf-8')
        assert len(text.splitlines()) <= 500
        result = dict(source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
            identity=seed['identity'], promotedCompleteTypedGlobals=promoted, sourceDataCredit=0, sourceCredit=0)
        flags, before = seed['compilerFlags'], compiler.FLAGS
        try:
            compiler.FLAGS = flags
            compiler.WORK = ROOT / 'work/main-vram-global-interfaces-20261102' / folder.name / 'compile'
            rows, _ = compiler.compare(source, 'main', flags[0][2:], flags[flags.index('-inline') + 1],
                compiler=ROOT / seed['compiler'])
            assert len(rows) == 1 and not rows[0].get('compileFailed')
            row = rows[0]
            proof = validate(row, qualified_bindings(row), ROOT / 'work/main-vram-global-interfaces-20261102' / folder.name / 'link')
            result.update(genuineExact=True, compiledEntry=row, genuineLinkProof=proof)
        except Exception as error:
            result.update(genuineExact=False, errorType=type(error).__name__, refusal=str(error))
        finally: compiler.FLAGS = before
        results.append(result)
    write_json(output, dict(sourceCredit=0, results=results, actualNativeFunctionReturns=0))
    exact = {r['identity']['address']: r for r in results if r['genuineExact']}
    print(dict(profiles=len(results), genuineExactFunctions=len(exact),
        genuineExactBytes=sum(r['identity']['bytes'] for r in exact.values()), sourceCredit=0))


if __name__ == '__main__':
    main()
