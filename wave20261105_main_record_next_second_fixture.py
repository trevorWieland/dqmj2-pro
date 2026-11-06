import hashlib
import itertools
import struct
import wave20261104_main_front_eighth_common as H
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR

INPUT = H.RAM
RECORD = H.RAM+0x100
OTHER = H.RAM+0x200
GETTER_INPUT = 0x021d63c8


def run(address,code,case):
    large = address == 0x020c9c58
    args = [INPUT,case['id'],case['value']] if large else [case['value']] if address == 0x020c9e30 else [INPUT,case['value']]
    machine = H.Machine(address,code,bytearray(0x8000),args)
    uc = machine.uc
    uc.reg_write(UC_ARM_REG_CPSR,((case['flags']&15)<<28)|0x10)
    incoming = bytes(range(16))+bytes([case['flags']])
    uc.mem_write(INPUT,incoming)
    uc.mem_write(GETTER_INPUT,incoming)
    uc.mem_write(RECORD+0x14,struct.pack('<Ih',case['id'],case['short']))
    uc.mem_write(OTHER+0x14,struct.pack('<Ih',case['id']^0x55aa0055,0x1234))
    expected = []
    signed_flag = H.signed(case['flags'] if case['flags'] < 128 else case['flags']-256)&0xffffffff
    def add(target,words,result=0x12345678):
        expected.append(dict(address=target,words=[value&0xffffffff for value in words],result=result&0xffffffff))
    if large:
        add(0x02062a10,[case['id']],RECORD)
        add(0x02062a10,[case['id']],RECORD)
        add(0x020c9984,[1,signed_flag,12,1,5,25,8,1,0])
        add(0x020c9984,[13,signed_flag,1,2,6,23,2,0,1])
        add(0x020c9a3c,[13,9,1,6,16])
        add(0x02072f48,[case['short']])
        add(0x020c9984,[14,signed_flag,7,2,8,23,2,0,1])
        add(0x020c9a3c,[14,9,1,21,16])
        add(0x02062aa0,[],case['count'])
        condition = case['count'] == 1 and case['equal']
        if case['count'] == 1:
            add(0x02062a50,[0],RECORD if case['equal'] else OTHER)
        if not condition:
            add(0x020629e0,[],case['otherCount'])
        selected = 3 if condition or case['otherCount'] == 1 else 1
        add(0x020c9984,[15,signed_flag,7,2,10,23,2,0,1])
        add(0x020c9a3c,[15,9,1,7,16])
        add(0x020c9c10,[2,selected])
        add(0x020c9a84,[INPUT,3,3,13,5,7,case['value']],case['result'])
    else:
        selector = 0 if address == 0x020c9e30 else 2
        if selector == 0:
            add(0x020c8fa8,[],GETTER_INPUT)
        add(0x020c9984 if selector == 0 else 0x020ccd44,[selector,signed_flag,127,1,1,20,2,1,1])
        add(0x020c9a3c if selector == 0 else 0x020cce5c,[selector,9,1,case['value'],8],case['result'])
    stopped = []
    def hook(uc,pc,size,unused):
        if pc == H.STOP:
            stopped.append(pc)
            uc.emu_stop()
            return
        if not address <= pc < address+len(code):
            index = len(machine.calls)
            assert index < len(expected)
            call = expected[index]
            assert pc == call['address'],('Wrong provider order',hex(pc),hex(call['address']))
            words = machine.arguments()[:len(call['words'])]
            if len(call['words']) > 4:
                stack = uc.reg_read(H.REGISTERS[13])
                words.extend(struct.unpack('<'+'I'*(len(call['words'])-4),uc.mem_read(stack,4*(len(call['words'])-4))))
            assert words == call['words'],('Wrong original register/stack slot',hex(pc),words,call['words'])
            machine.calls.append(dict(address=hex(pc),arguments=words,returnedWord=call['result']))
            machine.finish_call(call['result'])
    uc.hook_add(UC_HOOK_CODE,hook)
    uc.emu_start(address,H.STOP+4,count=5000)
    assert stopped == [H.STOP] and uc.reg_read(UC_ARM_REG_PC) == H.STOP
    assert len(machine.calls) == len(expected)
    snapshot = machine.snapshot(True)
    assert snapshot['registers'][0] == case['result']
    assert bytes(uc.mem_read(INPUT,17)) == incoming and bytes(uc.mem_read(GETTER_INPUT,17)) == incoming
    assert bytes(uc.mem_read(RECORD+0x14,6)) == struct.pack('<Ih',case['id'],case['short'])
    assert bytes(uc.mem_read(OTHER+0x14,6)) == struct.pack('<Ih',case['id']^0x55aa0055,0x1234)
    assert all(H.STACK <= where < H.STACK+0x10000 for kind,where,size,value in machine.writes if kind == 'caller')
    return snapshot


def vectors(address):
    words = [0,1,0x7fffffff,0x80000000,0xffffffff,0x12345678]
    cases = []
    if address == 0x020c9c58:
        combinations = itertools.product([0,1,2,0xffffffff],[0,1,2,0xffffffff],[False,True],[-32768,-1,0,32767])
        for index,(count,other,equal,short) in enumerate(combinations):
            cases.append(dict(flags=(index*13)&255,count=count,otherCount=other,equal=equal,short=short,id=(index+1)|0x80000000,
                value=words[index%len(words)],result=words[(index+3)%len(words)]))
    else:
        for flags in range(256):
            cases.append(dict(flags=flags,count=1,otherCount=0,equal=False,short=-1,id=0x87654321,value=words[flags%len(words)],result=words[(flags+3)%len(words)]))
    return cases


def prove(address,native,source):
    hashes = []
    for case in vectors(address):
        original = run(address,native,case)
        rebuilt = run(address,source,case)
        assert original == rebuilt
        hashes.append(hashlib.sha256(repr(original).encode()).hexdigest())
    return dict(function=hex(address),cases=len(hashes),actualNativeCallerReturns=len(hashes),actualSourceCallerReturns=len(hashes),
        actualNativeAndSourceCallerReturns=2*len(hashes),independentAllNineRegisterAndStackWordOracle=True,allGprsCpsrCalleeSavedStackAndOrderedWritesCompared=True,
        suppliedNativeCalleeBodiesExecuted=0,suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,semanticStateSha256=hashes,
        oracleScope='Signed input byte, distinct duplicate middle-slot words, fixed builder records, short-circuit count/equality branches, signed16 payload and unchanged full32-bit forwarding')
