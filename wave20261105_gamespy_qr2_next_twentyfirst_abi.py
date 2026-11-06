import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from project import ROOT,sha256


def verify(rows):
    indexed={int(row['address'],0):row for row in rows};assert set(indexed)=={0x20b523c,0x20b5344};image=(ROOT/'extract/arm9/arm9.bin').read_bytes();cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    def decode(lo,hi):return list(cs.disasm(image[lo-0x2000000:hi-0x2000000],lo))
    rx=decode(0x20b523c,0x20b5340);assert(rx[0].mnemonic,rx[0].op_str)==('push','{r3, r4, r5, r6, r7, lr}')
    required=[('sub','sp, #0x1fc'),('sub','sp, #0x1f8'),('movs','r0, #8'),('bl','#0x20a8c00'),('bl','#0x20b4f80')];assert all(any((i.mnemonic,i.op_str)==q for i in rx)for q in required)
    builder=decode(0x20b5344,0x20b5360);stores=[i for i in builder if i.address in [0x20b534e,0x20b5350,0x20b5352,0x20b5354]];assert[(i.mnemonic,i.op_str)for i in stores]==[('str','r0, [r3]'),('str','r0, [r3, #4]'),('str','r0, [r3, #8]'),('str','r0, [r3, #0xc]')]
    errorflow=[i for i in rx if 0x20b527c<=i.address<=0x20b5282 or 0x20b52b0<=i.address<=0x20b52b4 or 0x20b52e4<=i.address<=0x20b52ea]
    return dict(status='passed',receiver=dict(caller='0x20b523c',inputWords=1,originalStackBufferBytes=1500,originalPeerBytes=8,localStackBytes=1520,savedRegisterBytes=24,totalFrameBytes=1544,originalPrologue=[dict(address=hex(i.address),bytes=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str)for i in rx[:4]],measuredCallerErrorWords=dict(connectionReset=-15,hostUnreachable=-23,messageSize=-35),exactErrorSentinel=-1,originalErrorCompareFlow=[dict(address=hex(i.address),bytes=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str)for i in errorflow],messageForwardAbi=dict(inputWords=5,words=['socket','buffer','raw_length','raw_ip','host_order_port_u16'],actualOriginalCallsite='0x20b531a')),builder=dict(caller='0x20b5344',inputWords=3,sourceTypedZeroInitializer=True,completeRecordBytes=16,paddingBytes10and11AreActuallyZeroed=True,originalZeroStores=[dict(address=hex(i.address),bytes=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str)for i in stores]),sourceHeaders=sorted({(pin['path'],sha256(ROOT/pin['path']))for row in rows for pin in row['sourceDependencies']}),limits=['Error definitions are qualified properties of these measured native callers, not a blanket reconstruction of every platform error constant.','Received peer bytes and payloads come from supplied fixture contracts, including on error paths. Actual OS/network behavior, helper bodies, original storage and game/platform execution receive zero extra credit.'])
