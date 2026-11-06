import re
from project import ROOT,read_json,write_json,sha256
import match_main_oam_reference296_closed_20261101 as builder

VIEWS={
 '0202beec':('NNSG3dResTex *','const NNSG3dResFileHeader *header','u32','void *','(void *)header','return (NNSG3dResTex *)'),
 '0202ec30':('u32','const NNSG3dResTex *tex','u32','void *','(void *)tex','return '),
 '0202ec44':('u32','const NNSG3dResTex *tex','u32','void *','(void *)tex','return '),
 '0202ed70':('u32','const NNSG3dResTex *tex','u32','void *','(void *)tex','return '),
 '0202ec58':('void','NNSG3dResTex *tex, u32 normal, u32 compressed','void','void *, s32, s32','(void *)tex, (s32)normal, (s32)compressed',''),
 '0202ed84':('void','NNSG3dResTex *tex, u32 palette','u32','void *, s32','(void *)tex, (s32)palette','(void)'),
 '0202ec6c':('void','NNSG3dResTex *tex, BOOL beginEnd','void','void *, s32','(void *)tex, (s32)beginEnd',''),
 '0202ed8c':('void','NNSG3dResTex *tex, BOOL beginEnd','void','void *, s32','(void *)tex, (s32)beginEnd',''),
 '0202bbb4':('void *','const NNSG3dResDict *dict, const NNSG3dResName *name','u32','s32, u8 *','(s32)dict, (u8 *)name','return (void *)')}


def main():
    folder=ROOT/'src/runtime/20261102_resource_binding_v3';folder.mkdir(parents=True,exist_ok=True);results=[]
    builder.WORK=ROOT/'work/main-resource-binding-abi-v3-preflight-20261102'
    for source in sorted((ROOT/'src/runtime/20261102_resource_binding_v2').glob('*.c')):
        text=source.read_text(encoding='utf-8');applied=[]
        if 'typedef signed int s32;'not in text:text='typedef signed int s32;\n'+text
        for address,(result,args,raw_result,raw_args,call,prefix)in VIEWS.items():
            name='native_fn_'+address
            if name not in text:continue
            pattern=r'(?m)^(?=[A-Za-z_])[^;{}\n]*\b'+name+r'\s*\([^;{}]*\)\s*;'
            matches=list(re.finditer(pattern,text));assert len(matches)==1,(source,name,len(matches))
            wrapper='resource_view_'+address
            text=re.sub(r'\b'+name+r'\b',wrapper,text)
            block=f'extern {raw_result} {name}({raw_args});\ninline {result} {wrapper}({args})\n{{\n    {prefix}{name}({call});\n}}'
            pattern=pattern.replace(name,wrapper);text=re.sub(pattern,lambda match:block,text,count=1)
            applied.append(address)
        path=folder/source.name;assert len(text.splitlines())<=500 and '/*'not in text and '//'not in text
        if path.exists():assert path.read_text(encoding='utf-8')==text
        else:path.write_text(text,encoding='utf-8')
        row,proof,body=builder.build(path,path.stem,True)
        results.append(dict(entry=row,proof=proof,selectedRawViews=applied,sourceOrigin=source.relative_to(ROOT).as_posix(),
         sourceOriginSha256=sha256(source),exact=True));print(row['address'],len(body),'genuine ABI views',applied,flush=True)
    write_json(ROOT/'evidence/attempts/main-resource-binding-abi-v3-preflight-20261102.json',dict(sourceCredit=0,results=results,
     matchedCandidateBytes=sum(r['entry']['bytes']for r in results),nativeClosureAndModuleAdmissionPending=True,generatorSha256=sha256(__file__)))


if __name__=='__main__':
    main()
