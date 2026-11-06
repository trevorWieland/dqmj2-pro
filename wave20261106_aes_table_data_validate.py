import hashlib
import re
import struct
from project import ROOT,read_json,sha256
from wave20261106_aes_table_data_paths import SOURCE,EVIDENCE,REFERENCE
from wave20261106_aes_table_data_materialize import CLAIM_SHA,IMAGE,IMAGE_SHA
from wave20261106_aes_table_data_codec import encode

OV_SYMBOLS='config/arm9/overlays/ov006/symbols.txt'
OV_RELOCS='config/arm9/overlays/ov006/relocs.txt'


def records():
    result=[]
    for line in(ROOT/OV_SYMBOLS).read_text().splitlines():
        match=re.fullmatch(r'(\S+) kind:(.+?) addr:(0x[0-9a-f]+)(?:\s+(.*))?',line)
        if match:result.append(dict(name=match[1],kind=match[2],address=int(match[3],0),qualifier=match[4]or'',record=line))
    return result


def validate_layout(layout):
    if sha256(EVIDENCE/'data-claim.json')!=CLAIM_SHA:raise ValueError('AES exact admitted storage changed')
    claim=read_json(EVIDENCE/'data-claim.json');fields=['program','processor','module','kind','mode','formatKind','address','bytes','elementType','elementCount','targetSha256','semanticSource','semanticSourceSha256'];admitted={row['address']:{k:row[k]for k in fields}for row in claim['claimedStorage']};seen=set();end=0
    if layout['objectCount']!=10 or layout['initializedBytes']!=10240 or len(layout['assets'])!=10:raise ValueError('AES exact ten complete arrays/10240B accounting differs')
    for row in layout['assets']:
        address=int(row['address'],0)
        if(row['program'],row['processor'],row['module'],row['kind'],row['mode'],row['formatKind'],row['elementType'],row['elementCount'],row['bytes'],row['compilerProcessor'],row['binary'],row['inputModuleSha256'],row['moduleBase'])!=('','arm9','ov006','data','data','aes-rijndael-transform-table','u32',256,1024,'arm946e',IMAGE,IMAGE_SHA,'0x21d7240'):raise ValueError('AES exact data namespace/type/whole extent/native module differs')
        if row['address']not in admitted or{k:row[k]for k in fields}!=admitted[row['address']]or address<end or address in seen:raise ValueError('AES whole table moved/overlapped/crossed admission')
        if sha256(ROOT/row['semanticSource'])!=row['semanticSourceSha256']or(ROOT/row['source']).resolve()!=(SOURCE/f'{address:08x}.c').resolve()or row['nativeSymbol']!=f"native_aes_{row['primarySymbol']}_{address:08x}":raise ValueError('AES actual mathematical descriptor/promoted C/symbol differs')
        if row['encodedAssetBytes']or row['measuredZeroAlignmentBytes']:raise ValueError('AES whole arrays confer gap/alignment credit')
        seen.add(address);end=address+1024


def validate_primary(document,payload):
    primary=document['primarySource'];path=ROOT/primary['path'];snapshot_path=REFERENCE/'reference-snapshot.json';snapshot=read_json(snapshot_path)
    if not path.resolve().is_relative_to(REFERENCE.resolve())or sha256(path)!=primary['sha256']or primary['commit']!='a6cf94577c0d1e5bca5304342e4ddffb18255afe'or primary['symbol']!=document['symbol']:raise ValueError('AES exact canonical primary declaration identity changed')
    if snapshot.get('commit')!=primary['commit']:raise ValueError('AES actual primary snapshot commit changed')
    entry=next((row for row in snapshot['files']if row['path']==primary['path']or(REFERENCE/row['path']).resolve()==path.resolve()),None)
    if not entry or entry['sha256']!=primary['sha256']:raise ValueError('AES primary canonical file/hash snapshot relation changed')
    text=path.read_text(encoding='utf-8');match=re.search(r'static const uint32_t '+document['symbol']+r'\[256\]\s*=\s*\{([^}]*)\};',text,re.S)
    if not match:raise ValueError('AES complete typed256word primary declaration absent')
    words=[int(token.strip().rstrip('uUlL'),0)for token in match[1].split(',')if token.strip()]
    if len(words)!=256 or struct.pack('<256I',*words)!=payload:raise ValueError('AES complete primary declaration disagrees with semantic finite-field generation')
    return dict(path=primary['path'],sha256=primary['sha256'],commit=primary['commit'],symbol=document['symbol'],line=text.count('\n',0,match.start())+1,completeWords=256)


def validate_native(row,payload,image):
    if hashlib.sha256(image).hexdigest()!=IMAGE_SHA:raise ValueError('AES full original overlay6 image changed')
    start=int(row['address'],0)-0x21d7240
    if len(payload)!=1024 or row['bytes']!=1024 or hashlib.sha256(payload).hexdigest()!=row['targetSha256']or image[start:start+1024]!=payload:raise ValueError('AES complete semantic table/word packing/typed extent differs from native')


