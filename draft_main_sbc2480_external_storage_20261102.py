import hashlib
import re
import match_runtime as compiler
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from slice_reference_sdk_entities_v3_20261102 import functions


def main():
    report = ROOT / 'evidence/attempts/main-sbc2480-external-storage-20261102.json'
    assert not report.exists()
    previous = read_json(ROOT / 'evidence/attempts/main-sdk-visibility-v4-breadth-20261102.json')
    selected = {0x020308EC, 0x02030BF4, 0x02031800}
    _, image, _ = measured_module('main')
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    results = []
    for item in previous['compilation']:
        seed = item.get('candidate')
        if not seed or int(seed['identity']['address'], 0) not in selected: continue
        address = int(seed['identity']['address'], 0)
        original = ROOT / item['source']
        assert sha256(original) == item['sourceSha256']
        text = original.read_text(encoding='utf-8')
        aliases, storage = {seed['referenceFunction']: f'native_main_{address:08x}'}, []
        with (ROOT / seed['object']).open('rb') as stream:
            elf = ELFFile(stream)
            symbols = {s.name: s for s in elf.get_section_by_name('.symtab').iter_symbols()}
            for rel in seed['relocations']:
                offset, kind = rel['offset'], rel['type']
                native = image[address - 0x02000000 + offset:address - 0x02000000 + offset + 4]
                if kind == 1:
                    ins = next(decoder.disasm(native, address + offset))
                    assert ins.operands[0].type == 2
                    alias = f'native_fn_{ins.operands[0].imm & ~1:08x}'
                    name = rel['symbol']
                elif kind == 2:
                    target = (int.from_bytes(native, 'little') - rel['explicitAddend']) & 0xFFFFFFFF
                    alias, name = f'native_data_main_{target:08x}', rel['symbol']
                    if '$' in name:
                        symbol = symbols[name]
                        start, length = symbol['st_value'], symbol['st_size']
                        values = elf.get_section(symbol['st_shndx']).data()[start:start + length]
                        assert symbol['st_info']['type'] == 'STT_OBJECT' and length % 4 == 0
                        native_values = image[target - 0x02000000:target - 0x02000000 + length]
                        assert values == native_values
                        if not any(s['symbol'] == name for s in storage):
                            storage.append(dict(symbol=name, sourceName=name.split('$')[0], address=hex(target),
                                bytes=length, sha256=hashlib.sha256(values).hexdigest(), sourceDataCredit=0))
                        name = name.split('$')[0]
                else: raise AssertionError(rel)
                assert name not in aliases or aliases[name] == alias
                aliases[name] = alias
        for data in storage:
            pattern = r'\bstatic\s+u32\s+' + re.escape(data['sourceName']) + r'\s*\[\s*\]\s*=\s*\{.*?\};'
            replacement = 'extern u32 ' + data['sourceName'] + '[' + str(data['bytes'] // 4) + '];'
            text, count = re.subn(pattern, replacement, text, flags=re.S)
            assert count == 1
        for name, alias in aliases.items(): text = re.sub(r'\b' + re.escape(name) + r'\b', alias, text)
        own = next(r for r in functions(text) if r['name'] == aliases[seed['referenceFunction']])
        folder = ROOT / f'nonmatching/main/20261102-sbc-external-storage/{address:08x}'
        folder.mkdir(parents=True, exist_ok=True)
        header, source = folder / 'types.h', folder / f'native_main_{address:08x}.c'
        header.write_text(text[:own['start']], encoding='utf-8')
        source.write_text('#include "types.h"\n' + text[own['start']:], encoding='utf-8')
        assert all(len(p.read_text(encoding='utf-8').splitlines()) <= 500 for p in [header, source])
        result = dict(identity=seed['identity'], source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
            header=header.relative_to(ROOT).as_posix(), headerSha256=sha256(header), originalStorage=storage, sourceCredit=0)
        old = compiler.FLAGS
        try:
            compiler.FLAGS = seed['compilerFlags']
            compiler.WORK = ROOT / f'work/main-sbc2480-external-storage/{address:08x}/compile'
            rows, _ = compiler.compare(source, 'main', '2', 'off', compiler=ROOT / seed['compiler'])
            assert len(rows) == 1 and not rows[0].get('compileFailed')
            row = rows[0]
            row['sourceDependencies'] = [dict(path=header.relative_to(ROOT).as_posix(), sha256=sha256(header))]
            proof = validate(row, qualified_bindings(row), ROOT / f'work/main-sbc2480-external-storage/{address:08x}/link')
            result.update(genuineExact=True, compiledEntry=row, genuineLinkProof=proof)
        except Exception as error:
            result.update(genuineExact=False, errorType=type(error).__name__, refusal=str(error))
        finally: compiler.FLAGS = old
        results.append(result)
    write_json(report, dict(sourceCredit=0, results=results, actualNativeFunctionReturns=0))
    print(dict(candidates=len(results), genuineExactFunctions=sum(r['genuineExact'] for r in results),
        genuineBytes=sum(r['identity']['bytes'] for r in results if r['genuineExact']), sourceCredit=0))


if __name__ == '__main__':
    main()
