import hashlib
import json
import struct
from pathlib import Path
import main_frame_heap_wrappers108_native_20261101 as native
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/application/frame-heap-wrappers108-word-abi-20261101.json'


def main():
    path=ROOT/'extract/arm9/arm9.bin';image=path.read_bytes()
    if sha256(path)!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':raise ValueError('Measured ARM9 module differs')
    cases=[]
    for entry,index,label in[(native.CREATOR,1330,'mapped-minimum48'),(native.CREATOR,59,'full32-option-word-forwarding'),(native.CREATOR,1425,'mapped-near-minimum60'),
        (native.CREATOR,1269,'creator-wrap-guard'),(native.ALLOCATOR,0,'alignment0-word-pointer-update'),
        (native.ALLOCATOR,196,'alignment0-clear-flag-signed-fill-skip'),(native.ALLOCATOR,24,'requested-FFFFFFFD-rounds0'),
        (native.ALLOCATOR,121,'tail-FFFFFFFC-advances-tail-word'),(native.ALLOCATOR,195,'head-overflow-updates-head0-returns-high-word'),
        (native.ALLOCATOR,517,'unsupported-negative-fill-address')]:
        size=56 if entry==native.CREATOR else 52;code=image[entry-0x02000000:entry-0x02000000+size]
        result=native.execute(image,entry,code,index)
        cases.append(dict(label=label,qualifiedNativeId=dict(processor='arm9',program='',module='main',mode='arm',address=hex(entry),bytes=size),
            index=index,result=result,sourceCredit=0))
    dependencies=[]
    for address,size in sorted(native.HELPERS.items()):
        data=image[address-0x02000000:address-0x02000000+size]
        dependencies.append(dict(processor='arm9',program='',module='main',mode='arm',address=hex(address),bytes=size,
            sha256=hashlib.sha256(data).hexdigest(),originalNativeDependency=True,additionalSourceCredit=0))
    table=struct.unpack_from('<I',image,0x2B9D8)[0];offset=table-0x02000000
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),
        fixture=Path(native.__file__).name,fixtureSha256=sha256(native.__file__),
        romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',moduleSha256=sha256(path),
        actualCreatorArguments=3,actualAllocatorArguments=3,actualCommonInitializerArguments=5,
        commonInitializerFlagsAreFullStackWord=True,allocatorSignedBranchAndUnsignedWordNegation=True,
        zeroReturnIsNotUnchangedState=True,nativeFillUsesSignedAddressComparison=True,
        fillPatternTable=dict(address=hex(table),bytes=12,sha256=hashlib.sha256(image[offset:offset+12]).hexdigest(),
            rawWords=[hex(x)for x in struct.unpack_from('<III',image,offset)],kind='original-initialized-data',additionalDataCredit=0),
        dependencies=dependencies,cases=cases,providerReplacements=[],additionalSourceOrDataCredit=0,
        limitations=['Native-only ABI characterization of deterministic synthetic contexts; no new code/source credit',
            'Disposable-boundary stops receive no normal-return or post-state credit',
            'Pointer words, wrap and signed fill comparisons do not establish legitimate ownership, safe game calls, concurrent behavior or Android/native64-bit portability']))
    print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),cases=len(cases),
        actualOwnReturns=sum(c['result']['actualOwnReturn']for c in cases))),flush=True)


if __name__=='__main__':main()
