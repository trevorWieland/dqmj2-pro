import concurrent.futures
import hashlib
import re
import struct
from pathlib import Path
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from project import ROOT,read_json,write_json,sha256
from link_runtime_unit import measured_module,validate

INPUT=ROOT/'evidence/attempts/main-nitrosystem-masked-candidates-20261101.json'
WORK=ROOT/'work/main-nitrosystem-links-20261101'


def namespace():
    functions={}
    for name in ['main','itcm','dtcm']:
        metadata,binary,config=measured_module(name)
        for mode,size,address in re.findall(r'^\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)$',config,re.M):
            address=int(address,0)
            assert address not in functions
            functions[address]=dict(kind='function',processor='arm9',program='',module=name,mode=mode,address=hex(address))
    return functions


def link(item):
    index,row,functions,image=item
    identity=row['identity'];address=int(identity['address'],0);size=identity['bytes']
    original=image[address-0x02000000:address-0x02000000+size]
    bindings={};directory=WORK/f'{index:04}-{address:08x}-{row["profile"]}'
    result=dict(referenceFunction=row['referenceFunction'],referenceSource=row['referenceSource'],
        identity=identity,profile=row['profile'],sourceCredit=0,sourceAdmissionRequested=False,
        provisionalHeaderAndCompleteCallerTypeNativeClosureStillUnproved=True)
    try:
        for relocation in row['relocations']:
            offset=relocation['offset'];name=relocation['symbol'];kind=relocation['type']
            is_function=kind in (1,28,29)or relocation['sourceSymbolType']=='STT_FUNC'
            if kind==2:
                addend=relocation['explicitAddend']if relocation['format']=='SHT_RELA'else int.from_bytes(bytes.fromhex(relocation['originalEncodedWord']),'little')
                target=(struct.unpack_from('<I',original,offset)[0]-addend)&0xFFFFFFFF
            else:
                instruction=next(Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(original[offset:offset+4],address+offset),None)
                if instruction is None:raise ValueError('Original branch undecodable')
                decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True
                instruction=next(decoder.disasm(original[offset:offset+4],address+offset))
                if not instruction.operands or instruction.operands[0].type!=2:raise ValueError('Original branch lacks immediate target')
                target=instruction.operands[0].imm&0xFFFFFFFF
            if is_function:
                canonical=target&~1
                if canonical not in functions:raise ValueError('Unknown or interior native function reference:'+name+' '+hex(target))
                binding=functions[canonical]
                if kind==2 and bool(target&1)!=(binding['mode']=='thumb'):raise ValueError('Function-pointer mode differs')
            else:
                allowed=0x01FF0000<=target<0x02400000 or 0x02700000<=target<0x02800000 or 0x04000000<=target<0x08000000
                if not allowed:raise ValueError('Unqualified diagnostic data target:'+name+' '+hex(target))
                binding=dict(kind='data',processor='arm9',program='',module='main',mode='data',address=hex(target),
                    sourceCredit=0,referenceDerivedOnly=True,sourceAdmissionNotRequested=True)
            if name in bindings and bindings[name]!=binding:raise ValueError('One source symbol requires conflicting targets')
            bindings[name]=binding
        entry=dict(**identity,name=row['referenceFunction'],source=row['referenceSource'],sourceSha256=row['sourceSha256'],
            object=row['object'],objectSha256=row['objectSha256'],targetSha256=hashlib.sha256(original).hexdigest(),
            compiler=row['compiler'],compilerSha256=row['compilerSha256'],compilerFlags=row['compilerFlags'])
        proof=validate(entry,bindings,directory)
        result.update(genuineLinkedExact=True,entry=entry,bindings=bindings,genuineLinkComparison=proof)
    except Exception as error:
        result.update(genuineLinkedExact=False,refusalType=type(error).__name__,refusal=str(error))
    directory.mkdir(parents=True,exist_ok=True);write_json(directory/'result.json',result)
    return result


def main():
    assert not (WORK/'report.json').exists(),'Preserve earlier campaign'
    functions=namespace();metadata,image,_=measured_module('main')
    queue=[row for row in read_json(INPUT)['candidates']if not row['alreadyAccepted121']and not row['queuedOamFamily']and row['sourceOwner']=='root']
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
        for index,result in enumerate(pool.map(link,[(index,row,functions,image)for index,row in enumerate(queue)])):
            results.append(result)
            if(index+1)%32==0:print(dict(completed=index+1,total=len(queue),genuineExact=sum(r['genuineLinkedExact']for r in results)),flush=True)
    exact=[row for row in results if row['genuineLinkedExact']]
    unique={(row['identity']['address'],row['identity']['bytes'])for row in exact}
    write_json(WORK/'report.json',dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),
        inputSha256=sha256(INPUT),inputModuleSha256=metadata['sha256'],sourceCredit=0,results=results,
        genuineExactRows=len(exact),uniqueUnacceptedRootIdentities=len(unique),
        uniqueCandidateInitializedBytes=sum(size for address,size in unique),
        unchangedNormalArm9LinkerPolicy=True,referenceDerivedDataBindingsDiagnosticOnly=True,
        provisionalHeadersAndCompleteSourceCallerTypeNativeProofsStillUnresolved=True))
    print(dict(genuineExactRows=len(exact),uniqueUnacceptedRootIdentities=len(unique),
        candidateBytes=sum(size for address,size in unique),sourceCredit=0))


if __name__=='__main__':
    main()
