import hashlib
import re
import match_runtime
from project import ROOT,read_json,sha256
from wave20261105_gamespy_qr2_followup_second_bindings import inputs


def verify(rows):
    value,image,inventory,records,imports=inputs()
    expected={0x20b8878:48,0x20b88a8:40,0x20b88d0:44,0x20b8d14:48,0x20b8d44:60,0x20b8d80:32,0x20b8da0:36,0x20b8dd8:36,0x20b8dfc:68,0x20b87e4:148,0x20b85d8:20}
    if {int(row['address'],0):row['bytes']for row in rows}!=expected:raise ValueError('Qualified control subset differs')
    providers={}
    for row in rows:
        header=next(ROOT/pin['path']for pin in row['sourceDependencies']if pin['path'].endswith('/context.h'))
        text=header.read_text()
        if row['address']=='0x20b8d44'and 'extern void native_fn_020b8d14(int,Event*);'not in text:raise ValueError('Two-word boundary callback declaration changed')
        for symbol,binding in row['nativeSymbolEntries'].items():
            if binding['kind']!='function':continue
            at=int(binding['address'],0);mode=binding['mode']
            found=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(%s,size=0x[0-9a-f]+\) addr:0x%08x'%(mode,at),line)),None)
            if found is None:raise ValueError('Original provider namespace/extent absent')
            size=int(re.search(r'size=(0x[0-9a-f]+)',found)[1],0)
            declarations=[line for line in text.splitlines()if line.startswith('extern ')and re.search(r'\b'+re.escape(symbol)+r'\b',line)]
            if len(declarations)!=1:raise ValueError(('Actual selected import declaration absent',symbol))
            providers[symbol]=dict(binding=binding,canonicalInventoryRecord=found,bytes=size,originalBodySha256=hashlib.sha256(image[at-0x2000000:at-0x2000000+size]).hexdigest(),sourceDeclaration=declarations[0],actualOriginalProviderBodyExecuted=False,providerSourceCredit=0)
    return dict(status='passed',callerExtents=expected,providers=providers,originalTypedFunctionPointerViews=imports['functionPointerViews'],
        prefixes=dict(control=48,result=40,event=20,activeOffset=36,userCallbackOffset=40,completionOffset=44),
        userCallbackBoundary='One Event* word; native and source callers exercise synthetic ARM and Thumb providers, returns and global-base mutations',
        registeredBoundaryCallback='void(int,Event*); original pointer020b8d15, canonical Thumb entry020b8d14, source caller independently exercises both incoming words',
        workerBoundary='One opaque thread argument retained; ignored by complete148-byte caller; supplied worker/queue providers never execute original bodies',
        registryBoundary='Signed key range50..254 inclusive; one raw incoming pointer word stored.1020-byte indexed address span is a caller view and adds no allocation or original storage credit',
        fullContainerLayoutsOrProviderImplementationsEstablished=False,hardwareThreadsNetworkingOrGameExecutionCredit=0)
