import json
import re
from pathlib import Path
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from link_runtime_unit import measured_module
from project import ROOT,configuration,sha256,write_json
TARGET=0x0222900C
SPECS={0x0222900C:244,0x02229100:1644,0x0222976C:240,0x0222985C:144,0x0221B070:1460,0x0221B624:1244,0x02221344:20,0x02221358:20,0x022212F0:28}
MAIN={0x02062A10:64,0x02062A50:24,0x02062A88:24,0x020628B0:84,0x02062980:96,0x020627A0:76}

def run():
    config=configuration()
    metadata,overlay,unused=measured_module('ov000')
    main_metadata,main,unused=measured_module('main')
    if metadata['sha256']!='783cb72f0d6ee2fdb632aba3e0ae41a9eee0c7e41933192b1680152e50aa61f6':
        raise ValueError('Birth331 overlay namespace differs')
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    bodies=[]
    for module,image,base,specs in[('ov000',overlay,0x021D7240,SPECS),('main',main,0x02000000,MAIN)]:
        symbols=ROOT/('config/arm9/overlays/ov000/symbols.txt'if module=='ov000'else'config/arm9/symbols.txt')
        text=symbols.read_text()
        for address,size in specs.items():
            if not re.search(r'kind:function\(arm,size='+hex(size)+r'\) addr:0x'+f'{address:08x}'+r'$',text,re.M):
                raise ValueError(('Birth331 configured boundary differs',hex(address),size))
            raw=image[address-base:address-base+size]
            code_size=size-4 if address==TARGET else size
            instructions=[dict(address=hex(i.address),bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str)for i in decoder.disasm(raw[:code_size],address)]
            bodies.append(dict(processor='arm9',program='',module=module,mode='arm',address=hex(address),bytes=size,sha256=match_runtime.sha(raw),configuredBoundarySha256=sha256(symbols),rawDecoderRowsIncludingPotentialLiterals=instructions,sourceCredit=0))
    callers=[]
    for path in sorted((ROOT/'asm').glob('*.s')):
        owner=None
        for number,line in enumerate(path.read_text().splitlines(),1):
            start=re.match(r'\s*(arm|thumb)_func_start (\S+)',line)
            if start:owner=start[2]
            if re.match(r'\s+blx? func_ov000_0222900c\s*$',line):
                callers.append(dict(assembly=str(path.relative_to(ROOT)),assemblySha256=sha256(path),line=number,owner=owner,staticOnly=True))
    report=dict(schemaVersion=1,romSha256=config['romSha256'],processor='arm9',program='',module='ov000',mode='arm',moduleSha256=metadata['sha256'],mainSha256=main_metadata['sha256'],sourceCredit=0,nativeExecutions=0,evidenceClass='Measured native instruction decoding and static direct-call inventory; no execution or original formal-arity proof',target=dict(address=hex(TARGET),bytes=244,qualifiedCallView='u32 observed_view(u32 parentUidA,u32 parentUidB)',originalFormalSignature='unproven',contradictedRole='child identity getter',staticRole='UID-consuming state-mutating call chain returning the final helper result'),bodies=bodies,directCallers=callers,facts=['0222900C looks up R0/R1 UIDs through02062A10 and passes both pointers plus signed child species from022474C8+18 to0222976C','It loops indices0..2 over02062A50 and02062A88, reads each nonnull record UID at+14, and calls020628B0 or02062980 when either incoming UID matches','It then calls020627A0 with each incoming UID and forwards0222976C result to0222985C; its physicalR0 comes from0222985C','0222976C writes scratch+1B; its fallback calls actual RNG0203D294 with17, then1024 only when the first result is nonzero; child-kind predicate02044D60 may subsequently overwrite that byte with2','0222985C calls0206271C with scratch signed species+18/raw variant+1A, forwards returned word through record writers and returns that word','02229100 is a distinct1644-byte function returning the scratch address022474C8; this is not the same operation as0222900C'],limits=['All facts here are static; zero native executions and zero source-match credit','Configured function extents are pinned inventory boundaries; native interface meaning and original formal typedefs remain qualified','The direct-call inventory searches existing generated assembly and excludes indirect calls, interior entries and unloaded namespaces not represented there','The observed caller is itself a larger state-driven routine; its raw state, prior initialization, scene reachability and user intent are not established by this packet','RNG chronology, record deletion/allocation success/error paths, persistence and full synthesis semantics require separate native execution','Naming0222900C a commit/create step is an inference from this call chain, not an accepted semantic fact','Raw decoder rows for bodies other than0222900C may include literal-pool words; those rows are scaffolding, not accepted code classification','No application/adapters/UI or frozen source is changed'],generatorSha256=sha256(__file__),reproductionCommand='python inspect_ov000_birth_roles331_20261031.py')
    write_json(ROOT/'evidence/application/ov000-birth-roles331-static-20261031.json',report)
    print(json.dumps(dict(target=hex(TARGET),bodies=len(bodies),directCallers=callers,reportSha256=sha256(ROOT/'evidence/application/ov000-birth-roles331-static-20261031.json'))))

if __name__=='__main__':run()
