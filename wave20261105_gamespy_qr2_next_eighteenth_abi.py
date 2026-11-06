import re
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from project import ROOT,sha256


def verify(rows):
    indexed={int(row['address'],0):row for row in rows};assert len(indexed)==10
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    def decode(lo,hi):return list(cs.disasm(image[lo-0x2000000:hi-0x2000000],lo))
    init=decode(0x20b718c,0x20b72e0);assert(init[0].mnemonic,init[0].op_str)==('push','{r3, r4, r5, r6, r7, lr}')and(init[1].mnemonic,init[1].op_str)==('sub','sp, #0x40')
    stack=[i for i in init if i.mnemonic=='ldr'and re.fullmatch(r'r\d+, \[sp, #0x[0-9a-f]+\]',i.op_str)]
    offsets={int(re.search(r'#(0x[0-9a-f]+)',i.op_str)[1],0)for i in stack};assert offsets==set(range(88,128,4))
    remainder=decode(0x20b7264,0x20b7270);assert(remainder[0].mnemonic,remainder[0].op_str)==('blx','#0x2026144')and(remainder[-1].mnemonic,remainder[-1].op_str)==('strb','r1, [r0]')
    indirect=[]
    for address,end,slot in [(0x20b73c0,0x20b747c,156),(0x20b78ac,0x20b791c,168)]:
        items=decode(address,end);calls=[i for i in items if i.mnemonic=='blx'and re.fullmatch(r'r\d+|ip',i.op_str)];assert len(calls)==1
        indirect.append(dict(caller=hex(address),callsite=hex(calls[0].address),instruction=calls[0].bytes.hex(),measuredCallbackSlotOffset=slot,sourceAbi='void(word,word,userdata_word)',argumentRegisters=['r0','r1','r2'],targetIdentity='Unresolved runtime callback; synthetic fixture ARM/Thumb targets are not static bindings',calleeSourceOrExecutionCredit=0))
    witnesses={int(row['address'],0):row['originalNamespaceWitnesses']['witnesses']for row in rows}
    think=[w['target']for w in witnesses[0x20b7334]if 'actualMnemonic'in w];assert think==['0x20b73c0','0x20b7360','0x20b8068']
    return dict(status='passed',initializer=dict(caller='0x20b718c',targetSha256=indexed[0x20b718c]['targetSha256'],inputWords=14,registerWords=4,entryStackWords=10,entryStackBytes=40,prologueSavedBytes=24,localStackBytes=64,observedStackLoadOffsetsFromCurrentSP=sorted(offsets),stackArgumentFlow=[dict(address=hex(i.address),instruction=i.mnemonic+' '+i.op_str,bytes=i.bytes.hex())for i in stack],callbackWords='Six incoming function-pointer words stored unchanged; this initializer does not call them',completeRecordCSizeAndAllocationBytes=3476,ipVerifyOffset=276,ipVerifyZeroBytes=3200,globalStorageSourceCredit=0),originalRemainderUse=[dict(address=hex(i.address),instruction=i.mnemonic+' '+i.op_str,bytes=i.bytes.hex())for i in remainder],indirectCallbacks=indirect,thinkOriginalCalleeEntries=think,sourceHeaders=[dict(path=pin['path'],sha256=sha256(ROOT/pin['path']))for row in rows for pin in row['sourceDependencies']],limits=['Native full caller flow, source declarations and bounded supplied-contract models qualify these interfaces only. No original callback/network implementation, OS service, complete game or native platform execution is inferred.'])
