import hashlib
import re
import match_runtime
from project import ROOT,read_json,sha256
from wave20261105_gamespy_qr2_followup_seventh_bindings import inputs


def verify(rows):
    value,image,inventory,records,imports=inputs()
    expected={0x20b9068:24,0x20b9364:160,0x20b9404:172,0x20b95d8:120}
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
    for at,mnemonic in [(0x20b9370,'ldr'),(0x20b939a,'ldr'),(0x20b93cc,'ldr'),(0x20b93e8,'ldr'),(0x20b93ec,'ldr'),(0x20b93f2,'ldr'),(0x20b93f8,'ldr'),(0x20b9444,'ldr'),(0x20b9476,'ldr'),(0x20b9492,'ldr'),(0x20b9496,'ldr'),(0x20b949c,'ldr'),(0x20b94a2,'ldr'),(0x20b95e2,'ldr'),(0x20b95f8,'str')]:
        raw=image[at-0x2000000:at-0x2000000+2];ins=list(dis.disasm(raw,at))
        if len(ins)!=1 or ins[0].mnemonic!=mnemonic:raise ValueError('Original typed access/alignment/callback instruction differs')
        instructions.append(dict(origin=hex(at),instruction=raw.hex(),mnemonic=mnemonic,operands=ins[0].op_str))
    return dict(status='passed',callerExtents=expected,providers=providers,nativeInstructionEvidence=instructions,
        stateLayout=dict(minimumObservedBytes=4816,volatileRawPhaseOffset=4,volatileRawStatusOffsets=[52,64],rawStoredCallbackWordOffset=2572,volatileSignedHandleOffset=440,mutexOffset=444),
        controlFlow='Two independent switches preserve0..5 cases,1/2 sleep and optional cancellation,initial special phase gates,3/5/4 loop stops,unknown status fallthrough and repeated status reads; finite scripted supplied transitions qualify caller behavior only',
        signedCloseBoundary='Incoming signed32 handle captured before mutex,original shared word receives-59,nonnegative handles include0,first negative close result reports5/-50,subsequent-26 results retry after100-word sleeps,final nonzero reports5/-50; published phase1 follows all bounded returning paths',
        callbackBoundary='Only the original raw incoming word is stored at state2572 when state pointer nonnull; no callback argument/type/body interpretation or execution credit',
        providerBodiesThreadingNetworkingSleepSchedulingHardwareGamePlatformExecutionCredit=0)
