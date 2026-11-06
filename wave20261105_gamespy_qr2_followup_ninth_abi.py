import hashlib
import re
import match_runtime
from project import ROOT,read_json,sha256
from wave20261105_gamespy_qr2_followup_ninth_bindings import inputs


def verify(rows):
    value,image,inventory,records,imports=inputs()
    expected={0x20b88fc:92}
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
    for at,mnemonic in [(0x20b8904,'cmp'),(0x20b8910,'ldr'),(0x20b8912,'ldr'),(0x20b8914,'ldr'),(0x20b8918,'cmp'),(0x20b891a,'bhs'),(0x20b8926,'adds'),(0x20b8936,'str'),(0x20b8942,'str'),(0x20b894a,'str')]:
        raw=image[at-0x2000000:at-0x2000000+2];ins=list(dis.disasm(raw,at))
        if len(ins)!=1 or ins[0].mnemonic!=mnemonic:raise ValueError('Original typed access/alignment/callback instruction differs')
        instructions.append(dict(origin=hex(at),instruction=raw.hex(),mnemonic=mnemonic,operands=ins[0].op_str))
    return dict(status='passed',callerExtents=expected,providers=providers,nativeInstructionEvidence=instructions,
        bufferBoundary=dict(eventArgumentRegister='R0',eventHeaderBytes=20,discriminatorWordOffset=8,lengthWordOffset=16,continuationWordOffset=12,payloadOffset=20,requestBufferWordOffset=12,requestCapacityWordOffset=20,requestProgressWordOffset=24,requestReturnedWordOffset=36,requestMarkerWordOffset=32),
        unsignedArithmetic='All progress/capacity/length words are unsigned32. Remaining capacity clamps copied bytes when capacity<offset+length. Nonnull modeled destinations satisfy offset<=capacity<=64; null destinations separately qualify wrap/underflow arithmetic without performing copy. No malformed nonnull capacity-overrun safety guarantee.',
        compilerContext='One focused declaration-order change declares offset before length while preserving measured load and expression order; this reproduces original r4/r5 live u32 locals. No flagsweep,registerbinding,assembly or object changes.',
        providerBoundary='Only original ARM copy source/destination/length tuple is supplied; base/continuation mutations are bounded caller contracts. No original callback or copy provider bodies execute.',
        hardwareNetworkQueueThreadGamePlatformExecutionCredit=0)
