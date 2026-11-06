from project import ROOT,read_json,sha256


MANIFEST='evidence/verification/cohort172-superseded-frozen-source-inputs-v1-20261106.json'
MANIFEST_SHA='efba18f3de2d1ead4854416545f5a98396a843c68fe51442d15288faf9d145e7'


def classify(cohort,row):
    if cohort!=172 or row.get('classified'):return False
    if sha256(ROOT/MANIFEST)!=MANIFEST_SHA:raise ValueError('Superseded candidate classification manifest changed')
    proof=read_json(ROOT/MANIFEST);assert proof['sourceCredit']==0 and proof['cohort']==172
    pins={p['path']:p['sha256']for p in proof['files']}
    if row.get('path')not in pins:return False
    if row.get('sha256')!=pins[row['path']]or sha256(ROOT/row['path'])!=pins[row['path']]:return False
    for key in ['originalReady','originalInputManifest','replacementReady']:
        pin=proof[key]
        if sha256(ROOT/pin['path'])!=pin['sha256']:return False
    old=proof['originalReady']['path'];new=proof['replacementReady']['path']
    config=read_json(ROOT/'provenance/parallel-wave20261105-q-packets.json')
    if old in config['readyPackets']or new not in config['readyPackets']:return False
    recorded=read_json(ROOT/proof['originalReady']['path'])['frozenInputManifest']
    if recorded!=proof['originalInputManifest']:return False
    original={p['path']:p['sha256']for p in read_json(ROOT/recorded['path'])['files']}
    if not all(original.get(p)==h and sha256(ROOT/p)==h for p,h in pins.items()):return False
    selected={p for b in read_json(ROOT/'recovery.json')['batches']for p in b.get('sourceHashes',{})}
    if any(p in selected for p in pins):return False
    reports=read_json(ROOT/'evidence/verification/cohort-2026-10-29-172.json')['reports']
    for name in reports:
        if any(r.get('source')in pins for r in read_json(ROOT/name).get('matches',[])):return False
    row.update(classified=True,frozenSupersededCandidate=True,supersededSourceCredit=0,classificationManifest=MANIFEST,classificationManifestSha256=MANIFEST_SHA)
    return True
