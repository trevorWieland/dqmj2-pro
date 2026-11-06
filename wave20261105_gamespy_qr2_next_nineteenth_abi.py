import re
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from project import ROOT,sha256


def verify(rows):
    indexed={int(row['address'],0):row for row in rows};assert set(indexed)=={0x20b7ea8,0x20b7eec}
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    def decode(lo,hi):return list(cs.disasm(image[lo-0x2000000:hi-0x2000000],lo))
    items=decode(0x20b7f86,0x20b7ff2);calls=[i for i in items if i.mnemonic=='blx'];assert len(calls)==8 and all(i.op_str=='#0x201d5d4'for i in calls)
    original=indexed[0x20b7eec]['originalNamespaceWitnesses']['witnesses'];rng=[w for w in original if w.get('target')=='0x201d5d4'];assert[hex(i.address)for i in calls]==[w['origin']for w in rng]
    required=[('lsls','r1, r6, #0x10'),('orrs','r1, r7'),('lsls','r1, r1, #0x18'),('lsls','r2, r1, #8'),('lsrs','r1, r1, #0x18'),('lsrs','r0, r0, #8'),('str','r0, [r5, r4]')]
    assert all(any((i.mnemonic,i.op_str)==q for i in items)for q in required)
    ring=decode(0x20b7ed2,0x20b7edc);assert(ring[0].mnemonic,ring[0].op_str)==('blx','#0x2026144')and(ring[-1].mnemonic,ring[-1].op_str)==('str','r1, [r5, r0]')
    return dict(status='passed',sourceHeaders=[dict(path=pin['path'],sha256=sha256(ROOT/pin['path']))for row in rows for pin in row['sourceDependencies']],recentMessageAbi=dict(caller='0x20b7ea8',inputWords=2,returnRegister='r0',messageKeyOffset=216,indexOffset=256,capacity=10,actualR1RemainderConsumer='0x20b7eda'),ipVerificationAbi=dict(caller='0x20b7eec',inputWords=3,returnRegister='r0',backendByteOffset=272,backendMask=128,entryOffset=276,entryBytes=16,entryCount=200,duplicateLimit=5),randomMacro=dict(originalCallsites=[dict(address=hex(i.address),bytes=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str)for i in calls],sourceWrittenRandCalls=2,actualNativeRandCalls=8,measuredPairTermOrder=['shift-left24','shift-left8-and-mask','shift-right24-and-low8','shift-right8-and-mask'],pairWordFormula='pairs[k]=(rand[2k]<<16)|rand[2k+1]; result=((pairs[2]>>24)&255)|((pairs[3]>>8)&0xff00)|((pairs[1]<<8)&0xff0000)|((pairs[0]<<24)&0xff000000)',nativeDataFlow=[dict(address=hex(i.address),bytes=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str)for i in items],compilerSpecificEvaluationOrder=True,limits=['No portable C evaluation order is inferred. This is actual original/pinned-compiler behavior for the measured source macro; independent bounded models use eight distinct ordered supplied RNG results.','RNG/buffer/helper bodies, original storage, devices/network and game/platform execution receive no extra source or execution credit.']),calleeSourceOrExecutionCredit=0)