def validate_views(row,document,payload,image):
    start=int(row['address'],0);inside=[r for r in records()if start<=r['address']<start+1024];normal=[r for r in inside if r['address']==start];views=document['existingConfiguredInteriorElementViews'];expected=[r for r in inside if r['address']!=start];main=(ROOT/'extract/arm9/arm9.bin').read_bytes();main_relocs=set((ROOT/'config/arm9/relocs.txt').read_text().splitlines());ov0=set((ROOT/'config/arm9/overlays/ov000/symbols.txt').read_text().splitlines())
    if len(normal)!=1 or normal[0]['kind']!='data(any)'or normal[0]['qualifier']or normal[0]['name']!=f'data_ov006_{start:08x}':raise ValueError('AES whole object lacks actual unambiguous overlay-local configured start')
    if len(views)!=len(expected)or{v['nativeAlias']for v in views}!={r['name']for r in expected}:raise ValueError('AES existing normal/ambiguous interior-label set changed')
    aliases={normal[0]['name']:row['address']}
    for view in views:
        address=int(view['address'],0);offset=address-start;record=next(r for r in expected if r['name']==view['nativeAlias'])
        if(view['program'],view['processor'],view['module'],view['kind'],view['wholeObjectAddress'],view['wholeObjectBytes'],view['owningWholeTable'],view['trailingQualifierPreserved'],view['additionalStorageBytes'],view['additionalDataObjects'],view['additionalFunctionBytes'])!=('','arm9','ov006','existing-ambiguous-element-view-only',row['address'],1024,document['symbol'],'ambiguous',0,0,0):raise ValueError('AES existing view namespace/object/zero-extra-credit identity changed')
        if record['kind']!='data(any)'or record['qualifier']!='ambiguous'or view['originalOverlay6ConfiguredRecord']!=record['record']or view['byteOffset']!=offset or offset%4 or not 0<offset<1024 or view['elementIndex']!=offset//4 or view['elementType']!='uint32_t'or view['viewBytes']!=4:raise ValueError('AES ambiguous view byte/element offset or original qualified record changed')
        native=image[address-0x21d7240:address-0x21d7240+4]
        if native!=payload[offset:offset+4]or native.hex()!=view['nativeElementBytesHex']or int.from_bytes(native,'little')!=int(view['nativeElementValue'],0)or view['primaryElementValue']!=view['nativeElementValue']:raise ValueError('AES complete native/primary ambiguous element word changed')
        if not view['pluralMainReferenceMustRemainUnresolved']or len(view['sameAddressOtherOverlayConfiguredRecords'])!=1 or len(view['actualOriginalMainReferences'])!=1 or not all(line in ov0 for line in view['sameAddressOtherOverlayConfiguredRecords']):raise ValueError('AES original multiple-overlay view was dropped/disambiguated')
        for pointer in view['actualOriginalMainReferences']:
            origin=int(pointer['origin'],0);literal=main[origin-0x2000000:origin-0x2000000+4]
            if(pointer['originProgram'],pointer['originProcessor'],pointer['originModule'],pointer['originalModuleExpression'],pointer['activeOverlayOrIntendedTargetNotInferred'],pointer['originalPluralNamespaceUnchanged'])!=('','arm9','main','overlays(0,6)',True,True)or pointer['originalRecord']not in main_relocs or pointer['originalRecord']!=f'from:0x{origin:08x} kind:load to:0x{address:08x} module:overlays(0,6)'or literal.hex()!=pointer['literalWordHex']or int.from_bytes(literal,'little')!=address:raise ValueError('AES original main pointer/plural overlay namespace was changed or rebound')
        aliases[view['nativeAlias']]=view['address']
    return aliases


def validate_pointers(layout,image):
    symbols=(ROOT/'config/arm9/overlays/ov006/symbols.txt').read_text().splitlines();functions=[]
    for line in symbols:
        match=re.fullmatch(r'\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)',line)
        if match:functions.append((int(match[3],0),int(match[3],0)+int(match[2],0),match[1],line))
    output=[]
    for row in layout['assets']:
        target=int(row['address'],0);pointers=[]
        for line in(ROOT/OV_RELOCS).read_text().splitlines():
            match=re.fullmatch(r'from:(0x[0-9a-f]+) kind:load to:0x%08x module:overlay\(6\)'%target,line)
            if not match:continue
            origin=int(match[1],0);literal=image[origin-0x21d7240:origin-0x21d7240+4];function=next((r for r in functions if r[0]<=origin<r[1]),None)
            if int.from_bytes(literal,'little')!=target or function is None or function[2]!='thumb':raise ValueError('AES actual configured Thumb caller/literal table pointer changed')
            pointers.append(dict(origin=hex(origin),target=row['address'],literalWordHex=literal.hex(),originalRecord=line,caller=dict(program='',processor='arm9',module='ov006',mode='thumb',address=hex(function[0]),bytes=function[1]-function[0],canonicalRecord=function[3])))
        if not pointers:raise ValueError('AES table lacks actual configured Thumb caller pointer witnesses')
        output.append(dict(address=row['address'],bytes=1024,originalPointerWitnesses=pointers))
    if len(output)!=10 or sum(len(r['originalPointerWitnesses'])for r in output)!=16:raise ValueError('AES exact original table-pointer witness set changed')
    return output
