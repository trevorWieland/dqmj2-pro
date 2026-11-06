import hashlib
import re
import match_runtime
from project import ROOT,read_json,sha256
from wave20261105_gamespy_qr2_followup_fourth_bindings import inputs


def verify(rows):
    value,image,inventory,records,imports=inputs()
    expected={0x20b8fd8:88,0x20b909c:32,0x20b9a98:28,0x20b9bf4:56,0x20b9c4c:40,0x20b9cd8:28,0x20b9a48:80,0x20b9c74:68,0x20b9ab4:112,0x20b9b24:108,0x20b9b90:100}
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
    dis=Cs(CS_ARCH_ARM,CS_MODE_THUMB);reads=[]
    for at,operand in [(0x20b8ff4,'r1, [r2, r0]'),(0x20b900a,'r1, [r2, r0]'),(0x20b9010,'r0, [r2, r0]')]:
        raw=image[at-0x2000000:at-0x2000000+2];ins=list(dis.disasm(raw,at))
        if len(ins)!=1 or ins[0].mnemonic!='ldr'or ins[0].op_str!=operand:raise ValueError('Original signed shared-word load differs')
        reads.append(dict(origin=hex(at),instruction=raw.hex(),operands=operand,width=4))
    return dict(status='passed',callerExtents=expected,providers=providers,measuredOrderedSignedErrorLoads=reads,
        prefixes=dict(status=72,requestOffset=20,requestBytes=40,callbackOffset=60,opaqueWord4Offset=64,opaqueWord5Offset=68,errorPair=8),
        requestProducerBoundary='Five incoming words id,buffer-word,capacity-word,opaque-word4,opaque-word5; word5 at entrySP+0 retained; final two words only stored with no callback/userdata interpretation',
        idBoundary='Actual unsigned id ranges1..255 for nonzero mode and1..15 otherwise; selected producer1 adds1024 to id, not pointer arithmetic',
        errorForwardBoundary='Two incoming words preserved: opaque unsigned word0 and signed word1; actual provider body comparisons consume R1 signed and store both words, while callers discard its return value',
        callbackBoundary='One explicit raw result word, synthetic ARM/Thumb entry modes and helper mutations tested; no actual callback body execution',
        readBoundary='Pre-lock signed error load, post-lock sign recheck and separate forwarded argument load preserved and independently counted',
        fullForeignStatusAllocationOrUncoveredSizeCalculatorEstablished=False,unknownOpaqueWordsOrGameMeaningInferred=False,providedBodiesOrHardwareExecutionCredit=0)
