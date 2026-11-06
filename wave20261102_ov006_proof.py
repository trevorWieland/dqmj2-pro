import argparse
import gzip
import hashlib
import json
import os
import random
import re
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'deps/native'))
import unicorn
from unicorn import arm_const as R
from elftools.elf.elffile import ELFFile
import match_runtime as C
import link_runtime_unit as L
from project import configuration, sha256
from recover_linked_runtime import qualified_bindings

LANE = ROOT / 'evidence/lanes/parallel-wave20261102/ov006'
WORK = ROOT / 'work/parallel-wave20261102/ov006/proof'
SOURCE = ROOT / 'src/ov006/parallel_wave20261102'
SP = 0x027F0000
STOP = 0x027E0000
INPUT = 0x02400000
OUTPUT = 0x02401000
CALLBACK_ARM = 0x02670000
CALLBACK_THUMB = 0x02671000
REGS = [R.UC_ARM_REG_R0, R.UC_ARM_REG_R1, R.UC_ARM_REG_R2, R.UC_ARM_REG_R3, R.UC_ARM_REG_R4, R.UC_ARM_REG_R5, R.UC_ARM_REG_R6, R.UC_ARM_REG_R7, R.UC_ARM_REG_R8, R.UC_ARM_REG_R9, R.UC_ARM_REG_R10, R.UC_ARM_REG_R11, R.UC_ARM_REG_R12, R.UC_ARM_REG_SP, R.UC_ARM_REG_LR]
KINDS = {0x021EC8F0:'range', 0x021EDB7C:'compare', 0x021EDC50:'swap32', 0x021EDC90:'swap32', 0x021EDC78:'swap16', 0x021EDCB8:'swap16', 0x021EDAD8:'alloc', 0x021EDAF0:'callback', 0x021EE334:'optional', 0x021EDB9C:'copy', 0x021EDBAC:'fill', 0x021EDE18:'header', 0x021EDBB8:'pointer-word', 0x021EDC20:'raw-word', 0x021EDDF4:'serialize', 0x021EFA70:'initialize'}


def dump(name, value):
    (LANE / name).write_text(json.dumps(value, indent=2) + '\n')


