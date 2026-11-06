import ast
import hashlib
import random
import sys
import match_runtime as compiler
import save_link_snapshots
from project import ROOT, configuration, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UC_MEM_WRITE, __version__
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_CPSR
from match_runtime import REGISTERS

COPY, GATE, DATA, STACK, SP, STOP = 0x02021274, 0x0203CF7C, 0x02380000, 0x03030000, 0x03030800, 0x0F000000
FIRST, SECOND = 0x0202AA58, 0x0202AAB4
WORK = ROOT / 'work/main-halfword-zeroarg-20261031'


def recipes():
    return [dict(index=i, length=[0, 1, 2, 3, 7, 31, 127][i % 7], placement=i // 7 % 4,
                 first=[0, 1, 0xFFFFFFFF, 0x80000000][i // 3 % 4]) for i in range(384)]


def initial(entry, item):
    rng = random.Random(entry * 1000 + item['index'])
    data = bytearray(rng.randbytes(4096))
    source = DATA + 0x100
    destination = [DATA + 0x800, source, source - 2, source + 8][item['placement']]
    if destination == source + 8 and item['length'] >= 4:
        destination = DATA + 0x800
    for offset in range(item['length'] + 1):
        value = 0 if offset == item['length'] else [1, 0x20, 0x100, 0x7FFF, 0x8000, 0xFFFF][offset % 6]
        data[source - DATA + offset * 2:source - DATA + offset * 2 + 2] = value.to_bytes(2, 'little')
    before = bytes(data)
    events, calls = [], []
    second = rng.getrandbits(32)
    if entry == COPY:
        reader, writer = source, destination
        for unused in range(129):
            value = int.from_bytes(data[reader - DATA:reader - DATA + 2], 'little')
            events.append([16, reader, 2, value])
            data[writer - DATA:writer - DATA + 2] = value.to_bytes(2, 'little')
            events.extend([[17, writer, 2, value], [16, writer, 2, value]])
            reader += 2
            writer += 2
            if value == 0:
                break
        else:
            raise ValueError('Recipe has no bounded terminator')
        returned = destination
    else:
        calls.append([FIRST, 0])
        if item['first']:
            calls.append([SECOND, 0])
        returned = second if item['first'] else 0
    registers = [rng.getrandbits(32) for unused in REGISTERS]
    registers[:2] = [destination, source]
    registers[13:] = [SP, STOP | (item['index'] & 1)]
    return dict(before=before, expected=bytes(data), events=events, calls=calls,
                returned=returned, second=second, registers=registers)


def execute(original, entry, code, item):
    model = initial(entry, item)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, original)
    uc.mem_write(entry, code)
    uc.mem_write(DATA, model['before'])
    for address in [STACK, STOP]:
        uc.mem_map(address, 4096)
    uc.mem_write(STACK, bytes([0xA5]) * 4096)
    control = 0x10 | ((item['index'] // 16 & 3) << 6)
    uc.reg_write(UC_ARM_REG_CPSR, item['index'] % 16 << 28 | control)
    for register, value in zip(REGISTERS, model['registers']):
        uc.reg_write(register, value)
    events, calls, pcs = [], [], set()
    stopped, instructions = False, 0

    def memory(engine, access, address, width, value, user):
        if DATA <= address < DATA + 4096:
            events.append([access, address, width, value if access == UC_MEM_WRITE else int.from_bytes(engine.mem_read(address, width), 'little')])

    def instruction(engine, address, width, user):
        nonlocal stopped, instructions
        instructions += 1
        if address == STOP:
            stopped = True
            engine.emu_stop()
            return
        if entry == GATE and address in [FIRST, SECOND]:
            calls.append([address, engine.reg_read(REGISTERS[0])])
            lr = engine.reg_read(UC_ARM_REG_LR)
            for index in [1, 2, 3, 12]:
                engine.reg_write(REGISTERS[index], 0xD4600000 + index)
            engine.reg_write(REGISTERS[0], item['first'] if address == FIRST else model['second'])
            engine.reg_write(UC_ARM_REG_CPSR, (len(calls) % 16 << 28) | control)
            engine.reg_write(UC_ARM_REG_PC, lr)
            return
        assert entry <= address < entry + 32, hex(address)
        pcs.add(address)

    uc.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, memory)
    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.emu_start(entry, STOP + 4, count=3000)
    assert stopped and uc.reg_read(UC_ARM_REG_SP) == SP
    assert uc.reg_read(UC_ARM_REG_CPSR) & 255 == control | ((item['index'] & 1) << 5)
    for index in range(4, 12):
        assert uc.reg_read(REGISTERS[index]) == model['registers'][index]
    assert bytes(uc.mem_read(STACK, SP - STACK - 128)) == bytes([0xA5]) * (SP - STACK - 128)
    assert bytes(uc.mem_read(SP, 4096 - (SP - STACK))) == bytes([0xA5]) * (4096 - (SP - STACK))
    data = bytes(uc.mem_read(DATA, 4096))
    return dict(modelPassed=data == model['expected'] and events == model['events'] and calls == model['calls']
                and uc.reg_read(REGISTERS[0]) == model['returned'],
                pageSha256=hashlib.sha256(data).hexdigest(), events=events, suppliedCalls=calls, pcs=sorted(pcs),
                registers=[uc.reg_read(register) for register in REGISTERS], cpsr=uc.reg_read(UC_ARM_REG_CPSR), instructions=instructions)


def main():
    assert sys.version_info[:3] == (3, 13, 5) and __version__ == '2.1.4'
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    unused, original, unused = measured_module('main')
    matches, qualifications = [], []
    for entry in [COPY, GATE]:
        source = ROOT / f'src/runtime/20261031_halfword_and_zeroarg/native_main_{entry:08x}.c'
        directory = WORK / f'{entry:08x}'
        compiler.WORK = directory / 'compile'
        rows, unused = compiler.compare(source, 'main', 2, 'off')
        assert len(rows) == 1
        row = rows[0]
        proof = validate(row, qualified_bindings(row), directory / 'link')
        save_link_snapshots.DIRECTORY = directory / 'immutable-links'
        row.update(save_link_snapshots.freeze_link(proof))
        row.update(exactAfterRealMwLink=True, exactAfterGenuineLink=True, linkedMatchingBytes=32)
        native = original[entry - 0x02000000:entry - 0x02000000 + 32]
        code = (directory / 'link/caller.bin').read_bytes()
        assert code == native
        cases, pcs = [], set()
        for item in recipes():
            first, second = execute(original, entry, native, item), execute(original, entry, code, item)
            assert first == second and first['modelPassed'], (hex(entry), item)
            pcs.update(first['pcs'])
            cases.append(dict(recipe=item, result=first, actualReturns=2))
        text = source.read_text()
        wrong = text.replace('var_r3 += 1;', 'var_r3 += 2;') if entry == COPY else text.replace('extern u32 native_fn_0202aab4(u32);', 'extern u32 native_fn_0202aab4();').replace('native_fn_0202aab4(0);', 'native_fn_0202aab4();')
        assert wrong != text
        negative = ROOT / f'nonmatching/main-runtime/20261031-halfword-zeroarg-negative/{entry:08x}/source.c'
        negative.parent.mkdir(parents=True, exist_ok=True)
        assert not negative.exists() or negative.read_bytes() == wrong.encode()
        negative.write_bytes(wrong.encode())
        compiler.WORK = directory / 'negative-compile'
        bad_rows, unused = compiler.compare(negative, 'main', 2, 'off')
        assert len(bad_rows) == 1
        try:
            validate(bad_rows[0], qualified_bindings(bad_rows[0]), directory / 'negative-link')
        except ValueError as error:
            mismatch = ast.literal_eval(str(error))
        else:
            raise ValueError('Wrong C unexpectedly byte-matched')
        bad = (directory / 'negative-link/caller.bin').read_bytes()
        controls = []
        for item in recipes()[:12]:
            item = dict(item, placement=0)
            good, other = execute(original, entry, native, item), execute(original, entry, bad, item)
            assert good['modelPassed']
            controls.append(dict(recipe=item, original=good, wrong=other, actualReturns=2))
        assert any(not case['wrong']['modelPassed'] for case in controls)
        assert any(case['wrong']['modelPassed'] for case in controls)
        assert len([pc for pc in pcs if entry <= pc < entry + 32]) * 4 == 32
        row['nativeOracle'] = dict(verifiedReturn=True, isolatedState=True, actualReturns=2 * len(cases),
            suppliedCalls=2 * sum(len(case['result']['suppliedCalls']) for case in cases), observedCodeBytes=32)
        matches.append(row)
        qualifications.append(dict(address=hex(entry), cases=cases, negativeControls=controls, wrongC=bad_rows[0], wrongLinkMismatch=mismatch))
    write_json(ROOT / 'evidence/matches/main-halfword-zeroarg-20261031.json', dict(romSha256=config['romSha256'],
        matches=matches, qualifications=qualifications, generator='match_main_halfword_zeroarg_20261031.py', generatorSha256=sha256(__file__),
        limitations=['Backed aligned halfword arrays, bounded terminators and supported overlap; no text encoding claim',
                     'Two conditional-call helper identities are explicit no-memory-write providers; no implementation/heap meaning claim',
                     'No Windows game, Android execution or complete source-only ROM claim']))
    print(dict(functions=2, bytes=64, actualReturns=1536, negativeActualReturns=48))


if __name__ == '__main__':
    main()
