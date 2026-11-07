import struct
import hashlib
import match_runtime
from project import ROOT,read_json,sha256
from qualify_arm7_pm_mic_boundaries_v1_20261106 import bounded_switch
CHANNEL_CALLS={0x027e99d4,0x027e99f0,0x027e9a30,0x027e9a6c,0x027e9ab0,0x027e9ac4,0x027e9b18,0x027e9b38}

def check_callbacks(image,base,start,reached,edges,flow):
    from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
    from capstone.arm import ARM_REG_R9
    words={at:struct.unpack_from('<I',image,at-base)[0]for at in reached}
    assert words[0x027e991c]==0xe3510000
    assert words[0x027e9924]==0x159f9260 and words[0x027e9930]==0x059f9258
    assert struct.unpack_from('<I',image,0x027e9b8c-base)[0]==0x027f4e7c
    assert struct.unpack_from('<I',image,0x027e9b90-base)[0]==0x027f4e1c
    assert {int(c['origin'],0)for c in flow['indirectCalls']}==CHANNEL_CALLS
    assert all(c['targetRegister']=='r9'for c in flow['indirectCalls'])
    for at in range(start+4,0x027e9934,4):assert {a for a,b in edges if b==at}=={at-4}
    reverse={at:set()for at in reached}
    for a,b in edges:reverse[b].add(a)
    todo=list(CHANNEL_CALLS);can_reach_callback=set()
    while todo:
        at=todo.pop()
        if at in can_reach_callback:continue
        can_reach_callback.add(at);todo.extend(reverse[at])
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True
    for at in can_reach_callback:
        ins=next(decoder.disasm(image[at-base:at-base+4],at,count=1))
        if ARM_REG_R9 in ins.regs_access()[1]:assert at in {0x027e9924,0x027e9930}
        if 0x027e991c<at<0x027e9930:assert not ins.update_flags
    for callback in CHANNEL_CALLS:assert {a for a,b in edges if b==callback}=={callback-4}

def walk(row, image, base, kind):
    start, size = int(row['address'], 0), row['bytes']
    assert row['mode']=='arm'and(kind,start,size)in[('channel',0x027e990c,652),('rtc',0x027f60b4,1156)]
    assert sha256(ROOT / row['flow']['path']) == row['flow']['sha256']
    flow = read_json(ROOT / row['flow']['path'])
    assert not any(flow[key] for key in ['unresolved', 'unaccountedRanges', 'tailCalls', 'addressOnlyReferences'])
    assert(kind=='channel'and len(flow['indirectCalls'])==8)or(kind=='rtc'and not flow['indirectCalls'])
    claimed = {int(item['address'], 0): int(item['word'], 0) for item in flow['instructions']}
    assert len(claimed) == len(flow['instructions'])
    todo, reached, loads, returns, edges, switches = [start], set(), [], [], set(), []
    def edge(origin, target):
        edges.add((origin, target)); todo.append(target)
    while todo:
        at = todo.pop()
        if at in reached:
            continue
        assert start <= at < start + size and at % 4 == 0 and at in claimed
        word = struct.unpack_from('<I', image, at - base)[0]
        assert word == claimed[at]; reached.add(at); condition = word >> 28
        assert condition < 15
        if word & 0xfffffff0 == 0x908ff100:
            proof = bounded_switch(image, base, at); switches.append(proof)
            for target in [at + 4] + [int(a, 0) for a in proof['tableAddresses']]:
                edge(at, target)
        elif kind=='channel'and word==0xe12fff19:
            assert at in CHANNEL_CALLS and struct.unpack_from('<I',image,at-base-4)[0]==0xe1a0e00f
            edge(at,at+4)
        elif word & 0x0fffffff == 0x012fff1e:
            returns.append(at)
            if condition != 14:
                edge(at, at + 4)
        elif word & 0x0e000000 == 0x0a000000:
            displacement = (word & 0xffffff) << 2
            if displacement & 0x02000000:
                displacement -= 0x04000000
            target = at + 8 + displacement
            if word & 0x01000000:
                edge(at, at + 4)
            else:
                edge(at, target)
                if condition != 14:
                    edge(at, at + 4)
        else:
            assert word & 0x0ffffff0 != 0x012fff10
            if word & 0x0c000000 == 0:
                assert word >> 12 & 15 != 15
            if word & 0x0c000000 == 0x04000000:
                assert not word & 0x00100000 or word >> 12 & 15 != 15
                if word >> 16 & 15 == 15:
                    assert word & 0x01100000 == 0x01100000 and word & 0x02200000 == 0
                    offset = word & 4095; target = at + 8 + (offset if word & 0x00800000 else -offset)
                    width = 1 if word & 0x00400000 else 4
                    loads.append((at, target, width, image[target - base:target - base + width].hex()))
            if word & 0x0e000000 == 0x08000000:
                assert not word & 0x00100000 or not word & 0x8000
            edge(at, at + 4)
    assert reached==set(claimed)
    assert bool(returns)==(kind=='channel')
    assert all(any(origin==at for origin,target in edges)for at in reached)if kind=='rtc'else True
    if kind=='channel':check_callbacks(image,base,start,reached,edges,flow)
    assert sorted(loads) == sorted((int(r['origin'], 0), int(r['address'], 0), r['bytes'], r['hex']) for r in flow['literalReads'])
    assert len({item[0] for item in loads}) == len(loads)
    for proof in switches:
        at = int(proof['dispatch'], 0)
        assert {origin for origin, target in edges if target == at} == {at - 4}
        original = [item for item in flow['boundedExecutableSwitches'] if item['dispatch'] == proof['dispatch']]
        assert len(original) == 1
        for key in ['compareAddress', 'compareWord', 'dispatchWord', 'defaultWord', 'upper', 'tableAddresses', 'tableWords']:
            assert original[0][key] == proof[key]
    assert len(switches) == len(flow['boundedExecutableSwitches'])
    coverage = bytearray(size)
    for at in reached:
        coverage[at - start:at - start + 4] = b'\x01' * 4
    for origin, target, width, value in loads:
        assert start <= target < target + width <= start + size
        for at in range(target - start, target - start + width):
            assert coverage[at] in [0, 2]; coverage[at] = 2
    assert 0 not in coverage and coverage.count(1) == row['entryReachableInstructionBytes']
    assert coverage.count(2) == row['actualLiteralReadBytes']
    assert hashlib.sha256(image[start - base:start - base + size]).hexdigest() == row['nativeSpanSha256']
    return dict(address=row['address'], bytes=size, instructionBytes=coverage.count(1), literalBytes=coverage.count(2),
        completePerOriginLiteralLoads=len(loads), originalSwitches=switches, dispatchGuardHasOnlyImmediateCmpPredecessor=True,normalReturns=len(returns),graphEdges=sorted(edges))
