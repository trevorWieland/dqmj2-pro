import struct
import match_runtime
from project import ROOT, sha256, write_json
from link_runtime_unit import measured_module


def main():
    mainInfo, main, _ = measured_module('main')
    moduleInfo, overlay, _ = measured_module('ov003')

    def words(address, count):
        base, data = (0x02000000, main) if address < 0x021D7240 else (0x021D7240, overlay)
        return list(struct.unpack_from('<' + 'I' * count, data, address - base))

    getters = []
    for address, pointer in [(0x0202A634, 0x020EDEB8), (0x020C36AC, 0x021D4D10), (0x021DAD9C, 0x021E06B8)]:
        expected = [0xE59F0000, 0xE12FFF1E, pointer]
        if words(address, 3) != expected:
            raise ValueError(('795 original constant pointer getter differs', hex(address)))
        getters.append(dict(address=hex(address), mode='arm', bytes=12, observedIncomingWordReads=0, rawR0=hex(pointer), originalWords=[hex(x) for x in expected]))
    setters = []
    for ordinal, address in enumerate(range(0x020C35EC, 0x020C36AC, 32)):
        offset = 4 + ordinal * 4
        expected = [0xE59F1004, 0xE5810000 | offset, 0xE12FFF1E, 0x021D4CF4]
        if words(address, 4) != expected:
            raise ValueError(('795 original setter differs', hex(address)))
        setters.append(dict(address=hex(address), mode='arm', bytes=16, observedR0='full32 store and preserved raw return', destination=hex(0x021D4CF4 + offset), originalWords=[hex(x) for x in expected]))
    copy = [0xE59FC008, 0xE59F1008, 0xE3A02018, 0xE12FFF1C, 0x02008E0C, 0x021E0678]
    if words(0x021DA3E4, 6) != copy:
        raise ValueError('795 original fixed24 copy tail differs')
    half = words(0x021DD5C0, 2)
    if half != [0xE1A02084, 0xE19020B2] or words(0x021DD5F0, 1) != [0x021E038C]:
        raise ValueError('795 original halfword indexed load differs')
    report = dict(schemaVersion=1, sourceCredit=0, romSha256=sha256(ROOT / 'inputs/game.nds'), mainSha256=mainInfo['sha256'], module='ov003', moduleSha256=moduleInfo['sha256'], processor='arm9', program='', mode='arm', address='0x021dd300', bytes=756, constantPointerGetters=getters, fullWordSetters=setters, copyTail=dict(address='0x021da3e4', originalWords=[hex(x) for x in copy], callerSourceRegister='R0', actualDestination='0x021e0678', actualByteCount=24, actualNativeTarget='0x02008e0c'), indexedLoad=dict(shiftPc='0x021dd5c0', loadPc='0x021dd5c4', tableLiteralPc='0x021dd5f0', table='0x021e038c', originalWords=[hex(x) for x in half], operation='R2=(unsigned16)*(R0+(R4<<1)); observed index R4 has low8 of full state word'), limits=['Code/physical interface facts, not original C formal types or game meanings.', 'Complete callback/service effects and ordinary scene eligibility remain unqualified.', 'The synthetic400-pair corpus separately validates contiguous24-byte inputs and all256 low-byte indices; this does not establish legal game enum/table bounds.'], generatorSha256=sha256(__file__))
    write_json(ROOT / 'evidence/abi/ov003-config795-input-loads-20261101.json', report)


if __name__ == '__main__':
    main()