def private_link(row, directory, origin):
    canonical = directory / 'canonical'
    private = directory / 'private'
    private.mkdir(parents=True, exist_ok=True)
    old = (canonical / 'unit.lcf').read_text()
    token = f'CALL: ORIGIN = {int(row["address"], 0):#x} > caller.bin'
    if old.count(token) != 1:
        raise ValueError('Thumb negative LCF origin ambiguous')
    copies = []
    objects = [canonical / 'caller.o'] + sorted(canonical.glob('binding*.o'))
    for path in objects:
        shutil.copyfile(path, private / path.name)
        if sha256(path) != sha256(private / path.name):
            raise ValueError('Private Thumb object copy changed bytes')
        copies.append(dict(name=path.name, sha256=sha256(path)))
    lcf = private / 'unit.lcf'
    lcf.write_text(old.replace(token, f'CALL: ORIGIN = {origin:#x} > caller.bin'))
    if lcf.read_text().replace(f'{origin:#x}', f'{int(row["address"], 0):#x}', 1) != old:
        raise ValueError('Thumb negative LCF changed beyond origin')
    linked = private / 'linked.elf'
    command = [str(L.LINKER), '-nostdlib', '-nodeadstrip', '-interworking', '-proc', 'arm946e', '-main', row['name'], str(lcf), *[str(private / path.name) for path in objects], '-o', str(linked)]
    process = subprocess.run(command, cwd=private, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')), capture_output=True, text=True, timeout=30)
    if process.returncode:
        raise ValueError(('Thumb private link failed', process.stdout, process.stderr))
    body = (private / 'caller.bin').read_bytes()
    with linked.open('rb') as stream:
        elf = ELFFile(stream)
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        caller = next(s for s in symbols if s.name == row['name'])
        if caller['st_value'] != origin or caller['st_size'] != row['compiledBytes'] or len(body) < row['compiledBytes'] or not any(s.name == '$t' and s['st_value'] == origin for s in symbols):
            raise ValueError('Private Thumb entry/extent/mapping differs')
        veneers = [dict(name=s.name, address=s['st_value'], bytes=s['st_size']) for s in symbols if s.name.startswith('$Ven$') and origin + row['compiledBytes'] <= s['st_value'] < origin + len(body)]
        end = origin + row['compiledBytes']
        alignment = []
        for veneer in sorted(veneers, key=lambda v:v['address']):
            if veneer['address'] != end:
                gap = veneer['address'] - end
                padding = body[end - origin:veneer['address'] - origin]
                if gap != 2 or veneer['address'] % 4 or padding not in [bytes(2), bytes.fromhex('c046')]:
                    raise ValueError('Private Thumb veneer gap not verified linker alignment')
                alignment.append(dict(address=end, bytes=gap, hex=padding.hex(), sourceCredit=0))
                end += gap
            end += veneer['bytes']
        if end != origin + len(body):
            raise ValueError('Private Thumb veneer coverage differs')
        for name, binding in qualified_bindings(row).items():
            target = L.verify_binding(name, binding)
            if binding['kind'] == 'function':
                symbol = next(s for s in symbols if s.name == name)
                mode = '$t' if binding['mode'] == 'thumb' else '$a'
                if symbol['st_value'] != target or symbol['st_size'] != 0 or not any(s.name == mode and s['st_value'] == target for s in symbols):
                    raise ValueError('Private Thumb binding mapping changed')
    if any(path.stat().st_size for path in private.glob('binding*.bin')):
        raise ValueError('Private Thumb anchor emitted executable bytes')
    originalRelocations = L.relocation_rows(ROOT / row['object'], row['name'])
    if originalRelocations != L.relocation_rows(private / 'caller.o', row['name']):
        raise ValueError('Private Thumb source relocation/addend/H-bit payload changed')
    return dict(privateAddress=hex(origin), mode='thumb', privateBytes=len(body), sourceCallerBytes=row['compiledBytes'], generatedLinkerVeneers=veneers, generatedAlignmentPadding=alignment, linkerVeneerSourceCredit=0, copiedObjects=copies, originalRelocations=originalRelocations, originalRelocationTypesAddendsAndHBitsUnchanged=True, linkerSha256=sha256(L.LINKER), lcfSha256=sha256(lcf), linkedElfSha256=sha256(linked), callerBinarySha256=sha256(private / 'caller.bin'), sourceCredit=0, nativeBytesOverwritten=0), body


def build(item, source, directory, origin=None):
    C.WORK = directory / 'compile'
    rows, unused = C.compare(source, 'ov006', item['optimization'], 'off', item['speed'], thumb=True, compiler=ROOT / item['compilerPath'])
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('Ov006 compilation failed', rows))
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    try:
        proof = L.validate(row, qualified_bindings(row), directory / 'canonical')
    except ValueError as error:
        if origin is None:
            raise
        proof = error.args[0]
    if origin is not None:
        private, body = private_link(row, directory, origin)
        return dict(source=row, canonicalComparison=proof, privateLink=private), body
    row['manualRelocationComparison'] = dict(exact=row['exactAfterDeclaredRelocation'], matchingBytes=row['matchingBytes'])
    row['exactAfterDeclaredRelocation'] = proof['exactCallerBytes']
    row['exactAfterDeclaredRelocationBasis'] = 'Complete caller bytes after declared relocations resolved by the genuine pinned MW linker, including Thumb BL/BLX interworking; original object/relocation payloads remain unchanged.'
    row['matchingBytes'] = row['bytes']
    row['matchingBytesScope'] = 'Complete genuinely linked caller extent'
    row['realLink'] = proof
    return row, (directory / 'canonical/caller.bin').read_bytes()


