import hashlib
import random
import struct
import time

from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put, u32
from mechanics_save_record_update_oracle import lookup
import mechanics_save_runtime_view_oracle as view_model
import mechanics_save_runtime_refresh_oracle as refresh_model

EKT = 0x02500000
SKILL = 0x02510000
FEAT = 0x02520000
RECORDS = 0x021bd674
VIEWS = 0x021c1b74
MODE = 0x020f69e8
STOP = 0x027ff800
RETAINED = {address: value for address, value in refresh_model.RETAINED.items() if address != 0x02044ff4}
SAVED_REGISTERS = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm, matches):
    available = refresh_model.dependencies(root, arm, matches)
    wanted = {int(relocation['target'], 16) for row, code in matches.values() for relocation in row.get('relocations', []) if relocation['type'] in (1, 28, 29)}
    result = {}
    while wanted:
        address = wanted.pop()
        if address in result or address in RETAINED:
            continue
        if address not in available:
            raise AssertionError(('Reserve refresh unresolved callee', hex(address)))
        row, code = available[address]
        result[address] = (row, code)
        wanted.update(int(relocation['target'], 16) for relocation in row.get('relocations', []) if relocation['type'] in (1, 28, 29))
    return result

def expected(memory, arm, blobs, mode, arguments):
    if mode in (0, 3, 5, 6, 7, 8):
        previous = view_model.VIEW
        try:
            for index in range(3):
                record = lookup(memory, u32(memory, 0x021bd54c + index * 4))
                view_model.VIEW = VIEWS + index * 528
                view_model.expected(memory, arm, *blobs, record or 0, 0)
        finally:
            view_model.VIEW = previous
    elif mode == 4:
        write(memory, VIEWS, bytes(1584))
        for index in range(3):
            write(memory, VIEWS + index * 528 + 46, b'\xff\xff')
    elif mode == 1:
        for index, value in enumerate(arguments):
            write(memory, VIEWS + index * 528 + 46, struct.pack('<H', value & 65535))

