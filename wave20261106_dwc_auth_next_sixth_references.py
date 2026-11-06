from project import ROOT,read_json,sha256

REFERENCE='deps/reference/libntrdwc-ac-c6622266a9388d854443c659daf316fd9d1f540d'
SNAPSHOT_SHA='fd8d1c26536b0c8f44e49538b708ae873bb30b2db1a09e68bd7b89aebe646868'


def qualify():
    snapshot=ROOT/REFERENCE/'snapshot.json'
    if sha256(snapshot)!=SNAPSHOT_SHA:raise ValueError('Actual immutable AC source snapshot changed')
    value=read_json(snapshot)
    if value['commit']!='c6622266a9388d854443c659daf316fd9d1f540d' or value['repository']!='https://github.com/cybervisi0n/libntrdwc' or not value['textOnly'] or len(value['files'])!=28:raise ValueError('Exact primary AC reference provenance differs')
    for pin in value['files']:
        path=ROOT/pin['path'];raw=path.read_bytes()
        if not path.resolve().is_relative_to((ROOT/REFERENCE).resolve()) or sha256(path)!=pin['sha256'] or len(raw)!=pin['bytes'] or bytes(1) in raw:raise ValueError('Actual raw public AC file changed')
        raw.decode('utf-8')
    return dict(repository=value['repository'],commit=value['commit'],snapshot=REFERENCE+'/snapshot.json',snapshotSha256=SNAPSHOT_SHA,files=value['files'],unmodifiedRawTextOnly=True,prebuiltObjectsUsed=False,sourceCredit=0)
