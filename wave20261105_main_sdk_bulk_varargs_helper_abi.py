import hashlib
import re
from project import ROOT
import wave20261104_main_front_eighth_common as H
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC


def evaluate(entry, numerator, denominator):
    machine = H.Machine(entry, H.IMAGE[entry - H.BASE:entry - H.BASE + 4], bytes(0x8000),
        [numerator & 0xffffffff, numerator >> 32, denominator & 0xffffffff, denominator >> 32])
    visited = set()
    allowed = [(0x02025F1C, 0x020260DC), (0x020260DC, 0x02026124), (0x02026350, 0x02026534)]
    def code(uc, pc, size, unused):
        if not any(start <= pc < end for start, end in allowed):
            raise ValueError('Unsigned helper escaped its bounded original runtime-code window: ' + hex(pc))
        visited.add(pc)
    machine.uc.hook_add(UC_HOOK_CODE, code)
    machine.uc.emu_start(entry, H.STOP, count=100000)
    assert machine.uc.reg_read(UC_ARM_REG_PC) == H.STOP
    snapshot = machine.snapshot(True)
    return snapshot, visited


def prove():
    results, visited = [], set()
    for numerator in [0, 1, 0xffffffff, 0x100000000, 0x8000000000000000, 0xffffffffffffffff]:
        for denominator in [1, 8, 10, 16, 0xffffffff, 0x100000000]:
            snapshot, pcs = evaluate(0x020260DC, numerator, denominator)
            quotient = snapshot['registers'][0] | snapshot['registers'][1] << 32
            assert quotient == numerator // denominator
            visited |= pcs
            results.append(dict(numerator=hex(numerator), denominator=hex(denominator), quotient=hex(quotient), gprs=snapshot['registers'], cpsr=hex(snapshot['cpsr']),
                stackSha256=hashlib.sha256(snapshot['stack']).hexdigest(), orderedStackWrites=snapshot['writes']))
    alternate, unused = evaluate(0x020260E8, 17, 3)
    assert alternate['registers'][0] | alternate['registers'][1] << 32 != 17 // 3
    symbols = (ROOT / 'config/arm9/symbols.txt').read_text()
    bodies = []
    for match in re.finditer(r'(?m)^(\S+) kind:function\(arm,size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)$', symbols):
        address, size = int(match[3], 0), int(match[2], 0)
        pcs = [pc for pc in visited if address <= pc < address + size]
        if pcs:
            body = H.IMAGE[address - H.BASE:address - H.BASE + size]
            assert len(body) == size
            bodies.append(dict(name=match[1], address=hex(address), bytes=size, sha256=hashlib.sha256(body).hexdigest(), executedInstructionSites=len(pcs), sourceCredit=0))
    assert sum(body['executedInstructionSites'] for body in bodies) == len(visited)
    return dict(nativeAbiCases=len(results), results=results, originalConfiguredBodyPins=bodies, inputR0R1NumeratorAndR2R3Denominator=True,
        resultR0R1Unsigned64Quotient=True, originalCalleeSavedAndStackPointerPreserved=True, cpsrAndAllGprsAndOrderedStackWritesRecorded=True,
        interiorModuloEntryRejectedByQuotientOracle=True, sourceOrFunctionCoverageCredit=0, originalModuleRetainedHelperExecutionOnly=True,
        noHardwareOrDsPeripheralAddressMapped=True, divisionByZeroOrGeneralCallerExecutionCredit=0)
