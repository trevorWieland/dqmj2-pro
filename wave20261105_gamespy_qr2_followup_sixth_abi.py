import hashlib
import re
import match_runtime
from project import ROOT,read_json,sha256
from wave20261105_gamespy_qr2_followup_sixth_bindings import inputs


def verify(rows):
    value,image,inventory,records,imports=inputs()
    expected={0x20b9848:32,0x20b9898:112,0x20b9998:84,0x20b99ec:92,0x20b9868:46,0x20b9914:132,0x20b9c2c:32}
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
            declarations=[line for line in text.splitlines()if line.startswith('extern ')and re.search(r'\b'+re.escape(symbol)+r'\b',line)]
            if len(declarations)!=1:raise ValueError(('Actual selected import declaration absent',symbol))
            providers[symbol]=dict(binding=binding,canonicalInventoryRecord=found,bytes=size,originalBodySha256=hashlib.sha256(image[at-0x2000000:at-0x2000000+size]).hexdigest(),sourceDeclaration=declarations[0],actualOriginalProviderBodyExecuted=False,providerSourceCredit=0)
    from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
    dis=Cs(CS_ARCH_ARM,CS_MODE_THUMB);instructions=[]
    for at,mnemonic in [(0x20b9882,'ldrsb'),(0x20b98de,'ldrsh'),(0x20b9956,'lsrs'),(0x20b9958,'lsls'),(0x20b9c38,'lsrs'),(0x20b9c3a,'lsls'),(0x20b99d6,'ldr'),(0x20b99dc,'ldr'),(0x20b99de,'ldr'),(0x20b99e0,'ldr'),(0x20b99e2,'blx')]:
        raw=image[at-0x2000000:at-0x2000000+2];ins=list(dis.disasm(raw,at))
        if len(ins)!=1 or ins[0].mnemonic!=mnemonic:raise ValueError('Original typed access/alignment/callback instruction differs')
        instructions.append(dict(origin=hex(at),instruction=raw.hex(),mnemonic=mnemonic,operands=ins[0].op_str))
    return dict(status='passed',callerExtents=expected,providers=providers,originalTypedFunctionPointerViews=imports['functionPointerViews'],nativeInstructionEvidence=instructions,
        statusView=dict(clearedBytes=72,roundedHeaderBytes=96,requestOffset=20,requestBytes=40,oneWordCallbackOffset=60,threeWordCallbackOffset=64,thirdWordOffset=68),
        peerView=dict(bytes=8,lengthOffset=0,familyOffset=1,portOffset=2,addressOffset=4),hostView=dict(bytes=16,signed16LengthOffset=10,addressListOffset=12),
        newConsumerCallbackQualification=dict(callsite='0x20b99e2',functionPointerOffset=64,argumentOffsets=[52,56,68],argumentRegisters=['R0','R1','R2'],actualModes='runtime ARM/Thumb inputs remain unresolved',earlierFrozenProducerOpaqueWordsUnchanged=True,userdataOrGameMeaningInferred=False),
        roundingBoundary='Unsigned32 word addition and LSR/LSL shift expression; wraps before shifts exactly; previous bit-mask source is retained only as uncredited diagnostic',
        allocationBoundary='Original tag53574300,size word,alignment32; provided allocation view and getters determine caller carving; underlying allocations/constructors are supplied only',
        hostProviderPrecondition='Bounded host lengths0/4 preserve signed16 ABI and destination span; malformed negative/oversized host data is not qualified',
        providerBodiesOrRealRandomnessDNSNetworkingThreadsHardwareGamePlatformExecutionCredit=0)
