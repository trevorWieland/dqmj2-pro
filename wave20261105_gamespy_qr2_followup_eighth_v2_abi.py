import hashlib
import re
import match_runtime
from project import ROOT,read_json,sha256
from wave20261105_gamespy_qr2_followup_eighth_bindings import inputs


def verify(rows):
    value,image,inventory,records,imports=inputs()
    expected={0x20b8958:92,0x20b89b4:252,0x20b8ab0:92,0x20b8b0c:80,0x20b8b5c:104,0x20b8bc4:104,0x20b8c2c:80,0x20b8c7c:80}
    if {int(row['address'],0):row['bytes']for row in rows}!=expected:raise ValueError('Qualified control subset differs')
    providers={}
    for row in rows:
        header=next(ROOT/pin['path']for pin in row['sourceDependencies']if pin['path'].endswith('/context.h'))
        text=header.read_text()

        for symbol,binding in row['nativeSymbolEntries'].items():
            if binding['kind']!='function':continue
            at=int(binding['address'],0);mode=binding['mode']
            found=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(%s,size=0x[0-9a-f]+\) addr:0x%08x'%(mode,at),line)),None)
            if found is None:raise ValueError('Original provider namespace/extent absent')
            size=int(re.search(r'size=(0x[0-9a-f]+)',found)[1],0)
            declarations=re.findall(r'\bextern\s+[^;{}]*\b'+re.escape(symbol)+r'\s*\([^;{}]*\)\s*;',text)
            if len(declarations)!=1:raise ValueError(('Actual selected import declaration absent',symbol))
            providers[symbol]=dict(binding=binding,canonicalInventoryRecord=found,bytes=size,originalBodySha256=hashlib.sha256(image[at-0x2000000:at-0x2000000+size]).hexdigest(),sourceDeclaration=declarations[0],actualOriginalProviderBodyExecuted=False,providerSourceCredit=0)
    from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
    dis=Cs(CS_ARCH_ARM,CS_MODE_THUMB);instructions=[]
    for at,mnemonic in [(0x20b89ce,'cmp'),(0x20b89d8,'str'),(0x20b89ec,'str'),(0x20b89f6,'str'),(0x20b8a38,'adds'),(0x20b8a4e,'str'),(0x20b8a58,'str'),(0x20b8a70,'str'),(0x20b8a94,'str'),(0x20b8b8a,'ldr'),(0x20b8bf2,'ldr')]:
        raw=image[at-0x2000000:at-0x2000000+2];ins=list(dis.disasm(raw,at))
        if len(ins)!=1 or ins[0].mnemonic!=mnemonic:raise ValueError('Original typed access/alignment/callback instruction differs')
        instructions.append(dict(origin=hex(at),instruction=raw.hex(),mnemonic=mnemonic,operands=ins[0].op_str))
    if int.from_bytes(image[0xb8b08:0xb8b0c],'little')!=0x20b8dd9:raise ValueError('Original8ab0 callback entry/mode differs')
    return dict(status='passed',callerExtents=expected,providers=providers,originalTypedFunctionPointerViews=imports['functionPointerViews'],nativeInstructionEvidence=instructions,
        controlView=dict(observedAccessBytes=52,activePointerOffset=36,callbackOffset=40,completionOffset=44,rawWordOffset=48,rawWordBytes=4,noCallbackMeaningInferredForWord48=True,earlierFrozenContextsUnchanged=True),
        packetView=dict(backingBytes=1044,lengthOffset=0,magicOffset=4,codeOffset=8,param0Offset=12,param1Offset=16,payloadOffset=20,maximumPayloadBytes=1024,unusedTailIsUninitializedAndNotReadBySuppliedContract=True),
        backingStorageContext='Ordinary typed header pointer overlays actual1044-byte backing array; provider call expressions use the measured backing-array address rather than an equivalent cached pointer. Compiler naturally reproduces original SP recomputation without object or instruction edits.',
        originalCallbackQualification=dict(caller='0x20b8ab0',literalOrigin='0x20b8b08',rawWord='0x20b8dd9',entry='0x20b8dd8',mode='thumb',earlierMismatchingDraftRetainedUncredited=True,allAddressNamedProviderAliasesRequiredToEqualOriginalNativeTarget=True),
        senderBoundary='Unsigned clamp1024; code205 first fragment includes total word;207 continuation stores boolean1 only for further chunks,fragment size andprogress; final supplied wait compares sent count with raw returned word. Failure and zero-length cases qualify caller behavior only.',
        providerCallbackBodiesQueueThreadNetworkSchedulingHardwareGamePlatformExecutionCredit=0)
