import hashlib
import re
import match_runtime
from project import ROOT,read_json,sha256
from wave20261105_dwc_http_next_first_bindings import inputs


def verify(rows):
    value,image,inventory,records,imports=inputs()
    expected={0x20983d0:68,0x2098a7c:56,0x2098ab4:40,0x2098adc:104,0x2098c38:212,0x2098ed8:60,0x2098f14:52,0x2098f48:42,0x2098f74:72}
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
    for at,mnemonic in [(0x20983d8,'ldrb'),(0x20983da,'cmp'),(0x20983ea,'str'),(0x20983f6,'ldr'),(0x2098a84,'ldr'),(0x2098a9c,'str'),(0x2098a9e,'str'),(0x2098aa4,'str'),(0x2098aca,'movs'),(0x2098acc,'movs'),(0x2098ae4,'ldr'),(0x2098ae8,'ldr'),(0x2098b20,'subs'),(0x2098b24,'str'),(0x2098c40,'ldr'),(0x2098c44,'ldr'),(0x2098c4c,'cmp'),(0x2098c4e,'ble'),(0x2098f40,'bhs'),(0x2098f60,'blt')]:
        raw=image[at-0x2000000:at-0x2000000+2];ins=list(dis.disasm(raw,at))
        if len(ins)!=1 or ins[0].mnemonic!=mnemonic:raise ValueError('Original typed access/alignment/callback instruction differs')
        instructions.append(dict(origin=hex(at),instruction=raw.hex(),mnemonic=mnemonic,operands=ins[0].op_str))
    refs=read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/reference.json')
    source=refs['comparativeSource'];assert sha256(ROOT/source['path'])==source['sha256']and source['classification']=='independent-reconstructed-C-not-original-SDK-text'
    for pin in refs['primaryHeaders']:assert sha256(ROOT/pin['path'])==pin['sha256']
    allocator_header=(ROOT/next(p['path']for p in refs['primaryHeaders']if p['path'].endswith('/util_alloc.h'))).read_text(encoding='utf-8')
    assert 'typedef void *(*DWCAuthAlloc)(unsigned long name, long size);'in allocator_header and 'typedef void (*DWCAuthFree)(unsigned long name, void * ptr, long size);'in allocator_header
    return dict(status='passed',callerExtents=expected,providers=providers,nativeInstructionEvidence=instructions,referenceInputs=refs,
        sourceProvenance='Comparative independent reconstructed C,actual published header and complete measured native control flow; not original SDK C. DestroyResult comparative body is empty and contributes no implementation; source body and array_entry tags are measured native reconstruction.',
        bufferLayout=dict(bytes=16,buffer=0,writeIndex=4,tail=8,length=12),publishedHttpPrefix=dict(param=4100,alloc=4112,free=4116),observedHttpViews=dict(initByte=4096,table=6712,tableEntries=32,thread=6968,threadStateWord=7076,mutex=7160,abortWord=7184,fullObservedHeaderViewBytes=7188,unknownPlatformAreaIsOpaque=True),
        callbackBoundary='Primary DWCAuthAlloc(unsignedlong,long) and DWCAuthFree(unsignedlong,void*,long) are two/three32-bit-word calls; native fields loaded before conditional paths. Actual runtime destinations remain unresolved; synthetic ARM/Thumb targets qualify only caller ABI and effects,never callback implementations.',
        addressArithmetic='Buffer growth preserves original unsigned32 address delta in integer arithmetic and converts back to pointer; no subtraction of pointers from distinct allocated objects is used.',
        resultBoundary='Signed index>limit early return; equality remains admitted by original caller. Supplied backing rows cover tested nonnegative indexes; no allocation extent is inferred from limit. Strings,cleanup tags and declared imports match original bytes/modes/entries.',
        boundedProviderLimits='Getter/table/string/allocator/thread-boundary fixtures stop at supplied implementations. Full HTTP thread,SSL,networking,real allocator/free/synchronization/scheduler,game/device/platform and provider execution remain unqualified.',
        originalDataAuthorshipAndAdditionalProviderSourceOrExecutionCredit=0)