def validate(arm, save, matches, root):
    reused = dependencies(root, arm, matches)
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*reused.values(), *matches.values()]:
                machine.mem_write(int(row['address'], 16), code)
        machines.append(machine)
    rom = NintendoDSRom((root / 'inputs/game.nds').read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'SkillTbl.bin', 'FeatTbl.bin')}
    blobs = assets['EnmyKindTbl.bin'][8:], assets['SkillTbl.bin'], assets['FeatTbl.bin']
    rng = random.Random(20261027)
    groups = ([1, 2, 3], [0, 0, 0], [1, 0, 3], [3, 1, 1], [0xffffffff, 2, 0], [0, 2, 3], [0, 0, 3], [3, 2, 1])
    vectors = [(mode, pattern, (0, 139, -1), pattern % 512) for mode in range(256) for pattern in range(8)]
    vectors += [(0, 0, (0, 0, 0), species) for species in range(512)]
    vectors += [(1, pattern, arguments, 139) for pattern in range(8) for arguments in ((-32768, -1, 0), (511, 139, 0), (65536, 65535, -65536), (0x7fffffff, -0x80000000, 32767))]
    cases = calls = 0
    for mode, pattern, arguments, species in vectors:
        original = {0x020f6900: bytearray(rng.randbytes(0x1000)), 0x021bd000: bytearray(rng.randbytes(0x6000)), 0x021c6700: bytearray(rng.randbytes(0x1000)), EKT: bytearray(blobs[0] + bytes(0x10000 - len(blobs[0]))), SKILL: bytearray(blobs[1] + bytes(0x4000 - len(blobs[1]))), FEAT: bytearray(blobs[2] + bytes(0x1000 - len(blobs[2])))}
        write(original, 0x021bd51c, save[0x90:0x3a68])
        for index in range(100):
            data = bytearray(rng.randbytes(132))
            struct.pack_into('<IhB', data, 20, index + 1, (species + index) % 512, index % 3)
            data[122:132] = bytes([1, 0, 2, 255, 128, 100, 255, 255, 0, 0])
            write(original, RECORDS + index * 132, bytes(data))
        write(original, 0x021bd54c, struct.pack('<III', *groups[pattern]))
        write(original, MODE, bytes([mode]))
        put(original, 0x020f69f0, EKT)
        put(original, 0x021c673c, SKILL)
        put(original, 0x021c6740, 256)
        put(original, 0x021c6750, FEAT)
        put(original, 0x021c6754, FEAT + 8)
        memory = {address: bytearray(data) for address, data in original.items()}
        expected(memory, arm, blobs, mode, arguments)
        saved_values = [rng.getrandbits(32) for register in SAVED_REGISTERS]
        stack = rng.randbytes(0x10000)
        row, code = next(iter(matches.values()))
        for machine in machines:
            for address, data in original.items():
                machine.mem_write(address, bytes(data))
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED_REGISTERS, saved_values):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), arguments):
                machine.reg_write(register, value & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(int(row['address'], 16), STOP, count=2000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000:
                raise AssertionError(('Reserve refresh execution/stack bounds', mode, pattern, species))
            if [machine.reg_read(register) for register in SAVED_REGISTERS] != saved_values:
                raise AssertionError(('Reserve refresh callee-saved register ABI', mode, pattern, species))
            for address, data in memory.items():
                observed = bytes(machine.mem_read(address, len(data)))
                if observed != data:
                    at = next(index for index, (left, right) in enumerate(zip(observed, data)) if left != right)
                    raise AssertionError(('Reserve refresh views/records/tables/guard RAM', mode, pattern, species, hex(address + at), observed[at], data[at]))
            calls += 1
        cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 2000000, 'elapsedSecondsLimit': 2, 'returnPcAndStackVerified': True, 'calleeSavedR4ThroughR11Verified': True, 'randomizedInitialStack': True, 'independentExpectedReserveViewsAndGuards': True, 'platformStubs': {}, 'transitiveDirectCallClosureChecked': True, 'patchedDependencyFunctions': len(reused), 'retainedNativeDependencies': [{'module': 'main', 'mode': 'ARM', 'address': hex(address), 'bytes': size, 'sha256': sha(arm[address - 0x02000000:address - 0x02000000 + size]), 'role': role} for address, (size, role) in RETAINED.items()], 'expectedModelIdentities': [{'source': name, 'sha256': sha((root / name).read_bytes())} for name in ('mechanics_save_runtime_view_oracle.py', 'mechanics_save_features_oracle.py', 'mechanics_save_action_banks_oracle.py', 'mechanics_save_projection_oracle.py', 'mechanics_save_roster_oracle.py')], 'dependencyLoader': {'source': 'mechanics_save_runtime_refresh_oracle.py', 'sha256': sha((root / 'mechanics_save_runtime_refresh_oracle.py').read_bytes()), 'selectedClosureOnlyPatched': True}, 'assetSha256': {name: sha(blob) for name, blob in assets.items()}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Modes0/3/5/6/7/8 construct three reserve views through real native record lookup and the matched runtime constructor.', 'Mode4 clears all1584 destination bytes and then marks the three species halfwords as-1.', 'Mode1 truncates its three supplied species halfwords and preserves all other bytes; mode2 and every mode9..255 preserve the destination.', 'Every byte mode0..255, all512 species, sparse/missing/duplicate references and full signed-halfword truncation boundaries are tested.', 'The caller returns with its original stack pointer and R4..R11 under randomized incoming stack/register state.'], 'limitations': ['Four SDK memory primitives remain native ARM; all gameplay callees are hash-verified C and no provider or name builder is used.', 'Field/mode labels remain technical and no ownership, full battle flow or legal species marker bounds are established.', 'The output buffer is separate and valid; overlap and invalid species/pointer dereferences are outside this proof.', 'No new save-byte semantics or original inputs are changed.']}
