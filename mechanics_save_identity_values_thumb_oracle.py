import hashlib
import json
import random
import re
import struct
import time

from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from mechanics_save_identity_core_thumb_oracle import expected_code

INPUT = 0x02500040
STOP = 0x027ff800
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def validate(arm, save, matches, root):
    report_path = 'evidence/matches/mechanics-save-identity-core-thumb.json'
    report = json.loads((root / report_path).read_text(encoding='utf-8'))
    dependency = next(row for row in report['matches'] if row['name'] == 'saved_identity_code')
    if sha((root / dependency['source']).read_bytes()) != dependency['sourceSha256'] or sha((root / dependency['object']).read_bytes()) != dependency['objectSha256']:
        raise AssertionError('Identity value constructor source/object differs')
    linked = (root / dependency['isolatedCallerBinary']).read_bytes()
    if sha(linked) != dependency['isolatedCallerBinarySha256'] or linked != arm[0x96e74:0x96ece]:
        raise AssertionError('Identity value constructor actual MW bytes differ')
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            machine.mem_write(0x02096e74, linked)
            for row, code in matches.values():
                actual = (root / row['isolatedCallerBinary']).read_bytes()
                if sha(actual) != row['isolatedCallerBinarySha256'] or actual != code:
                    raise AssertionError('Identity value actual MW caller bytes differ')
                machine.mem_write(int(row['address'], 16), actual)
        machines.append(machine)
    rng = random.Random(2026102781)
    vectors = []
    for position in range(12):
        for byte in range(256):
            text = bytearray(b'123456789012')
            text[position] = byte
            vectors.append(('saved_identity_decimal12', bytes(text), (), None))
    for text in (b'000000000000', b'999999999999', b'000000000001', b'214748364800', b'000000000000\xff', b'123456789012\xff'):
        vectors.append(('saved_identity_decimal12', text, (), None))
    words = (0, 1, 0x7ff, 0x800, 0x1000, 0x1800, 0x7fffffff, 0x80000000, 0xffffffff)
    for first in words:
        for second in words:
            for third in (0, 1, 0xffffffff):
                for name in ('saved_identity_login_words', 'saved_identity_pair_words'):
                    vectors.append((name, struct.pack('<III', first, second, third), (), None))
    for value in words:
        for mask in words:
            for shift in (0, 1, 7, 11, 31):
                vectors.append(('saved_identity_masked_write', rng.randbytes(12), (value, shift, mask), None))
    vectors.append(('saved_identity_masked_write', bytes(12), (1, 0, 0), 'null-rejected'))
    keys = (0, 1, 0xffffffff, 0x4a324a42)
    for identity in words:
        for key in keys:
            for mode in (0, 1):
                code = expected_code(identity, key, mode)
                for corrupt in (0, 1, 1 << 32, 1 << 63):
                    value = code ^ corrupt
                    vectors.append(('saved_identity_code_extract', b'', (value & 0xffffffff, value >> 32, key), None))
    cases = calls = 0
    for name, data, arguments, special in vectors:
        arena = bytearray(rng.randbytes(0x1000))
        arena[0x40:0x40 + len(data)] = data
        expected = bytearray(arena)
        if name == 'saved_identity_decimal12':
            text = data[:12]
            result = int(text) if all(48 <= value <= 57 for value in text) else 0
            inputs = (INPUT,)
        elif name in ('saved_identity_login_words', 'saved_identity_pair_words'):
            first, second, third = struct.unpack('<III', data)
            result = second | (((first & 0x7ff) if name == 'saved_identity_login_words' else third) << 32)
            inputs = (INPUT,)
        elif name == 'saved_identity_masked_write':
            value, shift, mask = arguments
            result = int(not value & ~mask)
            inputs = ((0 if special else INPUT), value, shift, mask)
            if result:
                previous = struct.unpack_from('<I', expected, 0x40)[0]
                changed = (previous & ~((mask << shift) & 0xffffffff)) | ((value << shift) & 0xffffffff)
                struct.pack_into('<I', expected, 0x40, changed)
        else:
            low, high, key = arguments
            code = low | (high << 32)
            result = low if 0 < low < 0x80000000 and any(code == expected_code(low, key, mode) for mode in (0, 1)) else 0
            inputs = arguments
        incoming = [rng.getrandbits(32) for register in SAVED]
        stack = rng.randbytes(0x10000)
        return_thumb = cases & 1
        row, code = matches[name]
        for machine in machines:
            machine.mem_write(0x02500000, bytes(arena))
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, incoming):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), inputs):
                machine.reg_write(register, value & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | return_thumb)
            began = time.monotonic()
            machine.emu_start(int(row['address'], 16) | 1, STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != incoming or bool(machine.reg_read(UC_ARM_REG_CPSR) & 0x20) != bool(return_thumb):
                raise AssertionError(('Identity value bounded return/ABI/state', name, arguments))
            actual = machine.reg_read(UC_ARM_REG_R0)
            if name in ('saved_identity_decimal12', 'saved_identity_login_words', 'saved_identity_pair_words'):
                actual |= machine.reg_read(UC_ARM_REG_R1) << 32
            if actual != result or bytes(machine.mem_read(0x02500000, 0x1000)) != expected:
                raise AssertionError(('Identity value independent number/word/mask/ID model', name, arguments, hex(result), hex(actual)))
            calls += 1
        cases += 1
    malformed = []
    for name, arguments, fault_pc in [('saved_identity_decimal12', (0,), 0x02096f6e), ('saved_identity_login_words', (0,), 0x02096c90), ('saved_identity_pair_words', (0,), 0x02096cac), ('saved_identity_masked_write', (0, 0, 11, 1), 0x02096c7c)]:
        states = []
        for machine in machines:
            machine.mem_write(0x02500000, bytes(0x1000))
            machine.mem_write(0x027f0000, bytes(0x10000))
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), (0, 0, 0, 0)):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), arguments):
                machine.reg_write(register, value)
            for register, value in zip(SAVED, range(8)):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_CPSR, 0x20000010)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            try:
                machine.emu_start(int(matches[name][0]['address'], 16) | 1, STOP, count=1000)
            except UcError:
                if machine.reg_read(UC_ARM_REG_PC) != fault_pc:
                    raise AssertionError(('Identity malformed fault PC', name, hex(machine.reg_read(UC_ARM_REG_PC))))
            else:
                raise AssertionError(('Identity malformed fixture did not fault', name))
            states.append(([machine.reg_read(register) for register in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, *SAVED, UC_ARM_REG_SP)], bytes(machine.mem_read(0x02500000, 0x1000))))
            calls += 1
        if states[0] != states[1]:
            raise AssertionError(('Identity malformed partial state differs', name))
        malformed.append({'name': name, 'module': 'main', 'mode': 'Thumb', 'faultPc': hex(fault_pc)})
        cases += 1
    config = (root / 'config/arm9/symbols.txt').read_text()
    retained = []
    for address, mode in ((0x02026124, 'arm'), (0x02096ee4, 'thumb'), (0x020199e0, 'arm'), (0x02019b58, 'arm'), (0x0200cad0, 'arm'), (0x0200cb10, 'arm'), (0x0200cbd8, 'arm')):
        boundary = re.search(r'kind:function\(' + mode + r',size=(0x[0-9a-f]+)\) addr:0x' + f'{address:08x}' + r'$', config, re.M)
        if not boundary:
            raise AssertionError('Identity value dependency boundary differs')
        size = int(boundary[1], 0)
        retained.append({'module': 'main', 'processor': 'arm9', 'mode': mode, 'address': hex(address), 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size])})
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'actualMwLinkedThumbBytesPatched': True, 'returnPcStackAndCalleeSavedR4ThroughR11Verified': True, 'bothArmAndThumbCallerReturnStatesVerified': True, 'randomizedInitialStack': True, 'independentDecimalUint64MaskAndHashIdModels': True, 'platformStubs': {}, 'retainedNativeEntries': retained, 'reusedAcceptedSources': [{**{key: dependency[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')}, 'report': report_path}], 'expectedMalformedFaults': malformed, 'observations': ['Decimal parsing reads exactly12 signed bytes from right to left, returns0 for any byte outside ASCII0..9, otherwise returns the full64-bit decimal value; a13th byte is ignored.', 'The two readers expose word1 as low32 bits and either word0 low11 bits or word2 as high32 bits.', 'Checked writing rejects value bits outside the supplied mask; accepted0..31 shifts replace only the shifted mask bits and return1. Invalid value bits are rejected before dereferencing a null pointer.', 'The dual-mode extractor accepts CRC or MD5 tagged codes only when the low identity word is positive as signed32-bit, otherwise returns0; independent hash expectations include corrupted tags.', 'Four malformed null cases stop at the same native PCs with identical partial state; every byte value at every decimal position is covered.'], 'limitations': ['The64-bit multiplier,44-byte validator and hash primitives remain native; the accepted code-construction C body supplies the shared checksum projection.', 'Mask shift counts are restricted to0..31 for defined ordinary C shifts.', 'Null dereference cases are isolated machine probes rather than portable C caller contracts.', 'The equality150-byte and validator44-byte source drafts remain unmatched and receive no credit; raw numeric fields establish no decoded identity meaning or SDK/online legality.']}
