import re
import struct
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import measured_module
from sequential_overlay_shapes843_20261102 import closing

BASE = ROOT / 'nonmatching/overlay-lane/20261102-geometry871'
EXPORT = ROOT / 'evidence/generated/ghidra868/ov000/export.json'


def comparison(text, address):
    if address == 0x021DEA78:
        old = '''                iVar11 = (int)((ulonglong)lVar7 >> 0x20);
                iVar1 = uStack_c4._4_4_ - iVar11;
                bVar4 = SBORROW4(uStack_c4._4_4_,iVar11);
                iVar11 = uStack_c4._4_4_ - (iVar11 + (uint)bVar34);
                if (iVar11 < 0 == (bVar4 != SBORROW4(iVar1,(uint)bVar34)))'''
        if text.count(old) != 1:
            raise ValueError('871 whole64 comparator shape changed')
        new = '                if ((s64) uStack_c4 >= (s64) lVar7)'
        return text.replace(old, new), dict(before=old, after=new, qualification='Whole signed64 ordering; generated comparator temporaries have no later textual use before loop redefinitions. Full CFG/native behavior remains unproved.')
    for match in re.finditer(r'\bif\s*\(', text):
        opening = text.index('(', match.start())
        end = closing(text, opening, '(', ')')
        old = text[opening + 1:end]
        if 'SBORROW4' not in old:
            continue
        compact = re.sub(r'\s+', '', old)
        if address == 0x021DC374:
            right, borrow = 'iVar10', 'bVar33'
            expected = f'(int)-({right}+(uint){borrow})<0==(SBORROW4(0,{right})!=SBORROW4(-{right},(uint){borrow}))'
            new = f'((s64) 0 - (s64) (s32) {right} - (s64) (u32) {borrow} >= 0)'
        else:
            left, right, borrow, op = {0x021DB15C: ('iVar1', 'iStack_dc', 'bVar34', '!='), 0x021DD54C: ('iVar9', 'iVar12', 'bVar31', '==')}[address]
            expected = f'(int)({left}-({right}+(uint){borrow}))<0{op}(SBORROW4({left},{right})!=SBORROW4({left}-{right},(uint){borrow}))'
            relation = '<' if op == '!=' else '>='
            new = f'((s64) (s32) {left} - (s64) (s32) {right} - (s64) (u32) {borrow} {relation} 0)'
        if compact != expected:
            raise ValueError(('871 whole signed comparator changed', compact))
        return text[:opening + 1] + new + text[end:], dict(before=old, after=new)
    raise ValueError('871 qualified signed comparator missing')


