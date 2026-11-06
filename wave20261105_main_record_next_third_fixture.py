import hashlib
import struct
import wave20261104_main_front_eighth_common as H
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC

MODE = 0x020e2f38
BANK = 0x021d682c
STATUS_BASE = 0x02101ae8
STATUS = STATUS_BASE+0xc84


class Machine(H.Machine):
    def store(self,uc,kind,where,size,value,unused):
        if where == MODE and size == 1 or where == STATUS and size == 4:
            self.writes.append(('caller',where,size,value))
        else:
            super().store(uc,kind,where,size,value,unused)


def run(address,code,value,handle):
    machine = Machine(address,code,bytearray(0x8000),[value])
    uc = machine.uc
    uc.mem_write(MODE,b'\x35\x79')
    uc.mem_write(BANK,bytes(range(20)))
    uc.mem_write(BANK+12,struct.pack('<I',handle))
    uc.mem_write(STATUS,struct.pack('<I',0xaabbccdd))
    original_bank = bytes(uc.mem_read(BANK,20))
    stopped = []
    def hook(uc,pc,size,unused):
        if pc == H.STOP:
            stopped.append(pc)
            uc.emu_stop()
        elif pc == 0x0204b61c:
            assert not machine.calls
            words = machine.arguments()[:2]
            assert words == [handle,value&0xffffffff]
            assert uc.mem_read(MODE,2) == bytes([value&255,0x79])
            assert struct.unpack('<I',uc.mem_read(STATUS,4))[0] == 0xaabbccdd
            machine.calls.append(dict(address=hex(pc),arguments=words,modeByteAtEntry=value&255))
            machine.finish_call(0xdeadbeef)
        elif not address <= pc < address+len(code):
            raise AssertionError(('Unexpected native caller boundary',hex(pc)))
    uc.hook_add(UC_HOOK_CODE,hook)
    uc.emu_start(address,H.STOP+4,count=1000)
    assert stopped == [H.STOP] and uc.reg_read(UC_ARM_REG_PC) == H.STOP
    assert len(machine.calls) == 1
    state = machine.snapshot(True)
    assert state['registers'][0] == STATUS_BASE
    assert uc.mem_read(MODE,2) == bytes([value&255,0x79])
    assert bytes(uc.mem_read(BANK,20)) == original_bank
    assert struct.unpack('<I',uc.mem_read(STATUS,4))[0] == 1
    state['modeBytes'] = bytes(uc.mem_read(MODE,2))
    state['bankBytes'] = bytes(uc.mem_read(BANK,20))
    state['statusWord'] = 1
    return state


def prove(address,native,source):
    assert address == 0x020ccb04
    values = list(range(256))+[256,257,0x10000,0x80000000,0xffffffff,0xabcdef00]
    hashes = []
    for index,value in enumerate(values):
        handle = [H.RAM+0x100,0,0x87654320][index%3]
        original = run(address,native,value,handle)
        rebuilt = run(address,source,value,handle)
        assert original == rebuilt
        hashes.append(hashlib.sha256(repr(original).encode()).hexdigest())
    return dict(function=hex(address),cases=len(hashes),actualNativeCallerReturns=len(hashes),actualSourceCallerReturns=len(hashes),
        actualNativeAndSourceCallerReturns=2*len(hashes),independentLowByteStoreAndFullWordForwardingOracle=True,
        allGprsCpsrCalleeSavedStackAndOrderedWritesCompared=True,suppliedNativeCalleeBodiesExecuted=0,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,semanticStateSha256=hashes,
        oracleScope='Low-byte publication preceding the call, unchanged full32-bit second argument, full-word field forwarding and later status store only')
