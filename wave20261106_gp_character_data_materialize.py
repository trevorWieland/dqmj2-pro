from project import ROOT,read_json,write_json,sha256
from wave20261106_gp_character_data_paths import SOURCE,EVIDENCE,WORK,assert_owned
from wave20261106_gp_character_data_codec import render


def main():
    assert_owned();claim_path=EVIDENCE/'data-claim.json';claim=read_json(claim_path);assets=[];declarations=[]
    if claim['exclusiveSourceRoot']!=SOURCE.relative_to(ROOT).as_posix()or claim['functionCount']!=0 or claim['functionOwnershipGranted']:raise ValueError('Exact admitted data-only ownership differs')
    if len(claim['claimedStorage'])!=259 or sum(x['bytes']for x in claim['claimedStorage'])!=3696:raise ValueError('Complete admitted GP data membership differs')
    for row in claim['claimedStorage']:
        if (row['program'],row['processor'],row['module'],row['mode'],row['kind'],row['formatKind'])!=('','arm9','main','data','data','whole-primary-c-character-object'):raise ValueError('Admitted GP character namespace differs')
        semantic=ROOT/row['semanticSource']
        if not semantic.resolve().is_relative_to(SOURCE)or sha256(semantic)!=row['semanticSourceSha256']:raise ValueError('Admitted whole-character semantic source differs')
        address=int(row['address'],0);symbol=f'native_gp_character_{address:08x}';code,payload=render(read_json(semantic),symbol);target=SOURCE/f'{address:08x}.c'
        if target.exists()and target.read_text(encoding='utf-8')!=code:raise ValueError('Existing promoted character C differs')
        if not target.exists():target.write_text(code,encoding='utf-8')
        declarations.append(f'extern const char {symbol}[{len(payload)}];')
        assets.append(dict(row,nativeSymbol=symbol,source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),compilerProcessor='arm946e',binary='extract/arm9/arm9.bin',inputModuleSha256='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f',moduleBase='0x2000000',encodedAssetBytes=0,measuredZeroAlignmentBytes=0))
    header=SOURCE/'characters.h';text='\n'.join(['#ifndef GP_CHARACTER_OBJECTS_H','#define GP_CHARACTER_OBJECTS_H','typedef char GPCharacterWidthMustBeOne[(sizeof(char)==1)?1:-1];',*declarations,'#endif',''])
    if header.exists()and header.read_text(encoding='utf-8')!=text:raise ValueError('Existing real character extent declarations changed')
    if not header.exists():header.write_text(text,encoding='utf-8')
    value=dict(schemaVersion=1,romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',program='',processor='arm9',module='main',kind='data',mode='data',assets=assets,objectCount=259,initializedBytes=3696,ordinaryFunctionCredit=0,encodedAssetBytes=0,measuredZeroAlignmentBytes=0,characterHeader=dict(path=header.relative_to(ROOT).as_posix(),sha256=sha256(header)),ownershipClaim=dict(path=claim_path.relative_to(ROOT).as_posix(),sha256=sha256(claim_path)))
    path=SOURCE/'layout.json'
    if path.exists()and read_json(path)!=value:raise ValueError('Existing exact character layout differs')
    if not path.exists():write_json(path,value)
    print(dict(objects=259,bytes=3696,layoutSha256=sha256(path),headerLines=len(text.splitlines()),cFiles=259),flush=True)


if __name__=='__main__':main()
