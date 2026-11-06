import hashlib
import re
from project import ROOT,read_json,sha256
from wave20261106_gp_character_data_paths import SOURCE,EVIDENCE,assert_owned
from wave20261106_gp_character_data_codec import encode,render

IMAGE='extract/arm9/arm9.bin'
IMAGE_SHA='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'


def validate_layout(layout,claim):
    if (layout['program'],layout['processor'],layout['module'],layout['kind'],layout['mode'])!=('','arm9','main','data','data')or layout['objectCount']!=259 or layout['initializedBytes']!=3696:raise ValueError('Exact complete GP character layout namespace/accounting differs')
    if claim['functionCount']!=0 or claim['functionOwnershipGranted']or len(claim['claimedStorage'])!=259:raise ValueError('GP character ownership acquired executable scope')
    fields=['program','processor','module','kind','mode','formatKind','address','bytes','targetSha256','semanticSource','semanticSourceSha256'];expected={x['address']:{k:x[k]for k in fields}for x in claim['claimedStorage']};seen=set();end=0
    for row in layout['assets']:
        address=int(row['address'],0)
        if (row['program'],row['processor'],row['module'],row['mode'],row['kind'],row['compilerProcessor'],row['binary'],row['inputModuleSha256'],row['moduleBase'])!=('','arm9','main','data','data','arm946e',IMAGE,IMAGE_SHA,'0x2000000'):raise ValueError('GP character object namespace/native module differs')
        if row['address']not in expected or {k:row[k]for k in fields}!=expected[row['address']]or address<end or address in seen:raise ValueError('Character object moved, changed extent/native identity, overlapped or duplicated')
        if row['nativeSymbol']!=f'native_gp_character_{address:08x}'or row['encodedAssetBytes']or row['measuredZeroAlignmentBytes']:raise ValueError('Character object symbol or gap/alignment accounting differs')
        if (ROOT/row['source']).resolve()!=(SOURCE/f'{address:08x}.c').resolve():raise ValueError('GP character source identity escaped selected object')
        seen.add(address);end=address+row['bytes']
    if len(seen)!=259 or sum(x['bytes']for x in layout['assets'])!=3696:raise ValueError('GP character membership dropped or inflated')


def validate_reference(document):
    ref=document['primaryReference'];source=ROOT/ref['path'];snapshot=ROOT/ref['snapshot']['path']
    if not source.resolve().is_relative_to(ROOT/'deps/reference')or sha256(source)!=ref['sha256']or sha256(snapshot)!=ref['snapshot']['sha256']:raise ValueError('Actual primary GP C/snapshot identity changed')
    manifest=read_json(snapshot);commit=manifest.get('commit',manifest.get('primaryCommit'))
    if commit!=ref['primaryCommit']or commit!='a2f340195975f4f042e28a60b62561dd9a0b2700':raise ValueError('Complete primary GP commit changed')
    item=next((x for x in manifest['files']if x['path']==ref['path']or(snapshot.parent/x['path']).resolve()==source.resolve()),None)
    if not item or item['sha256']!=ref['sha256']or item['url']!=ref['primaryUrl']:raise ValueError('Primary GP URL/hash/source relationship changed')
    text=source.read_text(encoding='utf-8-sig');line=ref['line'];lines=text.splitlines()
    if not 1<=line<=len(lines)or document['literalExpression']!=ref['literalExpression']or ref['literalExpression']not in lines[line-1]:raise ValueError('Complete original GP literal expression absent at actual pinned source line')
    return dict(path=ref['path'],sha256=ref['sha256'],line=line,primaryUrl=ref['primaryUrl'],snapshot=ref['snapshot'],completeLiteralExpression=True)


def validate_native(row,payload,image):
    if hashlib.sha256(image).hexdigest()!=IMAGE_SHA:raise ValueError('Full original main image changed')
    address=int(row['address'],0);start=address-0x2000000
    if len(payload)!=row['bytes']or payload[-1:]!=b'\0'or b'\0'in payload[:-1]or hashlib.sha256(payload).hexdigest()!=row['targetSha256']or image[start:start+len(payload)]!=payload:raise ValueError('Complete character value/NUL/extent does not match original native object')


def validate_pointers(proposal,image):
    symbols=(ROOT/'config/arm9/symbols.txt').read_text();relocs=set((ROOT/'config/arm9/relocs.txt').read_text().splitlines());out=[]
    for row in proposal['objects']:
        address=int(row['address'],0);end=address+row['bytes'];record=row['configuredDataRecord']
        if record not in symbols.splitlines()or not re.fullmatch(r'\S+ kind:data(?:\(any\))? addr:0x%08x'%address,record):raise ValueError('Original configured character data start/kind changed')
        for line in symbols.splitlines():
            m=re.search(r' addr:(0x[0-9a-f]+)$',line)
            if m and address<int(m[1],0)<end:raise ValueError('Original character object has an interior configured boundary')
        for witness in row['originalPointerWitnesses']:
            origin=int(witness['origin'],0);record=witness['originalRecord'];literal=image[origin-0x2000000:origin-0x2000000+4]
            if record not in relocs or record!=f'from:0x{origin:08x} kind:load to:0x{address:08x} module:main'or literal.hex()!=witness['literalWordHex']or int.from_bytes(literal,'little')!=address:raise ValueError('Full original character pointer word/origin/kind/module changed')
            out.append(dict(origin=hex(origin),target=hex(address),literalWordHex=literal.hex(),originalRecord=record))
    if len(out)!=387:raise ValueError('Complete original character pointer set differs')
    return out


def source_bytes(row,document):
    code,payload=render(document,row['nativeSymbol']);source=ROOT/row['source']
    if sha256(source)!=row['sourceSha256']or source.read_text(encoding='utf-8')!=code:raise ValueError('Actual readable C initializer differs from semantic primary literal')
    return payload
