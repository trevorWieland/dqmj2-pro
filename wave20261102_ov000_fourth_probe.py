import collections
import re
import shutil
from pathlib import Path

import match_runtime as C
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings

LANE = ROOT / 'evidence/lanes/parallel-wave20261102/overlay000/fourth'
WORK = ROOT / 'work/parallel-wave20261102/overlay000/fourth'
BASE_FLAGS = list(C.FLAGS)
PROFILES = [
    ('o2speed', ['-O2', '-inline', 'off', '-opt', 'speed']),
    ('o3speed', ['-O3', '-inline', 'off', '-opt', 'speed']),
    ('o4pfile', ['-O4,p', '-ipa', 'file', '-inline', 'on,noauto']),
    ('o4all', ['-O4,p', '-ipa', 'file', '-inline', 'all']),
]


def object_body(row):
    with (ROOT / row['object']).open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == row['name'])
        start = symbol['st_value'] & ~1
        return elf.get_section(symbol['st_shndx']).data()[start:start + symbol['st_size']]


def divergence(native, rebuilt, address):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    original = list(decoder.disasm(native, address))
    actual = list(decoder.disasm(rebuilt, address))
    first = next((index for index, (a, b) in enumerate(zip(native, rebuilt)) if a != b), min(len(native), len(rebuilt)))
    first_instruction = first // 4
    contexts = []
    for index in range(max(0, first_instruction - 2), min(first_instruction + 6, len(original), len(actual))):
        a, b = original[index], actual[index]
        contexts.append(dict(offset=index * 4, native=a.mnemonic + ' ' + a.op_str, compiled=b.mnemonic + ' ' + b.op_str))
    mnemonics = ['smull', 'smlal', 'umull', 'umlal', 'mul', 'mla', 'smlabb', 'ldm', 'stm']
    def counts(records):
        counter = collections.Counter(r.mnemonic for r in records)
        return {name:counter[name] for name in mnemonics}
    return dict(firstDifferentByte=first, equalPrefixBytes=first, nativeBytes=len(native), compiledBytes=len(rebuilt), firstDivergenceInstructions=contexts, nativeArithmetic=counts(original), compiledArithmetic=counts(actual), diagnosticOnly=True, sourceCredit=0)


def call_argument_counts(text, name):
    result = []
    for match in re.finditer(r'\b' + re.escape(name) + r'\s*\(', text):
        depth = 1
        commas = 0
        for index in range(match.end(), len(text)):
            if text[index] == '(':
                depth += 1
            elif text[index] == ')':
                depth -= 1
                if not depth:
                    result.append(commas + (1 if text[match.end():index].strip() else 0))
                    break
            elif text[index] == ',' and depth == 1:
                commas += 1
    return result


def run():
    residual = read_json(LANE / 'residual-work.json')['reservedFunctions']
    metadata, image, unused = measured_module('ov000')
    attempts, exact = [], []
    for item in residual:
        address = int(item['address'], 0)
        native = image[address - 0x021D7240:address - 0x021D7240 + item['bytes']]
        original_source = ROOT / item['newSourceTarget']
        text = original_source.read_text()
        context = original_source.with_name('context.h').read_text()
        for compiler_index, compiler in enumerate(C.COMPILER_PINS):
            for label, extra in PROFILES:
                directory = WORK / 'initial-profiles' / format(address, '08x') / (str(compiler_index) + '-' + label)
                directory.mkdir(parents=True, exist_ok=True)
                source = directory / original_source.name
                source.write_text(text)
                source.with_name('context.h').write_text(context)
                C.WORK = directory / 'compile'
                C.FLAGS = BASE_FLAGS + extra
                rows, unused = C.compare(source, 'ov000', BASE_FLAGS[0][2:], BASE_FLAGS[BASE_FLAGS.index('-inline') + 1], compiler=ROOT / compiler)
                result = dict(identity=item['id'], parameters=dict(compiler=compiler, profile=label), sourceCredit=0)
                if len(rows) != 1 or rows[0].get('compileFailed'):
                    result.update(compileFailure=rows)
                    attempts.append(result)
                    continue
                row = rows[0]
                row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
                result['entry'] = row
                try:
                    proof = validate(row, qualified_bindings(row), directory / 'link')
                    result.update(exact=True, realLink=proof)
                    exact.append(result)
                    print('EXACT', hex(address), compiler_index, label, flush=True)
                except Exception as error:
                    result.update(exact=False, linkRefusal=error.args[0] if error.args else str(error))
                linked = directory / 'link/caller.bin'
                body = linked.read_bytes() if linked.exists() else object_body(row)
                result['divergence'] = divergence(native, body, address)
                attempts.append(result)
        relevant = [row for row in attempts if row.get('entry', {}).get('address') == item['address']]
        best = max(relevant, key=lambda r:r['entry']['matchingBytes'])
        print('profiled', item['address'], item['bytes'], 'best', best['entry']['compiledBytes'], best['entry']['matchingBytes'], best['parameters'], flush=True)
        write_json(LANE / 'initial-profiles.json', dict(schemaVersion=1, moduleSha256=metadata['sha256'], attempts=attempts, exact=exact, actualNativeFunctionReturns=0, sourceCredit=0))
    print(dict(exactFunctions=len(exact), exactBytes=sum(row['entry']['bytes'] for row in exact)), flush=True)


if __name__ == '__main__':
    run()
