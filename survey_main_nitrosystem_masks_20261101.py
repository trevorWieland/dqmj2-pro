from collections import defaultdict
from pathlib import Path
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,configuration,read_json,write_json,sha256
from link_runtime_unit import measured_module

INPUT=ROOT/'work/main-nitrosystem-breadth-20261101/report.json'
OUTPUT=ROOT/'evidence/attempts/main-nitrosystem-masked-candidates-20261101.json'


def main():
    inventory=read_json(ROOT/'evidence/regions/canonical-symbol-functions.json')
    assert inventory['romSha256']==configuration()['romSha256']
    module,image,_=measured_module('main')
    functions=next(row for row in inventory['canonicalModules']if row['module']=='main')['functions']
    sizes=defaultdict(list)
    for row in functions:
        if row['mode']=='arm'and row['size']>=32:sizes[row['size']].append(row)
    snapshot=read_json(ROOT/'evidence/verification/accepted-cohort121-identities-v2-20261101.json')['functions']
    accepted=[(row['address'],row['address']+row['bytes'])for row in snapshot if row['processor']=='arm9'and row['module']=='main']
    queued={0x0203716C,0x02036C78,0x02036DD4,0x02036EA4,0x02036F68}
    results=[];seen_functions=0;unsupported=[]
    for unit in read_json(INPUT)['results']:
        if unit['exitCode']:continue
        obj=ROOT/unit['object'];assert sha256(obj)==unit['objectSha256']
        with obj.open('rb')as stream:
            elf=ELFFile(stream)
            for symbol in elf.get_section_by_name('.symtab').iter_symbols():
                if symbol['st_info']['type']!='STT_FUNC'or not isinstance(symbol['st_shndx'],int)or symbol['st_size']<32 or symbol['st_value']&1:continue
                seen_functions+=1
                start=symbol['st_value'];size=symbol['st_size']
                if size not in sizes:continue
                body=elf.get_section(symbol['st_shndx']).data()[start:start+size]
                assert len(body)==size
                mask=bytearray([255]*size);relocations=[];supported=True
                for section in elf.iter_sections():
                    if section['sh_type']not in ('SHT_REL','SHT_RELA')or section['sh_info']!=symbol['st_shndx']:continue
                    table=elf.get_section(section['sh_link'])
                    for rel in section.iter_relocations():
                        offset=rel['r_offset']-start
                        if not 0<=offset<size:continue
                        kind=rel['r_info_type']
                        if kind==2:mask[offset:offset+4]=bytes(4)
                        elif kind in (1,28,29):mask[offset:offset+3]=bytes(3)
                        else:supported=False
                        target=table.get_symbol(rel['r_info_sym'])
                        relocations.append(dict(offset=offset,type=kind,symbol=target.name,
                            sourceSymbolType=target['st_info']['type'],sourceSymbolBinding=target['st_info']['bind'],
                            sourceSymbolSection=target['st_shndx'],format=section['sh_type'],
                            explicitAddend=rel['r_addend']if section['sh_type']=='SHT_RELA'else None,
                            originalEncodedWord=body[offset:offset+4].hex()))
                if not supported:
                    unsupported.append(dict(referenceFunction=symbol.name,profile=unit['profile'],relocations=relocations));continue
                retained=sum(value.bit_count()for value in mask)
                if retained<size*4:continue
                for native in sizes[size]:
                    address=int(native['address'],0);original=image[address-0x02000000:address-0x02000000+size]
                    if len(original)!=size or any((a^b)&m for a,b,m in zip(body,original,mask)):continue
                    overlap=any(address<end and start_address<address+size for start_address,end in accepted)
                    owner='root'if address<0x02040000 or address>=0x020D0000 else'save-core'
                    results.append(dict(referenceFunction=symbol.name,referenceSource=unit['source'],
                        sourceSha256=unit['sourceSha256'],object=unit['object'],objectSha256=unit['objectSha256'],
                        compiler=unit['compiler'],compilerSha256=unit['compilerSha256'],compilerFlags=unit['compilerFlags'],
                        profile=unit['profile'],identity=dict(processor='arm9',program='',module='main',mode='arm',
                            address=hex(address),bytes=size,inputModuleSha256=module['sha256']),
                        originalBoundaryConfidence=native['boundaryConfidence'],sourceOwner=owner,
                        alreadyAccepted121=overlap,queuedOamFamily=address in queued,
                        retainedOpcodeAndDataBits=retained,totalBits=size*8,relocations=relocations,
                        originalOpcodeBitsAndNonRelocatedBytesExact=True,sourceCredit=0))
    unique={(row['identity']['address'],row['identity']['bytes'])for row in results
        if not row['alreadyAccepted121']and not row['queuedOamFamily']and row['sourceOwner']=='root'}
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),inputSha256=sha256(INPUT),
        sourceCredit=0,compiledFunctionRowsSurveyed=seen_functions,candidates=results,
        unsupportedRelocations=unsupported,maskedComparisonIsNotGenuineLinkOrSourceAdmission=True,
        provisionalHeaderAndCompleteTypeCallerNativeClosureUnproved=True,
        novelRootIdentities=len(unique),novelRootCandidateInitializedBytes=sum(size for address,size in unique))
    write_json(OUTPUT,report)
    print(dict(maskRows=len(results),novelRootIdentities=len(unique),novelRootCandidateBytes=sum(size for address,size in unique),
        unsupportedRelocationFunctions=len(unsupported),sourceCredit=0))


if __name__=='__main__':
    main()
