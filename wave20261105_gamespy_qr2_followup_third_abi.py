import hashlib
import re
import match_runtime
from project import ROOT,read_json,sha256
from wave20261105_gamespy_qr2_followup_third_bindings import inputs


def verify(rows):
    value,image,inventory,records,imports=inputs()
    expected={0x20b86cc:104,0x20b8e74:240,0x20b8f64:16,0x20b90bc:48,0x20b90ec:20,0x20b92b4:116}
    if {int(row['address'],0):row['bytes']for row in rows}!=expected:raise ValueError('Qualified control subset differs')
    providers={}
    for row in rows:
        header=next(ROOT/pin['path']for pin in row['sourceDependencies']if pin['path'].endswith('/context.h'))
        text=header.read_text()
        if row['address']=='0x20b8e74'and 'typedef void*(*Alloc)(unsigned long,long);typedef void(*Free)(unsigned long,void*,long);'not in text:raise ValueError('Published allocator callback word ABI changed')
        for symbol,binding in row['nativeSymbolEntries'].items():
            if binding['kind']!='function':continue
            at=int(binding['address'],0);mode=binding['mode']
            found=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(%s,size=0x[0-9a-f]+\) addr:0x%08x'%(mode,at),line)),None)
            if found is None:raise ValueError('Original provider namespace/extent absent')
            size=int(re.search(r'size=(0x[0-9a-f]+)',found)[1],0)
            declarations=[line for line in text.splitlines()if line.startswith('extern ')and re.search(r'\b'+re.escape(symbol)+r'\b',line)]
            if len(declarations)!=1:raise ValueError(('Actual selected import declaration absent',symbol))
            providers[symbol]=dict(binding=binding,canonicalInventoryRecord=found,bytes=size,originalBodySha256=hashlib.sha256(image[at-0x2000000:at-0x2000000+size]).hexdigest(),sourceDeclaration=declarations[0],actualOriginalProviderBodyExecuted=False,providerSourceCredit=0)
    path=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-followup/third/interfaces.json';reference=read_json(path)
    if len(reference['files'])!=1 or reference['commit']!='9136bfa0bf3a5123ce560e6cd47017456e4c130b':raise ValueError('Narrow published callback reference changed')
    pin=reference['files'][0];published=ROOT/pin['path']
    if sha256(published)!=pin['sha256']or 'DWCAuthAlloc)(unsigned long name, long size)'not in published.read_text()or 'DWCAuthFree)(unsigned long name, void * ptr, long size)'not in published.read_text():raise ValueError('Actual published callback declarations differ')
    from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
    dis=Cs(CS_ARCH_ARM,CS_MODE_THUMB);reads=[]
    for at,operand in [(0x20b90c8,'r1, [r0, #4]'),(0x20b90d4,'r0, [r1, #4]'),(0x20b90f4,'r1, [r2]'),(0x20b92c8,'r0, [r1]'),(0x20b92ce,'r0, [r1]')]:
        raw=image[at-0x2000000:at-0x2000000+2];ins=list(dis.disasm(raw,at))
        if len(ins)!=1 or ins[0].mnemonic!='ldr'or ins[0].op_str!=operand:raise ValueError('Original measured shared-word read instruction differs')
        reads.append(dict(origin=hex(at),instruction=raw.hex(),mnemonic='ldr',operands=operand,width=4))
    return dict(status='passed',callerExtents=expected,providers=providers,originalTypedFunctionPointerViews=imports['functionPointerViews'],
        initializedCallerViews=[dict(bytes=2292,threadOffset=52,threadBytes=192,stackOffset=244,stackBytes=2048),dict(bytes=4816,threadOffset=2576,threadBytes=192,stackOffset=2768,stackBytes=2048)],
        threadCreationBoundary='Six exact argument words: thread-view pointer, qualified Thumb entry, opaque argument0, stack end,2048-byte size, unchanged priority word',
        publishedAllocationCallbackReference=dict(path=pin['path'],sha256=pin['sha256']),allocatorBoundary='Published unsigned-long/long words, free adds pointer word; incoming function pointers stored only, no actual allocator invocation',
        measuredSharedWordReadInstructions=reads,readOracle='Transition old-word reads and each worker guard/switch read are independently compared in order; dropping a read or volatile qualifier must fail returning caller models',
        returnContracts='All six selected native caller boundaries are void; all incoming words and actual provider argument tuples are preserved',
        fullForeignContainerAllocationOrProviderImplementationsEstablished=False,unknownPhaseDefaultTerminationProven=False,hardwareThreadsNetworkingOrGameExecutionCredit=0)
