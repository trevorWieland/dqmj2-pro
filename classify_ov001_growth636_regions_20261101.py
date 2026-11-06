import json
from project import ROOT, write_json, sha256
from link_runtime_unit import measured_module
ENTRY, SIZE, CODE = 0x0222D240, 1696, 1620


def execute():
    module, image, symbols = measured_module('ov001')
    line = next(line for line in symbols.splitlines() if 'addr:0x0222d240' in line.lower())
    span = image[ENTRY - 0x021D7240:ENTRY - 0x021D7240 + SIZE]
    path = ROOT / 'evidence/attempts/ov001-growth636-functional-source-20261101.json'
    report = json.loads(path.read_text())
    seen = set(report['observedNativeOwnAddresses'])
    if seen != set(range(ENTRY, ENTRY + CODE, 4)):
        raise ValueError('636 original instruction addresses do not close')
    literals = []
    for offset in range(CODE, SIZE, 4):
        address, readers = ENTRY + offset, []
        for index in range(0, CODE, 4):
            word, pc = int.from_bytes(span[index:index + 4], 'little'), ENTRY + index
            if word & 0x0F7F0000 == 0x051F0000 and pc + 8 + ((word & 4095) if word & 0x00800000 else -(word & 4095)) == address:
                readers.append(dict(address=hex(pc), conditionNibble=word >> 28, instructionAddressObserved=pc in seen))
        if not readers or not all(reader['instructionAddressObserved'] for reader in readers):
            raise ValueError('636 literal word lacks observed native reference instruction')
        literals.append(dict(address=hex(address), bytes=4, value=hex(int.from_bytes(span[offset:offset + 4], 'little')), readers=readers))
    write_json(ROOT / 'evidence/verification/ov001-growth636-region-classification-20261101.json', dict(schemaVersion=1, processor='arm9', program='', module='ov001', moduleSha256=module['sha256'], address=hex(ENTRY), mode='arm', bytes=SIZE, canonicalSymbolLine=line, nativeCodeBytes=CODE, nativeReferencedLiteralBytes=SIZE - CODE, unresolvedRegionBytes=0, authoredSourceCredit=0, authoredDataCredit=0, functionBehaviorReport=dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)), codeExitInstructions=[dict(address='0x0222D884', instruction='BL0x0207C73C'), dict(address='0x0222D888', instruction='STRH R0,[R9]'), dict(address='0x0222D88C', instruction='ADD SP,SP,#0x48'), dict(address='0x0222D890', instruction='POP saved registers and PC')], literals=literals, limits=['Code/data classification and observed instruction addresses do not qualify every path, original source boundary provenance, or unresolved inherited-register inputs.', 'The1.25f literal has a conditional EQ reader; conditional read effects are not separately hooked. Category2 is explicitly tested with independent growth effects.', 'This is original-input inventory evidence only. It gives no reconstructed source/data bytes and changes no shared ledger.']))
    print(dict(nativeCodeBytes=CODE, nativeLiteralBytes=SIZE - CODE, sourceCredit=0))


if __name__ == '__main__':
    execute()
