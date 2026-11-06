from project import ROOT,read_json,write_json,sha256
from wave20261106_aes_table_data_paths import SOURCE,EVIDENCE,assert_owned
from wave20261106_aes_table_data_codec import render,header

CLAIM_SHA='366bfb04f9d8b3e92ae1e2d54b90c3699d13fb57d57654d4e596cb71803a2694'
IMAGE='extract/arm9_overlays/ov006.bin'
IMAGE_SHA='fb9cb28ea400207bda442e3265da73af994866cf3a6c352b46a11db59835d341'


def main():
    assert_owned();claim_path=EVIDENCE/'data-claim.json'
    if sha256(claim_path)!=CLAIM_SHA:raise ValueError('Exact ten-table AES admission changed')
    claim=read_json(claim_path)
    if claim['exclusiveSourceRoot']!=SOURCE.relative_to(ROOT).as_posix()or claim['exclusiveWorkRoot']!='work/w6at'or claim['functionCount']or claim['functionOwnershipGranted']:raise ValueError('AES exclusive initialized-data-only ownership differs')
    if len(claim['claimedStorage'])!=10 or sum(r['bytes']for r in claim['claimedStorage'])!=10240:raise ValueError('Exact ten-table10240B whole-array membership differs')
    assets=[]
    for row in claim['claimedStorage']:
        if(row['program'],row['processor'],row['module'],row['kind'],row['mode'],row['formatKind'],row['bytes'],row['elementType'],row['elementCount'])!=('','arm9','ov006','data','data','aes-rijndael-transform-table',1024,'u32',256):raise ValueError('AES admitted complete-object namespace or typed extent differs')
        semantic=ROOT/row['semanticSource']
        if not semantic.resolve().is_relative_to(SOURCE.resolve())or sha256(semantic)!=row['semanticSourceSha256']:raise ValueError('AES admitted mathematical descriptor changed')
        doc=read_json(semantic);symbol=f"native_aes_{doc['symbol']}_{int(row['address'],0):08x}";code,payload=render(doc,symbol);source=SOURCE/f"{int(row['address'],0):08x}.c"
        if source.exists()and source.read_text(encoding='utf-8')!=code:raise ValueError('Existing promoted AES C changed')
        if not source.exists():source.write_text(code,encoding='utf-8')
        assets.append(dict(row,nativeSymbol=symbol,primarySymbol=doc['symbol'],source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),compilerProcessor='arm946e',binary=IMAGE,inputModuleSha256=IMAGE_SHA,moduleBase='0x21d7240',encodedAssetBytes=0,measuredZeroAlignmentBytes=0))
    target=SOURCE/'aes_tables.h';text=header(assets)
    if target.exists()and target.read_text(encoding='utf-8')!=text:raise ValueError('Existing actual AES fixed-width/extent declarations changed')
    if not target.exists():target.write_text(text,encoding='utf-8')
    layout=dict(schemaVersion=1,romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',program='',processor='arm9',module='ov006',kind='data',mode='data',assets=assets,objectCount=10,initializedBytes=10240,wordHeader=dict(path=target.relative_to(ROOT).as_posix(),sha256=sha256(target)),ownershipClaim=dict(path=claim_path.relative_to(ROOT).as_posix(),sha256=CLAIM_SHA),ordinaryFunctionCredit=0,encodedAssetBytes=0,measuredZeroAlignmentBytes=0,interiorViewExtraBytes=0)
    target=SOURCE/'layout.json'
    if target.exists()and read_json(target)!=layout:raise ValueError('Existing exact AES layout changed')
    if not target.exists():write_json(target,layout)
    print(dict(objects=10,bytes=10240,headerLines=len(text.splitlines()),layoutSha256=sha256(target)),flush=True)


if __name__=='__main__':main()
