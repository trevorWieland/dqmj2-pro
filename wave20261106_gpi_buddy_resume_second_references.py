import re
from project import ROOT,sha256

PRIMARY='deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gp-api/GP/gpiBuddy.c'
PINS={'deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gp-api/GP/gpiBuddy.c': '14c6e4725a5f705da58b8d7c23f57aed51ebfe24f545ce598b5e5fece5036e2e', 'deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gp-api/GP/gpiBuddy.h': '9ad8fd559500bdbf40a07340a41d3fc599de61ccd71bcdc67839592baa7ddf04', 'src/runtime/parallel_wave20261105/gpi-connect-next/peers/020b0534/context.h': '195e1d445fa211d3f4e573f3d803e20505c132426b6b8a5c096a53baf97e0d4c', 'src/runtime/parallel_wave20261105/gpi-connect-next/peers/020b0534/string.h': '65d1cd35334830d762fd29ffda8641a4c3bada2a68cd0597fbf181e886c1c3f9', 'deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gp-api/GP/gp.h': '650559eb74b41b9aaad68bc502fee331b5e620b70fd2f3cbc612202b1bc238d4', 'deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gp-callback/GP/gpiCallback.h': '5edd993aee037b428ba4cdbde7157be89411a7ccc5028aea43835863278539f5', 'deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gpi-keys/GP/gpiKeys.h': 'b79dceb849a522b47224430bacc32a2873c74b220f6316cf647335b1ed7bc780', 'deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gp-buffer/GP/gpiUtility.h': '8df0478487a18fcb411d889908d829f2ea8f8f31d7278294e884dae4e4b9f5a4'}
FUNCTIONS={0x020ac130:'gpiBuddyHandleKeyReply'}


def generate(address):
    public=(ROOT/PRIMARY).read_text(encoding='utf-8')
    pattern=r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|(/\*[\s\S]*?\*/|//[^\n]*)'
    clean=re.sub(pattern,lambda m:m[1]or'',public);name=FUNCTIONS[address];m=re.search(r'GPResult\s+'+name+r'\s*\(',clean)
    if m is None:raise ValueError('Complete primary GP function missing')
    start=clean.index('{',m.end());depth=1;end=start+1
    while depth:
        depth+=(clean[end]=='{')-(clean[end]=='}');end+=1
    body=clean[m.start():end].replace(name,'native_main_%08x'%address,1)
    literals={'"Invalid profile."': 'native_data_020e0768', '""': 'native_data_020e0764', '"keys"': 'native_data_020e077c', '"Error reading keys reply message"': 'native_data_020e0784'}
    for left,right in literals.items():body=body.replace(left,right)
    body=re.sub(r'#ifdef GSI_UNICODE[\s\S]*?#else([\s\S]*?)#endif',lambda m:m[1],body)
    return '#include "context.h"\n'+body+'\n'


def qualify():
    for name,digest in PINS.items():
        if sha256(ROOT/name)!=digest:raise ValueError('Pinned complete GP primary/context lineage changed')
    for address in FUNCTIONS:
        source=ROOT/('src/runtime/parallel_wave20261106/gpi-buddy-resume-next/second/%08x/match.c'%address)
        if source.read_text(encoding='utf-8')!=generate(address):raise ValueError('Actual complete primary-derived GP source differs')
    return dict(origin='Complete commit-pinned public GP buddy C with independently measured DS interfaces/literals',primaryCommit='a2f340195975f4f042e28a60b62561dd9a0b2700',pins=[dict(path=name,sha256=digest)for name,digest in PINS.items()],fullSourceGenerationVerified=True,originalProviderAndStorageSourceCredit=0,unusedDeclarationsDoNotProveProviderABI=True)
