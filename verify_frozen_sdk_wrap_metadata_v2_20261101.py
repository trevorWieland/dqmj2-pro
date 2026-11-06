import hashlib
from project import ROOT,read_json,sha256

BASE='evidence/research/20261101-public-sdk-reference/'
TREE=BASE+'pokeheartgold-tree.json'
MANIFEST='provenance/public-sdk-reference-research-ready-v4-20261101.json'
EXPECTED={
 'NitroSDK.wrap':('d7572757ff09f182ec0c97978120c293e796d6d02e558d7a99be471f775748aa','fff68664321578c2b8b777a8d3573b931cdde8c4'),
 'NitroSystem.wrap':('69987ac577bb38fa89a4ae004f921127a9deebd767225eca39d513a5cc7871bd','50bee25d6524a6b9a12b4ccd857362b5b9f17f01')}


def classify(findings):
    relevant=[row for row in findings if row['path']in {BASE+name for name in EXPECTED}]
    if not relevant:return
    assert sha256(ROOT/TREE)=='282f2a3141598e9108e33a80a0c3f2bc212eb6f6d61b79595335df2fa68eebd3'
    assert sha256(ROOT/MANIFEST)=='cf7781c6459cb43bb3cdb168fd7187adefa43ce09cf96045d226a34e7172b2df'
    tree=read_json(ROOT/TREE);commit=read_json(ROOT/(BASE+'pokeheartgold-commit.json'))
    assert commit['sha']=='e1d5a4606640e31c44d36714ad0b5cdd9c8763fd'
    assert not tree['truncated']
    def tree_digest(prefix):
        children=[dict(item,name=item['path'][len(prefix):])for item in tree['tree']
            if item['path'].startswith(prefix)and '/'not in item['path'][len(prefix):]]
        children.sort(key=lambda item:(item['name']+('/'if item['type']=='tree'else'')).encode())
        raw=b''.join(item['mode'].lstrip('0').encode()+b' '+item['name'].encode()+b'\0'+bytes.fromhex(item['sha'])for item in children)
        return hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    assert tree_digest('')==commit['commit']['tree']['sha']=='d12c0882b3d115a4aed20cc68286395314dc62ee'
    assert tree_digest('subprojects/')==next(item['sha']for item in tree['tree']if item['path']=='subprojects')
    declared={row['path']:row['sha256']for row in read_json(ROOT/MANIFEST)['files']}
    for row in relevant:
        name=row['path'].removeprefix(BASE);expected,blob=EXPECTED[name]
        data=(ROOT/row['path']).read_bytes()
        assert row['sha256']==sha256(ROOT/row['path'])==expected==declared[row['path']]
        entry=next(item for item in tree['tree']if item['path']=='subprojects/'+name)
        digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert digest==blob==entry['sha']and entry['type']=='blob'and entry['size']==len(data)
        row.update(classified=True,unmodifiedPublicUpstreamMetadata=True,upstreamGitBlobSha1=blob,
            pinManifest=MANIFEST,pinManifestSha256=sha256(ROOT/MANIFEST),sourceCredit=0,
            verifier='verify_frozen_sdk_wrap_metadata_v2_20261101.py',verifierSha256=sha256(__file__))
