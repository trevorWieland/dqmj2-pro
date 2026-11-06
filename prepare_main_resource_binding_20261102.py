import re
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from project import ROOT,read_json,write_json,sha256
from link_runtime_unit import measured_module
from slice_reference_sdk_entities_v3_20261102 import functions,slice_closed
import match_main_oam_reference296_closed_20261101 as builder

TARGETS=[('NNS_G3dResDefaultSetup',0x02031FA4,'02031fa4'),('NNS_G3dBindMdlSet',0x0202F3DC,'0202f3dc'),
 ('NNS_G3dBindMdlTex',0x0202EFE4,'0202f3dc'),('NNS_G3dBindMdlPltt',0x0202F250,'0202f3dc'),
 ('bindMdlTex_Internal_',0x0202EDFC,'0202f3dc'),('bindMdlPltt_Internal_',0x0202F170,'0202f3dc')]


def main():
    meta,image,_=measured_module('main');assert meta['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    mapping={};all_bindings={}
    for row in read_json(ROOT/'evidence/attempts/main-nitrosystem-enum-closure-linking-20261102.json')['results']:
        for name,binding in row.get('bindings',{}).items():all_bindings.setdefault(name,set()).add(int(binding['address'],0))
    ambiguous={name:sorted(values)for name,values in all_bindings.items()if len(values)>1}
    for name,values in all_bindings.items():
        if len(values)==1:mapping[name]=next(iter(values))
    for name,address,unused in TARGETS:mapping[name]=address
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True
    instruction=next(decoder.disasm(image[0x2EDFC+228:0x2EDFC+232],0x0202EDFC+228))
    assert instruction.mnemonic=='bl';mapping['FX_Div']=instruction.operands[0].imm
    folder=ROOT/'src/runtime/20261102_resource_binding';folder.mkdir(parents=True,exist_ok=True);rows=[]
    for name,address,base in TARGETS:
        origin=ROOT/f'generated/recovery/20261102-nitrosystem-enum-closed/{base}/closed.c';text=origin.read_text(encoding='utf-8')
        for record in sorted(functions(text),key=lambda row:row['start'],reverse=True):
            header=text[record['start']:record['opening']]
            if record['name']==name or re.search(r'\binline\b',header):continue
            header=re.sub(r'\bstatic\s+','',header)
            text=text[:record['start']]+header.rstrip()+';\n'+text[record['end']:]
        text=re.sub(r'\bstatic\s+(?=[^;{}]*\b'+re.escape(name)+r'\s*\()','',text)
        text,closure=slice_closed(text,[name]);text=text.replace('unsigned long u32','unsigned int u32').replace('signed long s32','signed int s32')
        assert not any(re.search(r'\b'+re.escape(key)+r'\b',text)for key in ambiguous)
        replacements={key:('native_main_'if key==name else'native_fn_')+f'{value:08x}'for key,value in mapping.items()}
        for key in sorted(replacements,key=len,reverse=True):text=re.sub(r'\b'+re.escape(key)+r'\b',replacements[key],text)
        path=folder/f'native_main_{address:08x}.c';assert len(text.splitlines())<=500
        if path.exists():assert path.read_text(encoding='utf-8')==text
        else:path.write_text(text,encoding='utf-8')
        rows.append(dict(name=name,address=hex(address),source=path.relative_to(ROOT).as_posix(),sourceSha256=sha256(path),
         origin=origin.relative_to(ROOT).as_posix(),originSha256=sha256(origin),closure=closure,lines=len(text.splitlines())))
    write_json(ROOT/'evidence/attempts/main-resource-binding-source-origin-20261102.json',dict(sourceCredit=0,rows=rows,
     staticFunctionVisibilityOnlyPromoted=True,inlineBodiesPreserved=True,sourceTypesFixed32=True,
     unrelatedAmbiguousReferenceNamesExcluded=ambiguous,generatorSha256=sha256(__file__)))
    builder.WORK=ROOT/'work/main-resource-binding-preflight-20261102';results=[]
    for row in rows:
        try:
            entry,proof,body=builder.build(ROOT/row['source'],row['address'],True)
            results.append(dict(source=row,entry=entry,proof=proof,exact=True));print(row['address'],len(body),'genuine',flush=True)
        except Exception as error:
            results.append(dict(source=row,exact=False,error=repr(error)));print(row['address'],str(error)[:200],flush=True)
    write_json(ROOT/'evidence/attempts/main-resource-binding-preflight-20261102.json',dict(sourceCredit=0,rows=results))


if __name__=='__main__':
    main()