def execute():
    if (BASE / 'queue.json').exists():
        raise ValueError('871 prepared queue already exists')
    export = read_json(EXPORT)
    probePath = ROOT / 'evidence/verification/ghidra-flags869-sites-20261102.json'
    probe = read_json(probePath)
    if not probe['allPassed'] or probe['export']['sha256'] != sha256(EXPORT):
        raise ValueError('871 per-site qualification differs')
    metadata, image, unused = measured_module('ov000')
    if metadata['sha256'] != export['moduleSha256']:
        raise ValueError('871 module identity differs')
    entries = []
    for row in export['functions']:
        address = int(row['address'], 0)
        rawPath = EXPORT.parent / row['generatedC']
        raw = rawPath.read_text(encoding='utf-8')
        start = re.search(r'(?m)^(?:int|uint) ghidra868_', raw).start()
        text = raw[start:].replace('ghidra868_ov000_' + f'{address:x}', f'native_ov000_{address:08x}')
        operations = {}
        for operation in row['unsignedAdditionCarryOperations']:
            key = tuple(value['highName'] for value in operation['inputs'])
            operations.setdefault(key, []).append(operation)
        substitutions = []

        def carry(match):
            key = (match[1], match[2])
            candidates = operations[key]
            if any(op['outputBytes'] != 1 or any(value['bytes'] != 4 or value['highType'] != 'uint' or value['highTypeBytes'] != 4 for value in op['inputs']) for op in candidates):
                raise ValueError('871 unknown-width carry site')
            new = '((u32) (((u64) (u32) ' + key[0] + ' + (u64) (u32) ' + key[1] + ') >> 32))'
            substitutions.append(dict(before=match.group(0), after=new, candidateNativeOperations=candidates, uniqueNativeOrigin=len(candidates) == 1))
            return new

        text = re.sub(r'CARRY4\(\s*(\w+)\s*,\s*(\w+)\s*\)', carry, text)
        if len(substitutions) != len(row['unsignedAdditionCarryOperations']):
            raise ValueError('871 source/p-code carry counts differ')
        text, condition = comparison(text, address)
        if any(marker in text for marker in ['SBORROW4', 'CARRY4', '._4_4_']):
            raise ValueError('871 unsupported generated macro remains')
        helpers = set(re.findall(r'func_0x([0-9a-f]{8})', text))
        names = {key: 'native_fn_' + ('ov000_' if int(key, 16) >= 0x021D7240 else '') + key for key in helpers}
        for key, value in names.items():
            text = text.replace('func_0x' + key, value)
        header = 'typedef unsigned char byte;\ntypedef unsigned char u8;\ntypedef unsigned short u16;\ntypedef unsigned long u32;\ntypedef signed long s32;\ntypedef unsigned long long u64;\ntypedef signed long long s64;\ntypedef unsigned int uint;\ntypedef unsigned long undefined4;\ntypedef unsigned long long undefined8;\ntypedef signed long long longlong;\ntypedef unsigned long long ulonglong;\ntypedef unsigned char bool;\n#define false 0\n#define true 1\n'
        literals = []
        for symbol in sorted(set(re.findall(r'\b[A-Za-z]+Ram[0-9a-fA-F]{8}\b', text))):
            site = int(symbol[-8:], 16)
            value = struct.unpack_from('<I', image, site - 0x021D7240)[0]
            view = 'char *' if symbol.startswith('pcRam') else 's32'
            header += '#define ' + symbol + ' ((' + view + ') 0x' + f'{value:08X}' + 'U)\n'
            literals.append(dict(symbol=symbol, originalLiteralAddress=hex(site), value=hex(value), view=view))
        header += ''.join('extern u32 ' + name + '();\n' for name in sorted(names.values()))
        directory = BASE / f'{address:08x}' / 'qualified-ghidra-flags'
        directory.mkdir(parents=True, exist_ok=False)
        source = directory / 'source.c'
        source.write_text('#include "context.h"\n' + text)
        source.with_name('context.h').write_text(header)
        if len(source.read_text().splitlines()) > 500 or len(header.splitlines()) > 500:
            raise ValueError('871 formatted file exceeds500 lines')
        entries.append(dict(address=hex(address), variant='qualified-ghidra-flags', directory=directory.relative_to(ROOT).as_posix(), sourceSha256=sha256(source), contextSha256=sha256(source.with_name('context.h')), nativeBytes=row['nativeBytes'], sourceCredit=0, carryReplacements=substitutions, wholeComparisonReplacement=condition, nativeLiteralViews=literals))
    write_json(BASE / 'queue.json', dict(schemaVersion=1, sourceCredit=0, functions=entries, exportSha256=sha256(EXPORT), flagProbeSha256=sha256(probePath), limits=['Only explicit same-width p-code addition carries are lowered, with every possible named-variable origin independently tested. One repeated high-name pair has multiple candidate native PCs, recorded as ambiguous rather than silently unique.', 'Whole signed comparison hypotheses preserve ordinary/reversed relations; final whole64 ordering also removes generated comparison temporaries with textual liveness evidence, while full CFG/native behavior remains unproved.', 'Generated signed arithmetic/input domains, helper original formals, layouts and full game behavior remain hypotheses; no function/source/module credit.']))
    print('prepared', len(entries), sum(row['nativeBytes'] for row in entries))


if __name__ == '__main__':
    execute()
