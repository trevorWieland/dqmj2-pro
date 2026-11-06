from project import ROOT,read_json,write_json,sha256
from wave20261106_auth_character_data_paths import SOURCE,EVIDENCE,assert_owned
from wave20261106_auth_character_data_codec import render,header

CLAIM_SHA='02be137cee4d5da3d0311cd4c62335d1192d29f1ed1fd672d481eb892b001ed4'
IMAGE='extract/arm9/arm9.bin'
IMAGE_SHA='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'


def main():
    assert_owned();claim_name=EVIDENCE/'data-claim.json'
    if sha256(claim_name)!=CLAIM_SHA:raise ValueError('Exact102-object Auth storage admission changed')
    claim=read_json(claim_name)
    if claim['exclusiveSourceRoot']!=SOURCE.relative_to(ROOT).as_posix()or claim['exclusiveWorkRoot']!='work/w6ac'or claim['functionCount']or claim['functionOwnershipGranted']:raise ValueError('Auth data ownership namespace differs')
    rows=claim['claimedStorage']
    if len(rows)!=102 or sum(row['bytes']for row in rows)!=1431:raise ValueError('Auth102/1431 complete data membership differs')
    assets=[]
    for row in rows:
        address=int(row['address'],0)
        if (row['program'],row['processor'],row['module'],row['kind'],row['mode'],row['formatKind'])!=('','arm9','main','data','data','whole-primary-c-character-object')or address in(0x20deb48,0x20defec):raise ValueError('Auth source crossed exact admitted data identities')
        semantic=ROOT/row['semanticSource']
        if not semantic.resolve().is_relative_to(SOURCE.resolve())or sha256(semantic)!=row['semanticSourceSha256']:raise ValueError('Auth admitted semantic document changed')
        symbol=f'native_auth_character_{address:08x}';code,payload=render(read_json(semantic),symbol);target=SOURCE/f'{address:08x}.c'
        if target.exists()and target.read_text(encoding='utf-8')!=code:raise ValueError('Existing Auth promoted C changed')
        if not target.exists():target.write_text(code,encoding='utf-8')
        assets.append(dict(row,nativeSymbol=symbol,source=target.relative_to(ROOT).as_posix(),sourceSha256=sha256(target),compilerProcessor='arm946e',binary=IMAGE,inputModuleSha256=IMAGE_SHA,moduleBase='0x2000000',encodedAssetBytes=0,measuredZeroAlignmentBytes=0))
    target=SOURCE/'characters.h';text=header(assets)
    if target.exists()and target.read_text(encoding='utf-8')!=text:raise ValueError('Existing real Auth character declarations changed')
    if not target.exists():target.write_text(text,encoding='utf-8')
    layout=dict(schemaVersion=1,romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',program='',processor='arm9',module='main',kind='data',mode='data',assets=assets,objectCount=102,initializedBytes=1431,characterHeader=dict(path=target.relative_to(ROOT).as_posix(),sha256=sha256(target)),ownershipClaim=dict(path=claim_name.relative_to(ROOT).as_posix(),sha256=CLAIM_SHA),deferredUrlsExcluded=True,ordinaryFunctionCredit=0,encodedAssetBytes=0,measuredZeroAlignmentBytes=0)
    target=SOURCE/'layout.json'
    if target.exists()and read_json(target)!=layout:raise ValueError('Existing Auth character layout changed')
    if not target.exists():write_json(target,layout)
    print(dict(objects=102,bytes=1431,headerLines=len(text.splitlines()),layoutSha256=sha256(target)),flush=True)


if __name__=='__main__':main()
