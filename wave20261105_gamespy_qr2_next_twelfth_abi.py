import re
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from project import ROOT,sha256


def verify(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();callbacks=[];repeats=[];literal=None;copy=None
    for row in rows:
        address=int(row['address'],0);native=image[address-0x2000000:address-0x2000000+row['bytes']];instructions=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(native,address));header=ROOT/row['sourceDependencies'][0]['path']
        if address==0x20b6840:
            for target,count,contract in [(0x20b66a4,4,'unsigned32(void)'),(0x20b66e0,2,'unsigned16(socket_word)')]:
                witnesses=[w for w in row['originalNamespaceWitnesses']['witnesses']if w.get('target')==hex(target)]
                if len(witnesses)!=count:raise ValueError('Original repeated-evaluation SDK call count changed')
                repeats.append(dict(caller=row['address'],originalCallee=dict(program='',processor='arm9',module='main',mode='thumb',address=hex(target)),abi=contract,originalCallsites=witnesses,originalCalls=count,reason='Source-visible scalar macro repeats its argument; bounded fixtures supply distinct ordered helper returns',calleeBodiesExecuted=0,calleeSourceOrExecutionCredit=0))
            selected=[i for i in instructions if address+10<=i.address<address+36 and i.mnemonic in ['ldrb','strb']]
            if [i.mnemonic for i in selected].count('ldrb')!=6 or [i.mnemonic for i in selected].count('strb')!=6:raise ValueError('Original straight6-byte copy changed')
            copy=dict(caller=row['address'],ordinaryCOnly=True,originalInstructions=[dict(address=hex(i.address),instruction=i.mnemonic+' '+i.op_str,bytes=i.bytes.hex())for i in selected],assemblyCredit=0,storageAuthorshipCredit=0)
        elif address==0x20b7014:
            raw=native[176:180]
            if int.from_bytes(raw,'little')!=10000:raise ValueError('Actual native partner wait differs')
            published=ROOT/'deps/reference/gamespy-qr2-a2f340195975f4f042e28a60b62561dd9a0b2700/natneg/nninternal.h'
            if not re.search(r'#define\s+PARTNER_WAIT_TIME\s+60000',published.read_text()):raise ValueError('Pinned comparative SDK wait changed')
            literal=dict(caller=row['address'],originalNativeRange=[hex(address+176),hex(address+180)],bytes=raw.hex(),measuredValue=10000,publishedComparisonValue=60000,publishedSource=published.relative_to(ROOT).as_posix(),publishedSourceSha256=sha256(published),meaning='Use measured native build parameter; do not infer complete SDK revision from one constant')
            calls=[i for i in instructions if i.mnemonic=='blx'and re.fullmatch(r'r\d+|ip',i.op_str)]
            for call,(slot,offset,signature)in zip(calls,[('progressCallback',56,'void(state_word,userdata_word)'),('completedCallback',60,'void(result_word,socket_word,peer8*,userdata_word)')]):
                nearby=[dict(address=hex(i.address),instruction=i.mnemonic+' '+i.op_str,bytes=i.bytes.hex())for i in instructions if call.address-30<=i.address<=call.address]
                callbacks.append(dict(caller=row['address'],measuredRecordSlot=slot,measuredRecordOffset=offset,sourceAbi=signature,originalCallsite=hex(call.address),nativeInstruction=call.bytes.hex(),nearbyOriginalSlotAndArgumentFlow=nearby,sourceHeader=header.relative_to(ROOT).as_posix(),sourceHeaderSha256=sha256(header),targetIdentity='Unresolved runtime callback input; no static CPU/program/module/mode/entry inferred',fixtureScope='Synthetic ARM/Thumb/mixed inputs only',calleeSourceOrExecutionCredit=0))
            if len(calls)!=2:raise ValueError('Original INIT handler callback count changed')
    if len(repeats)!=2 or len(callbacks)!=2 or literal is None or copy is None:raise ValueError('Whole SDK ABI/constant qualification incomplete')
    return dict(status='passed',originalCallbackSites=callbacks,repeatedArgumentEvaluation=repeats,originalOrdinaryByteCopy=copy,measuredBuildParameter=literal,negotiationRecordViewBytes=84,sourceWireView='Only packet prefix fields0/1/2 and explicit byte-buffer offsets15..20 are measured; unused published InitPacket tail layout is not recovered',completeObjectOrStorageCredit=0)
