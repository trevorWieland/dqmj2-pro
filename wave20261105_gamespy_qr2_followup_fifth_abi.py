import hashlib
import re
import match_runtime
from project import ROOT,read_json,sha256
from wave20261105_gamespy_qr2_followup_fifth_bindings import inputs


def verify(rows):
    value,image,inventory,records,imports=inputs()
    expected={0x20b8780:40,0x20b87a8:60,0x20b9d2c:18,0x20b9d40:22,0x20b9270:68,0x20b9128:120,0x20b91a0:208}
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
    import struct
    from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
    dis=Cs(CS_ARCH_ARM,CS_MODE_THUMB);registers=[];signedness=[]
    for at in [0x20b87dc,0x20b92ac]:
        if struct.unpack_from('<I',image,at-0x2000000)[0]!=0x4000208:raise ValueError('Original exact16-bit register address differs')
    for at,mnemonic in [(0x20b87ae,'ldrh'),(0x20b87b0,'strh'),(0x20b87d4,'ldrh'),(0x20b87d6,'strh'),(0x20b9276,'ldrh'),(0x20b9278,'strh'),(0x20b92a4,'ldrh'),(0x20b92a6,'strh')]:
        raw=image[at-0x2000000:at-0x2000000+2];ins=list(dis.disasm(raw,at))
        if len(ins)!=1 or ins[0].mnemonic!=mnemonic:raise ValueError('Original16-bit read/write instruction differs')
        registers.append(dict(origin=hex(at),instruction=raw.hex(),mnemonic=mnemonic,width=2))
    for at,mnemonic in [(0x20b91de,'bgt'),(0x20b91f4,'blo'),(0x20b9244,'blo')]:
        raw=image[at-0x2000000:at-0x2000000+2];ins=list(dis.disasm(raw,at))
        if len(ins)!=1 or ins[0].mnemonic!=mnemonic:raise ValueError('Original signed/sizeof progress branch differs')
        signedness.append(dict(origin=hex(at),instruction=raw.hex(),mnemonic=mnemonic))
    return dict(status='passed',callerExtents=expected,providers=providers,
        messageBoundary='Original incomingR0 result pointer survives inR1 across three clears and is forwarded as queue message; NULL and non-NULL messages independently tested',
        threadViews=[dict(bytes=2292,threadOffset=52),dict(bytes=4816,threadOffset=2576)],
        boundedRegisterView=dict(address='0x4000208',width=2,originalInstructionEvidence=registers,sourceOnlyVolatileC=True,originalStorageCredit=0,actualInterruptsOrSchedulingExecuted=False),
        signednessEvidence=signedness,frameView=dict(bytes=1044,lengthOffset=0,magicOffset=4,minimumHeaderBytes=12,magic='0x44535359'),
        ioBoundary='Three exact words for each read/write provider; signed progress/error returns, unsigned sizeof/length bounds; provided positive counts never exceed request and finite scripts bound zero-progress writes',
        receiverBehavior='Four-byte length read first, then bounded remainder; partial-header zero/negative cases, oversized frames, short header and wrong magic preserve original return/error tuples',
        providerResultBoundary='Status result preserved across cleanup; output-pointer provider writes one private word, with actual argument position and modes checked',
        persistentZeroProgressOrOutOfContractProviderTerminationProven=False,actualProvidersThreadsHardwareNetworkingGameOrPlatformExecutionCredit=0)
