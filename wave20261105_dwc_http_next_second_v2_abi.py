import hashlib
import re
import match_runtime
from project import ROOT,read_json,sha256
from wave20261105_dwc_http_next_second_bindings import inputs


def verify(rows):
    value,image,inventory,records,imports=inputs()
    expected={0x209820c:216,0x20982e4:104,0x209834c:132,0x20987b0:128,0x2098954:184}
    if {int(row['address'],0):row['bytes']for row in rows}!=expected:raise ValueError('Qualified control subset differs')
    providers={}
    for row in rows:
        headers=[ROOT/pin['path']for pin in row['sourceDependencies']if pin['path'].endswith('.h')]
        text='\n'.join(path.read_text()for path in headers)

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
    for at,mnemonic in [(0x2098216,'ldr'),(0x209822e,'ldm'),(0x2098230,'stm'),(0x20982a4,'str'),(0x20982a6,'ldr'),(0x20982b4,'ldr'),(0x2098314,'movs'),(0x209836e,'cmp'),(0x209837c,'str'),(0x2098382,'cmp'),(0x2098398,'str'),(0x20983a2,'str'),(0x20987b6,'ldr'),(0x20987b8,'beq')]:
        raw=image[at-0x2000000:at-0x2000000+2];ins=list(dis.disasm(raw,at))
        if len(ins)!=1 or ins[0].mnemonic!=mnemonic:raise ValueError('Original typed access/alignment/callback instruction differs')
        instructions.append(dict(origin=hex(at),instruction=raw.hex(),mnemonic=mnemonic,operands=ins[0].op_str))
    refs=read_json(ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/reference.json')
    source=refs['comparativeSource'];assert sha256(ROOT/source['path'])==source['sha256']and source['classification']=='independent-reconstructed-C-not-original-SDK-text'
    for pin in refs['primaryHeaders']:assert sha256(ROOT/pin['path'])==pin['sha256']
    allocator_header=(ROOT/next(p['path']for p in refs['primaryHeaders']if p['path'].endswith('/util_alloc.h'))).read_text(encoding='utf-8')
    assert 'typedef void *(*DWCAuthAlloc)(unsigned long name, long size);'in allocator_header and 'typedef void (*DWCAuthFree)(unsigned long name, void * ptr, long size);'in allocator_header
    pointer=imports['functionPointerViews'].get('0x2098575')
    if pointer is None or pointer['entry']!='0x2098574'or pointer['mode']!='thumb'or pointer['callers']!=['0x209834c']:raise ValueError('Actual typed original thread entry differs')
    bss=[(at,view)for at,view in imports['dataViews'].items()if view['storage']=='bss']
    if len(bss)!=1 or bss[0][1]['type']!='raw-bool-word'or bss[0][1]['minimumBytes']!=4:raise ValueError('Actual scoped ignoreCA bool word differs')
    return dict(status='passed',callerExtents=expected,providers=providers,nativeInstructionEvidence=instructions,referenceInputs=refs,
        originalTypedThreadEntry=pointer,originalBssBool=bss,sourceProvenance='Independent reconstructed comparative C plus actual published typed header and complete measured native caller flow,not original SDK C',
        observedHttpLayout=dict(bytes=7188,param=4100,alloc=4112,free=4116,error=4128,url=4132,lowrecv=6604,lowsend=6608,req=6648,rep=6664,postCount=6644,contentMutex=6680,labels=6712,thread=6968,threadStateWord=7076,mutex=7160,abort=7184,opaqueCpsSslBytes=2198),
        createBoundary='Allocator is loaded from incoming parameter block before7188-byte clear;28-byte parameter copy and received/content-1 fields follow. Two2920/1514 allocations and explicit supplied buffer/host/basic-header failures preserve exact returned/stored error and initialized flag. Selected volatile error view is conservative: removing qualifier can retain same bytes/reads under pinned compiler,so necessity/original qualifier uniqueness is not asserted.',
        destructorBoundary='Native free field load precedes null branch. Returning fixtures REQUIRE nonnull Http; no safe-null guarantee is inferred from the later branch. Cached free survives supplied table/buffer/free field mutations; final7188-byte clear is exact.',
        threadBoundary='Caller compares raw ignoreCA word exactly1 and stores canonical0/1 into original four-byte BSS. Raw state0 or supplied termination result gates six-word create tuple including actual Thumb2098575 entry,stacktop andsize4096,priority; no callback/thread/scheduler executes.',
        formatBoundary='Only delimiter-present bounded requests and supplied one-argument format calls are modeled. Post base64 length prediction,provided8KiB physical backing,growth failure,second encoding result and counter/terminator effects qualify caller flow; advertised logical capacity does not establish actual allocation extent or global memory safety.',
        providerBodiesOriginalStorageAuthorshipHardwareNetworkSslThreadSchedulingGamePlatformExecutionCredit=0)
