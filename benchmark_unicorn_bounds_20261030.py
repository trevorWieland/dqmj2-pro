import argparse
import hashlib
import json
import random
import struct
import subprocess
import sys
import time
from project import ROOT, configuration, now, sha256, write_json


def profile(mode):
    from project import native_dependencies
    native_dependencies(configuration())
    from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_PROT_READ, UC_PROT_EXEC, UcError
    from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
    native = ROOT / 'extract/arm9/arm9.bin'
    code = native.read_bytes()[0x7DAA0:0x7DAC8]
    states, controls = [], []
    start = time.perf_counter()
    for case in range(64):
        data = random.Random(20261030 + case).randbytes(140)
        uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        for base, size in [(0x0207D000, 4096), (0x03000000, 65536), (0x03E00000, 65536), (0x05000000, 4096)]:
            uc.mem_map(base, size, UC_PROT_ALL)
        uc.mem_write(0x0207DAA0, code)
        uc.mem_protect(0x0207D000, 4096, UC_PROT_READ | UC_PROT_EXEC)
        uc.mem_write(0x03000000, data)
        for index in range(13):
            uc.reg_write(UC_ARM_REG_R0 + index, 0xA0000000 + index)
        uc.reg_write(UC_ARM_REG_R0, 0x03000000)
        uc.reg_write(UC_ARM_REG_SP, 0x03E0FFF0)
        uc.reg_write(UC_ARM_REG_LR, 0x05000000)
        uc.emu_start(0x0207DAA0, 0x05000000, timeout=1000000 if mode == 'timer' else 0, count=20000)
        registers = [uc.reg_read(UC_ARM_REG_R0 + i) for i in range(13)]
        assert uc.reg_read(UC_ARM_REG_PC) == 0x05000000 and uc.reg_read(UC_ARM_REG_SP) == 0x03E0FFF0
        assert registers[0] == sum(struct.unpack('<35I', data)) & 0xFFFFFFFF
        assert registers[4:] == [0xA0000000 + i for i in range(4, 13)]
        assert bytes(uc.mem_read(0x03000000, 140)) == data
        states.append({'registers': registers, 'cpsr': uc.reg_read(UC_ARM_REG_CPSR),
                       'sp': uc.reg_read(UC_ARM_REG_SP), 'lr': uc.reg_read(UC_ARM_REG_LR),
                       'pc': uc.reg_read(UC_ARM_REG_PC),
                       'ramSha256': hashlib.sha256(uc.mem_read(0x03000000, 65536)).hexdigest(),
                       'sentinelPageSha256': hashlib.sha256(uc.mem_read(0x05000000, 4096)).hexdigest(),
                       'stackSha256': hashlib.sha256(uc.mem_read(0x03E00000, 65536)).hexdigest()})
        if case == 0:
            uc.reg_write(UC_ARM_REG_R0, 0x03000000)
            uc.emu_start(0x0207DAA0, 0x05000000, timeout=0, count=1)
            assert uc.reg_read(UC_ARM_REG_PC) != 0x05000000
            controls.append({'kind': 'instruction-cap', 'actualReturns': 0})
            uc.reg_write(UC_ARM_REG_R0, 0xDEAD0000)
            try:
                uc.emu_start(0x0207DAA0, 0x05000000, timeout=0, count=20000)
            except UcError:
                assert uc.reg_read(UC_ARM_REG_PC) != 0x05000000
                controls.append({'kind': 'unmapped-input', 'actualReturns': 0})
            else:
                raise AssertionError('Unmapped input was accepted')
    return {'mode': mode, 'seconds': time.perf_counter() - start, 'actualReturns': 64,
            'states': states, 'controls': controls, 'nativeSha256': sha256(native),
            'instructionCapPerCall': 20000, 'freshMachines': 64}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--child', choices=['timer', 'count'])
    parser.add_argument('--deadline-control', action='store_true')
    args = parser.parse_args()
    if args.deadline_control:
        while True:
            pass
    if args.child:
        print(json.dumps(profile(args.child)))
        return
    results = []
    for mode in ['timer', 'count']:
        result = subprocess.run([sys.executable, __file__, '--child', mode], cwd=ROOT,
                                capture_output=True, text=True, timeout=30, check=True)
        results.append(json.loads(result.stdout))
    assert results[0]['states'] == results[1]['states'] and results[0]['controls'] == results[1]['controls']
    try:
        subprocess.run([sys.executable, __file__, '--deadline-control'], cwd=ROOT,
                       capture_output=True, timeout=1, check=True)
    except subprocess.TimeoutExpired:
        deadline_rejected = True
    else:
        raise AssertionError('External child deadline did not terminate control')
    report = {'createdUtc': now(), 'generatorSha256': sha256(__file__), 'passed': True,
              'results': results, 'sameCompleteObservedStates': True, 'deadlineControlRejected': deadline_rejected,
              'measuredSpeedup': results[0]['seconds'] / results[1]['seconds'],
              'adoptedForAcceptance': False, 'decompiledSourceCredit': 0,
              'limitations': ['Checksum-only throughput/parity experiment; no VM workload adoption or legacy fixture changes']}
    write_json(ROOT / 'evidence/tools/unicorn-bounds-benchmark-20261030.json', report)
    print({key: value for key, value in report.items() if key != 'results'})


if __name__ == '__main__':
    main()
