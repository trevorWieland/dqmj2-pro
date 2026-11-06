import re
from project import ROOT,sha256

PRIMARY='deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gp-api/GP/gpiBuddy.c'
PINS={'deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gp-api/GP/gpiBuddy.c': '14c6e4725a5f705da58b8d7c23f57aed51ebfe24f545ce598b5e5fece5036e2e', 'deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gp-api/GP/gpiBuddy.h': '9ad8fd559500bdbf40a07340a41d3fc599de61ccd71bcdc67839592baa7ddf04', 'src/runtime/parallel_wave20261105/gpi-connect-next/peers/020b0534/context.h': '195e1d445fa211d3f4e573f3d803e20505c132426b6b8a5c096a53baf97e0d4c', 'src/runtime/parallel_wave20261105/gpi-connect-next/peers/020b0534/string.h': '65d1cd35334830d762fd29ffda8641a4c3bada2a68cd0597fbf181e886c1c3f9'}
FUNCTIONS={0x020abf18:'gpiSendServerBuddyMessage',0x020abfe4:'gpiSendBuddyMessage',0x020ac0d8:'gpiBuddyHandleKeyRequest'}


def generate(address):
    public=(ROOT/PRIMARY).read_text(encoding='utf-8')
    pattern=r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|(/\*[\s\S]*?\*/|//[^\n]*)'
    clean=re.sub(pattern,lambda m:m[1]or'',public);name=FUNCTIONS[address];m=re.search(r'GPResult\s+'+name+r'\s*\(',clean)
    if m is None:raise ValueError('Complete primary GP function missing')
    start=clean.index('{',m.end());depth=1;end=start+1
    while depth:
        depth+=(clean[end]=='{')-(clean[end]=='}');end+=1
    body=clean[m.start():end].replace(name,'native_main_%08x'%address,1)
    literals={'"\\\\bm\\\\"': 'native_data_020e0624', '"\\\\sesskey\\\\"': 'native_data_020e05f8', '"\\\\t\\\\"': 'native_data_020e0760', '"\\\\msg\\\\"': 'native_data_020e0678', '"\\\\final\\\\"': 'native_data_020e061c', '""': 'native_data_020e0764'}
    for left,right in literals.items():body=body.replace(left,right)
    if address==0x020ac0d8:body=body.replace('message = native_data_020e0764;','message = (char*)native_data_020e0764;')
    return '#include "context.h"\n'+body+'\n'


def qualify():
    for name,digest in PINS.items():
        if sha256(ROOT/name)!=digest:raise ValueError('Pinned complete GP primary/context lineage changed')
    for address in FUNCTIONS:
        source=ROOT/('src/runtime/parallel_wave20261106/gpi-buddy-resume-next/first/%08x/match.c'%address)
        if source.read_text(encoding='utf-8')!=generate(address):raise ValueError('Actual complete primary-derived GP source differs')
    return dict(origin='Complete commit-pinned public GP buddy C with independently measured DS interfaces/literals',primaryCommit='a2f340195975f4f042e28a60b62561dd9a0b2700',pins=[dict(path=name,sha256=digest)for name,digest in PINS.items()],fullSourceGenerationVerified=True,originalProviderAndStorageSourceCredit=0,unusedDeclarationsDoNotProveProviderABI=True)
