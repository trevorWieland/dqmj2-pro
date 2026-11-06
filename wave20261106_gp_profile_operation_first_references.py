import re
import ast
from project import ROOT,read_json,sha256

PREFIX='deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700'
SOURCES={0x020b0cd4:(PREFIX+'-gpi-profile/GP/gpiSearch.c','gpiStartProfileSearch'),0x020b0e04:(PREFIX+'-gpi-profile/GP/gpiSearch.c','gpiInitSearchData'),0x020b2908:(PREFIX+'-gp-profile-operation/GP/gpiUnique.c','gpiProcessRegisterUniqueNick'),0x020b29a0:(PREFIX+'-gp-profile-operation/GP/gpiUnique.c','gpiProcessRegisterCdKey'),0x020b30c8:(PREFIX+'-gstats-profile/gstats/gstats.c','PersistThink')}
LANE='evidence/lanes/parallel-wave20261106/gp-profile-operation-next/first'


def tokens(text):return re.findall(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[A-Za-z_][A-Za-z_0-9]*|0x[0-9a-fA-F]+|[0-9]+|[^\s]',text)


def function(a):
    path,name=SOURCES[a];text=(ROOT/path).read_text(encoding='utf-8');clean=re.sub(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|(/\*[\s\S]*?\*/|//[^\n]*)',lambda m:m[1]or'',text);m=re.search(r'(?:GPResult|int)\s+'+name+r'\s*\(',clean)
    if m is None:raise ValueError('Complete primary function missing')
    start=clean.index('{',m.end());end=start+1;depth=1
    while depth:depth+=(clean[end]=='{')-(clean[end]=='}');end+=1
    body=clean[m.start():end].replace(name,'native_main_%08x'%a,1)
    if a==0x020b30c8:body=body.replace('native_main_020b30c8()','native_main_020b30c8(void)');return body
    entry=next(e for e in read_json(ROOT/(LANE+'/native-inputs.json'))['entries']if int(e['address'],0)==a);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();strings={}
    for record in entry['originalRelocationRecords']:
        if'kind:load'not in record:continue
        target=int(record.split()[2][3:],0);raw=image[target-0x02000000:].split(b'\0',1)[0]
        if all(b in[9,10,13]or 32<=b<127 for b in raw):strings[raw.decode('ascii')]=target
    for literal in set(re.findall(r'"(?:\\.|[^"\\])*"',body)):
        value=ast.literal_eval(literal)
        if value in strings:body=body.replace(literal,'native_data_%08x'%strings[value])
    if a==0x020b0cd4:body=body.replace('GPSearchManagerHostname','native_data_%08x'%strings['gpsp.gs.nintendowifi.net'])
    return body


def qualify():
    evidence=read_json(ROOT/(LANE+'/derivation.json'))
    for pin in evidence['primaryPins']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Complete immutable primary source changed')
    for a in SOURCES:
        path=ROOT/('src/runtime/parallel_wave20261106/gp-profile-operation-next/first/%08x/match.c'%a);source=path.read_text(encoding='utf-8').removeprefix('#include "context.h"\n')
        if tokens(source)!=tokens(function(a)):raise ValueError('Complete primary-derived function tokens differ:'+hex(a))
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes()
    if sha256(ROOT/'extract/arm9/arm9.bin')!=evidence['imageSha256']:raise ValueError('Full original image changed')
    for fact in evidence['nativeFacts']:
        a=int(fact['address'],0)-0x02000000
        if image[a:a+fact['bytes']].hex()!=fact['nativeHex']:raise ValueError('Actual native field/context evidence changed')
    return dict(origin='Complete commit-pinned primary functions with measured DS340-byte search type and8-byte socket contract',primaryCommit='a2f340195975f4f042e28a60b62561dd9a0b2700',fullPrimarySourceTokensVerified=True,pins=evidence['primaryPins'],actualNativeContextFacts=evidence['nativeFacts'],minimumConsumedViewsNotStorageAuthorship=True,sourceGenerationAndCHeaderDependenciesSeparate=True,originalStorageAndProviderCredit=0)
