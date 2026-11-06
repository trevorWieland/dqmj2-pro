import re
import ast
import struct
from project import ROOT,read_json,sha256

PINS={'deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gp-core-next/GP/gpi.c': '435ed0c0d18ddd881bbc6db8d9b8e7b501d172e23e3b063e72ce3d7300ec8250', 'deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gpi-connect/GP/gpiConnect.c': '13fedfe8fbaca9bc88860ae81dd4a63cabb2fe00e83cfb0ed3ff87a9a8e820d6', 'deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gp-core-next/snapshot.json': '30c63d9c4a39b48b3d49fc31fcb1118bd065bdef84b97d5ed8063a672da2096e', 'deps/reference/nitrowifi-e6048fc29448-socl-continuation-next/include/nitroWiFi/soc.h': '5411d7f9d20b249e36e689730efd20a8bd5fa90ce2e2df0cee9b0aae15ce9dbe', 'src/runtime/parallel_wave20261105/gpi-connect-next/peers/020b0534/context.h': '195e1d445fa211d3f4e573f3d803e20505c132426b6b8a5c096a53baf97e0d4c', 'evidence/lanes/parallel-wave20261106/gp-core-resume-next/first/type-evidence.json': '057b51ade22319ab15897efb283629173647eba3cccaad45a4080452202876f6'}
SOURCES={34253236: ('deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gp-core-next/GP/gpi.c', 'gpiReset', 'reset'), 34262740: ('deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gpi-connect/GP/gpiConnect.c', 'randomString', 'random'), 34262784: ('deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gpi-connect/GP/gpiConnect.c', 'gpiStartConnect', 'startup')}


def function(address):
    path,name,kind=SOURCES[address];text=(ROOT/path).read_text(encoding='utf-8');clean=re.sub(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|(/\*[\s\S]*?\*/|//[^\n]*)',lambda m:m[1]or'',text);m=re.search(r'(?:GPResult|void)\s+'+name+r'\s*\(',clean)
    if m is None:raise ValueError('Complete GP primary function missing')
    start=clean.index('{',m.end());end=start+1;depth=1
    while depth:
        depth+=(clean[end]=='{')-(clean[end]=='}');end+=1
    body=clean[m.start():end].replace(name,'native_main_%08x'%address,1)
    if kind=='reset':body=body.replace('iconnection->profileList.numBlocked = 0;','');body=re.sub(r'#ifdef GSI_UNICODE[\s\S]*?#endif','',body)
    if kind=='random':body=body.replace("'\\0'",'0')
    if kind=='startup':
        native=read_json(ROOT/'evidence/lanes/parallel-wave20261106/gp-core-resume-next/first/native-inputs.json');entry=next(e for e in native['entries']if int(e['address'],0)==address);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();strings={}
        for record in entry['originalRelocationRecords']:
            if'kind:load'not in record:continue
            target=int(record.split()[2][3:],0)
            if target&1:continue
            raw=image[target-0x02000000:].split(b'\0',1)[0]
            if all(b in[9,10,13]or 32<=b<127 for b in raw):strings[raw.decode('ascii')]=target
        for literal in set(re.findall(r'"(?:\\.|[^"\\])*"',body)):
            value=ast.literal_eval(literal)
            if value in strings:body=body.replace(literal,'native_data_%08x'%strings[value])
    return body


def tokens(text):return re.findall(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[A-Za-z_][A-Za-z_0-9]*|0x[0-9a-fA-F]+|[0-9]+|[^\s]',text)


def qualify():
    for name,digest in PINS.items():
        if sha256(ROOT/name)!=digest:raise ValueError('Pinned complete GP source/type lineage changed')
    for address in SOURCES:
        path=ROOT/('src/runtime/parallel_wave20261106/gp-core-resume-next/first/%08x/match.c'%address);source=path.read_text(encoding='utf-8').removeprefix('#include "context.h"\n')
        if tokens(source)!=tokens(function(address)):raise ValueError('Complete primary-derived GP function tokens differ')
    evidence=read_json(ROOT/'evidence/lanes/parallel-wave20261106/gp-core-resume-next/first/type-evidence.json');image=(ROOT/'extract/arm9/arm9.bin').read_bytes()
    if sha256(ROOT/'extract/arm9/arm9.bin')!=evidence['imageSha256']or(evidence['program'],evidence['processor'],evidence['module'],evidence['mode'])!=('','arm9','main','thumb'):raise ValueError('Native type evidence image/namespace differs')
    for fact in evidence['facts']:
        offset=int(fact['address'],0)-0x02000000
        if image[offset:offset+fact['bytes']].hex()!=fact['nativeHex']:raise ValueError('Actual consumed native field/width/constant word changed')
    if struct.unpack_from('<I',image,0xaab68)[0]+0x74!=evidence['keepaliveFieldOffset']or struct.unpack_from('<I',image,0xad110)[0]!=6500:raise ValueError('Actual native keepalive/default UDP port derivation differs')
    return dict(origin='Complete immutable primary GP C with measured DS release types/constants and original field words',primaryCommit='a2f340195975f4f042e28a60b62561dd9a0b2700',pins=[dict(path=name,sha256=digest)for name,digest in PINS.items()],fullPrimarySourceTokensVerified=True,sourceGenerationAndHeaderDependenciesSeparate=True,minimumConsumedContextViewNotStorageAuthorship=True,originalProviderAndStorageCredit=0)
