import hashlib
import re
from project import ROOT,read_json,sha256
from wave20261106_auth_character_data_paths import SOURCE,EVIDENCE
from wave20261106_auth_character_data_materialize import CLAIM_SHA,IMAGE,IMAGE_SHA
from wave20261106_auth_character_data_codec import encode,render

SYMBOLS_SHA='95524d3e054b6841fe907788758e6f506fe8eba7f63119f1e96cf667de82b374'
RELOCS_SHA='4467aa2f299dcfcd32dd3744cbf37bec9e545cb29fc77e0b41287465101adc9e'


def validate_layout(layout):
    if sha256(EVIDENCE/'data-claim.json')!=CLAIM_SHA:raise ValueError('Auth admitted complete storage membership changed')
    claim=read_json(EVIDENCE/'data-claim.json');fields=['program','processor','module','kind','mode','formatKind','address','bytes','targetSha256','semanticSource','semanticSourceSha256'];admitted={row['address']:{k:row[k]for k in fields}for row in claim['claimedStorage']};seen=set();end=0
    if layout['objectCount']!=102 or layout['initializedBytes']!=1431 or len(layout['assets'])!=102:raise ValueError('Auth102/1431 layout accounting differs')
    for row in layout['assets']:
        address=int(row['address'],0)
        if(row['program'],row['processor'],row['module'],row['mode'],row['kind'],row['formatKind'],row['compilerProcessor'],row['binary'],row['inputModuleSha256'],row['moduleBase'])!=('','arm9','main','data','data','whole-primary-c-character-object','arm946e',IMAGE,IMAGE_SHA,'0x2000000'):raise ValueError('Auth exact data namespace/native module changed')
        if row['address']not in admitted or{k:row[k]for k in fields}!=admitted[row['address']]or address in seen or address<end or address in(0x20deb48,0x20defec):raise ValueError('Auth complete object moved/overlapped/crossed admission or deferred URL')
        if row['nativeSymbol']!=f'native_auth_character_{address:08x}'or(ROOT/row['source']).resolve()!=(SOURCE/f'{address:08x}.c').resolve()or row['encodedAssetBytes']or row['measuredZeroAlignmentBytes']:raise ValueError('Auth promoted source or no-gap/alignment identity changed')
        if sha256(ROOT/row['semanticSource'])!=row['semanticSourceSha256']:raise ValueError('Auth admitted readable semantics changed')
        seen.add(address);end=address+row['bytes']
    if len(seen)!=102 or sum(row['bytes']for row in layout['assets'])!=1431:raise ValueError('Auth complete object counts changed')


def validate_reference(document):
    ref=document['primaryReference'];source=ROOT/ref['path'];snapshot=ROOT/ref['snapshot']['path']
    if not source.resolve().is_relative_to((ROOT/'deps/reference').resolve())or sha256(source)!=ref['sha256']or sha256(snapshot)!=ref['snapshot']['sha256']:raise ValueError('Auth actual pinned primary C or source provenance changed')
    if(ref['primaryCommit'],ref['repository'])not in [('c6622266a9388d854443c659daf316fd9d1f540d','https://github.com/cybervisi0n/libntrdwc'),('ba548986500a6628ec37c0603bdb94245ff12a63','https://github.com/ntrtwl/NitroDWC')]:raise ValueError('Auth exact admitted primary source revision differs')
    item=next((r for r in read_json(snapshot)['files']if r['path']==ref['path']),None)
    if not item or item['sha256']!=ref['sha256']or item['primaryCommit']!=ref['primaryCommit']or item['primaryUrl']!=ref['primaryUrl']:raise ValueError('Auth complete primary URL/hash relationship changed')
    text=source.read_text(encoding='utf-8-sig');lines=text.splitlines(keepends=True);line=ref['line']
    if not 1<=line<=len(lines)or ref['literalExpression']!=document['literalExpression']:raise ValueError('Auth actual complete primary literal identity changed')
    start=sum(len(s)for s in lines[:line-1]);position=text.find(ref['literalExpression'],start)
    if position<start or position>=start+len(lines[line-1]):raise ValueError('Auth complete primary literal expression absent at actual pinned line')
    encode(document)


def validate_native(row,payload,image):
    if hashlib.sha256(image).hexdigest()!=IMAGE_SHA:raise ValueError('Full original Auth native image changed')
    start=int(row['address'],0)-0x2000000
    if len(payload)!=row['bytes']or payload[-1:]!=b'\0'or b'\0'in payload[:-1]or hashlib.sha256(payload).hexdigest()!=row['targetSha256']or image[start:start+len(payload)]!=payload:raise ValueError('Auth complete character value/NUL/extent differs from native object')


def validate_pointers(layout,image):
    if sha256(ROOT/'config/arm9/symbols.txt')!=SYMBOLS_SHA or sha256(ROOT/'config/arm9/relocs.txt')!=RELOCS_SHA:raise ValueError('Original Auth configured data/functions/relocations changed')
    proposal=read_json(ROOT/'evidence/lanes/parallel-wave20261106/whole-character-auth-read-only/proposal.json');rows={r['address']:r for r in proposal['objects']};symbols=(ROOT/'config/arm9/symbols.txt').read_text().splitlines();relocs=set((ROOT/'config/arm9/relocs.txt').read_text().splitlines());out=[]
    for asset in layout['assets']:
        row=rows[asset['address']];address=int(row['address'],0);end=address+asset['bytes']
        if row['bytes']!=asset['bytes']or row['targetSha256']!=asset['targetSha256']or row['configuredDataRecord']not in symbols or not re.fullmatch(r'data_%08x kind:data\(any\) addr:0x%08x'%(address,address),row['configuredDataRecord']):raise ValueError('Auth exact original configured whole data start differs')
        if any(address<int(m[1],0)<end for line in symbols if(m:=re.search(r' addr:(0x[0-9a-f]+)$',line))):raise ValueError('Auth proposed character object has an interior configured boundary')
        callers=[]
        for pointer in row['originalPointerWitnesses']:
            origin=int(pointer['origin'],0);record=pointer['originalRecord'];raw=image[origin-0x2000000:origin-0x2000000+4]
            if record not in relocs or record!=f'from:0x{origin:08x} kind:load to:0x{address:08x} module:main'or raw.hex()!=pointer['literalWordHex']or int.from_bytes(raw,'little')!=address:raise ValueError('Auth actual full native pointer word/origin/kind/target changed')
            function=pointer['containingConfiguredFunction']
            if function:
                start=int(function['address'],0)
                if(function['program'],function['processor'],function['module'])!=('','arm9','main')or function['mode']not in('arm','thumb')or not start<=origin<start+function['bytes']or function['canonicalRecord']not in symbols or not re.fullmatch(r'\S+ kind:function\(%s,size=0x%x\) addr:0x%08x'%(function['mode'],function['bytes'],start),function['canonicalRecord']):raise ValueError('Auth configured native caller boundary/mode/namespace changed')
                callers.append(pointer)
        if not callers:raise ValueError('Auth complete data object lacks required configured caller-function pointer witness')
        out.append(dict(address=row['address'],bytes=row['bytes'],originalPointers=row['originalPointerWitnesses'],configuredCallerWitnesses=len(callers),nativeAlias=f'data_{address:08x}'))
    if len(out)!=102:raise ValueError('Auth configured caller data membership differs')
    return out