def run(item, image, origin, ordinal, overlay):
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_THUMB)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x021D7240, overlay)
    vm.mem_write(origin, image)
    kind = item['kind']
    count = [0, 1, 7, 16, 0xFFFFFFFF, 8, 2, 4][ordinal]
    length = count if count < 32 else 0
    word = [0, 1, 0x12345678, 0xFFFFFFFF, 0x80000000, 0xA5A55A5A, 0x000080FF, 0xABCD0008][ordinal]
    before = bytes([(index * 37 + ordinal) & 255 for index in range(128)])
    vm.mem_write(INPUT, before)
    vm.mem_write(OUTPUT, bytes([0xA5]) * 128)
    values = [word, word ^ 0xA5A5A5A5, word ^ 0x12345678, word ^ 0x80000000]
    literal = struct.unpack_from('<I', overlay, int(item['address'], 0) - 0x021D7240 + item['bytes'] - 4)[0]
    callback = CALLBACK_ARM if ordinal & 1 else CALLBACK_THUMB | 1
    if kind == 'range':
        payload = bytes([[31, 32, 127, 128, 65, 32, 127, 255][ordinal]]) * 32
        vm.mem_write(INPUT, payload)
        values[:2] = [INPUT, count]
    elif kind == 'compare':
        vm.mem_write(OUTPUT, before if ordinal & 1 else bytes([value ^ 1 for value in before]))
        values[:3] = [INPUT, OUTPUT, count]
    elif kind in ['alloc', 'callback', 'optional']:
        vm.mem_write(literal + (4 if kind == 'optional' else 0), struct.pack('<I', 0 if kind == 'optional' and ordinal == 0 else callback))
        if kind != 'optional':
            values[1] = count
    elif kind in ['copy', 'fill', 'header']:
        values[:3] = [OUTPUT, INPUT if kind != 'fill' else word, length]
    elif kind in ['pointer-word', 'raw-word']:
        vm.mem_write(INPUT, struct.pack('<I', word))
    elif kind == 'serialize':
        vm.mem_write(INPUT, struct.pack('<I', 0xABCD0000 | length))
        values[:2] = [INPUT, OUTPUT]
    elif kind == 'initialize':
        values[0] = OUTPUT
    rng = random.Random(ordinal)
    initial = [rng.getrandbits(32) for unused in REGS]
    initial[:4] = values
    initial[13:15] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, 0x30 | ((ordinal & 15) << 28))
    for register, value in zip(REGS, initial):
        vm.reg_write(register, value)
    vm.mem_write(SP - 0x1000, bytes([ordinal]) * 0x1000)
    vm.mem_write(SP, struct.pack('<II', OUTPUT, INPUT if kind == 'pointer-word' else word))
    targets = {int(row['target'], 0) & ~1 for row in item.get('relocations', []) if row['symbol'].startswith('native_fn_')}
    targets.update([CALLBACK_ARM, CALLBACK_THUMB])
    calls, writes, pcs, returned = [], [], [], []
    supplied = 0xAABBCCDD ^ word
    def put(address, payload):
        for offset, byte in enumerate(payload):
            writes.append([address + offset, 1, byte])
        vm.mem_write(address, payload)
    def memory(uc, access, address, size, value, unused):
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    def code(uc, address, size, unused):
        pcs.append(address)
        if address == STOP:
            returned.append(True)
            uc.emu_stop()
        elif address in targets:
            args = [uc.reg_read(register) for register in REGS[:4]]
            stackWord = struct.unpack('<I', bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP), 4)))[0]
            calls.append(dict(address=address, words=args, stackWord=stackWord))
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            result = supplied
            if kind in ['copy', 'header']:
                put(args[1], bytes(uc.mem_read(args[0], args[2])))
            elif kind == 'fill':
                put(args[0], bytes([args[1] & 255]) * args[2])
            elif kind == 'serialize':
                if address == 0x02008BE0:
                    put(args[1], bytes([args[0] & 255]) * args[2])
                else:
                    put(args[1], bytes(uc.mem_read(args[0], args[2])))
            elif kind == 'initialize':
                put(args[0], bytes([0x5A]) * length)
                result = args[0] + length
            for index, register in enumerate(REGS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xCAFE0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, result)
            uc.reg_write(R.UC_ARM_REG_CPSR, 0xA0000010 | (0x20 if lr & 1 else 0))
            uc.reg_write(R.UC_ARM_REG_PC, lr)
    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(origin | 1, STOP + 4, count=5000)
    if not returned:
        raise ValueError(('Ov006 caller return missing', kind, hex(origin)))
    registers = [vm.reg_read(register) for register in REGS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError(('Ov006 callee-saved/SP', kind))
    failures = []
    expectedReturn = supplied
    signedCount = count - 0x100000000 if count & 0x80000000 else count
    if kind == 'range':
        expectedReturn = 0 if signedCount <= 0 or 32 <= payload[0] <= 127 else 0xFFFFFFFF
    elif kind == 'compare':
        left = before[:max(signedCount, 0)]
        right = left if ordinal & 1 else bytes([value ^ 1 for value in left])
        expectedReturn = next((a - b for a, b in zip(left, right) if a != b), 0) & 0xFFFFFFFF
    elif kind.startswith('swap'):
        width = 4 if kind == 'swap32' else 2
        expectedReturn = int.from_bytes((word & ((1 << (8 * width)) - 1)).to_bytes(width, 'little'), 'big')
    elif kind in ['alloc', 'callback', 'optional']:
        expectedCalls = 0 if kind == 'alloc' and signedCount <= 0 or kind == 'optional' and ordinal == 0 else 1
        expectedArgument = values[0] if kind == 'optional' else count
        if len(calls) != expectedCalls or calls and calls[0]['words'][0] != expectedArgument:
            failures.append('Independent callback condition/physical input')
        expectedReturn = 0 if kind == 'optional' or not expectedCalls else supplied
    elif kind == 'copy':
        if not calls or calls[0]['words'][:3] != [INPUT, OUTPUT, length] or bytes(vm.mem_read(OUTPUT, length)) != before[:length]:
            failures.append('Independent source/destination word swap')
    elif kind == 'fill':
        if not calls or calls[0]['words'][:3] != [OUTPUT, word & 255, length] or bytes(vm.mem_read(OUTPUT, length)) != bytes([word & 255]) * length:
            failures.append('Independent low8 fill boundary')
    elif kind == 'header':
        if not calls or calls[0]['words'][:3] != [INPUT, OUTPUT + 4, length] or bytes(vm.mem_read(OUTPUT, 4)) != struct.pack('<I', length):
            failures.append('Independent stored header and offset forwarding')
    elif kind in ['pointer-word', 'raw-word']:
        if bytes(vm.mem_read(OUTPUT, 1)) != bytes([word & 255]) or not calls or calls[0]['words'] != values or calls[0]['stackWord'] != OUTPUT:
            failures.append('Independent low8 output and outgoing fifth word')
    elif kind == 'serialize':
        if len(calls) != 2 or calls[0]['words'][:3] != [0, OUTPUT + 12, 32] or calls[1]['words'][:3] != [INPUT + 4, OUTPUT + 12, length] or bytes(vm.mem_read(OUTPUT + 10, 2)) != struct.pack('<H', length):
            failures.append('Independent low16 length and clear/copy boundary words')
    elif kind == 'initialize':
        expectedReturn = length + 8
        if not calls or calls[0]['words'][0] != OUTPUT + 8 or bytes(vm.mem_read(OUTPUT, 8)) != struct.pack('<H', length) + bytes(6):
            failures.append('Independent zero header and returned extent')
    if registers[0] != expectedReturn:
        failures.append('Independent consumed physical return word')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs, memorySha256=hashlib.sha256(bytes(vm.mem_read(0x02000000, 0x800000))).hexdigest(), modelFailures=failures, actualTopReturn=True)


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Ov006 pinned runtime differs')
    inputs = json.loads((LANE / 'inputs.json').read_text())
    info, overlay, unused = L.measured_module('ov006')
    matches, traces, controls = [], [], []
    for item in inputs['entries']:
        source = ROOT / item['source']
        if sha256(source) != item['sourceSha256'] or sha256(ROOT / item['header']) != item['headerSha256']:
            raise ValueError('Ov006 frozen source/header changed')
        address = int(item['address'], 0)
        match, body = build(item, source, WORK / f'{address:08x}/source')
        item = dict(item, relocations=match['relocations'])
        native = overlay[address - 0x021D7240:address - 0x021D7240 + item['bytes']]
        if native != body:
            raise ValueError('Ov006 genuine linked complete extent differs')
        text = source.read_text()
        if item['kind'] == 'serialize':
            wrong = text.replace('02008be0(0,', '02008be0(1,')
        else:
            wrong = re.sub(r'\breturn ([^;]+);', lambda m: 'return (' + m[1] + ') ^ 1U;', text)
        if wrong == text:
            raise ValueError(('Ov006 negative mutation absent', item['kind']))
        directory = WORK / f'{address:08x}/negative'
        directory.mkdir(parents=True, exist_ok=True)
        wrongSource = directory / source.name
        wrongSource.write_text(wrong)
        wrongSource.with_name('context.h').write_bytes((ROOT / item['header']).read_bytes())
        negative, wrongBody = build(item, wrongSource, directory, 0x02650000)
        control = dict(address=item['address'], proof=negative, rejected=0, positive=0)
        for ordinal in range(8):
            original = run(item, native, address, ordinal, overlay)
            candidate = run(item, body, address, ordinal, overlay)
            if original != candidate or original['modelFailures']:
                dump('model-rejection.json', dict(identity=item, ordinal=ordinal, original=original, candidate=candidate))
                raise ValueError(('Ov006 model/physical comparison', item['address'], ordinal, original['modelFailures']))
            wrongResult = run(item, wrongBody, 0x02650000, ordinal, overlay)
            control['rejected' if wrongResult['modelFailures'] else 'positive'] += 1
            traces.append(dict(address=item['address'], ordinal=ordinal, result=original))
        if not control['rejected']:
            raise ValueError('Ov006 whole-C negative failed to reject')
        controls.append(control)
        matches.append(match)
        print('proved', item['address'], item['bytes'], control['rejected'], flush=True)
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = LANE / 'traces.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', module='ov006', program='', moduleSha256=info['sha256'], allPassed=True, matches=matches, canonicalMatchedFunctions=len(matches), canonicalMatchedBytes=sum(row['bytes'] for row in matches), sourceCreditPendingIntegrator=sum(row['bytes'] for row in matches), cases=len(traces), actualNativeAndSourceCallerReturns=2 * len(traces), completePhysicalRegistersCpsrCallsWritesAndRamEqual=True, negativeEvidence=controls, inputs=dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json')), generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=hashlib.sha256(raw).hexdigest()), producer=Path(__file__).relative_to(ROOT).as_posix(), producerSha256=sha256(Path(__file__)), limits=['Ordinary C Thumb full extents and actual pinned MW relocation/interworking links; manual BL/BLX scoring remains diagnostic. Fresh compilation and canonical report rows are regenerated on every replay.', 'Synthetic bounded RAM, eight fixtures per function. Pure range/compare/endian functions execute without supplied callees. Callback, memory and serializer providers are supplied boundaries with prescribed writes/return/scratch clobbers and zero native callee source/execution credit.', 'Complete GPRs/CPSR/raw call words/ordered writes/8MiB RAM compare, actual caller return sentinels and preserved callee-saved/SP checked. Return through a supplied tail boundary does not claim an original callee returned.', 'Whole-C wrong-return or wrong-clear controls link at a separate Thumb origin with checked mapping/zero-code anchors. No hardware timing, arbitrary aliases, input lengths above fixtures or game meaning claim. Whole-module/ROM admission remains coordinator-owned.'])
    dump('match.json', report)
    print(dict(functions=len(matches), bytes=report['canonicalMatchedBytes'], cases=len(traces)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['execute'])
    globals()[parser.parse_args().action]()
