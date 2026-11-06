import bisect
import hashlib
import json
import re
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from initialized_storage_protection_v2_20261106 import protected

EVIDENCE=ROOT/'evidence/lanes/parallel-wave20261106/whole-character-read-only'
REVISION='cfbac6c94de7d69bd70c92e81e652726cdb3c603'
RANGES=[(0x20d8d84,15848),(0x20dcd30,26064)]
TOKENS=re.compile(r'//[^\r\n]*|/\*[\s\S]*?\*/|(?:u8|L|u|U)?"(?:\\[\s\S]|[^"\\])*"|\x27(?:\\[\s\S]|[^\x27\\])*\x27')


def decode(token):
    if not token.startswith('"'):raise ValueError('Non-eight-bit literal')
    text=token[1:-1];out=bytearray();i=0;simple={'a':7,'b':8,'f':12,'n':10,'r':13,'t':9,'v':11,'\\':92,'"':34,"'":39,'?':63}
    while i<len(text):
        c=text[i];i+=1
        if c!='\\':
            if not 0<=ord(c)<128 or c in '\r\n':raise ValueError('Non-ASCII or invalid literal')
            out.append(ord(c));continue
        if i==len(text):raise ValueError('Truncated C escape')
        c=text[i];i+=1
        if c in simple:out.append(simple[c])
        elif c in '01234567':
            digits=c
            while i<len(text)and len(digits)<3 and text[i]in'01234567':digits+=text[i];i+=1
            value=int(digits,8)
            if value>255:raise ValueError('Non-byte octal escape')
            out.append(value)
        elif c=='x':
            start=i
            while i<len(text)and text[i]in'0123456789abcdefABCDEF':i+=1
            if i==start or int(text[start:i],16)>255:raise ValueError('Invalid byte hex escape')
            out.append(int(text[start:i],16))
        elif c=='\n':pass
        elif c=='\r'and i<len(text)and text[i]=='\n':i+=1
        else:raise ValueError('Unsupported C literal escape')
    return bytes(out)


def literals(text):
    matches=list(TOKENS.finditer(text));groups=[];current=None
    for m in matches:
        token=m.group()
        if token.startswith(('//','/*')):continue
        if not token.startswith('"'):
            if current:groups.append(current);current=None
            continue
        line_start=text.rfind('\n',0,m.start())+1
        if text[line_start:m.start()].lstrip().startswith(('#include','#line')):continue
        try:value=decode(token)
        except ValueError:
            if current:groups.append(current);current=None
            continue
        between=text[current['end']:m.start()]if current else None
        adjacent=current and not re.sub(r'/\*[\s\S]*?\*/|//[^\r\n]*|\s|\\\r?\n','',between)
        if adjacent:current.update(end=m.end(),value=current['value']+value)
        else:
            if current:groups.append(current)
            current=dict(start=m.start(),end=m.end(),value=value)
    if current:groups.append(current)
    for group in groups:
        value=group['value'];prefix=text[max(0,group['start']-160):group['start']];bound=re.search(r'\[([^\]]*)\]\s*=\s*$',prefix)
        if len(value)<4 or b'\0'in value or not all(x in(9,10,13)or 32<=x<127 for x in value):continue
        if bound and bound[1].strip():
            try:capacity=int(bound[1].strip(),0)
            except ValueError:continue
            if capacity!=len(value)+1:continue
        yield value+b'\0',dict(line=text.count('\n',0,group['start'])+1,literalExpression=text[group['start']:group['end']],surroundingContext=text[max(0,group['start']-100):min(len(text),group['end']+100)],explicitArrayExtentMatches=bool(bound and bound[1].strip()),automaticCharacterArray=bool(bound and not bound[1].strip()))


def primary_literals():
    index={};files=[];seen=set();roots=[ROOT/'deps/reference',ROOT/'deps/msl-ansi-reference-20261031']
    for base in roots:
        for path in sorted(base.rglob('*')):
            if path.suffix.lower()not in('.c','.h')or not path.is_file():continue
            data=path.read_bytes();digest=hashlib.sha256(data).hexdigest()
            if digest in seen:continue
            seen.add(digest)
            try:text=data.decode('utf-8-sig')
            except UnicodeDecodeError:continue
            relative=path.relative_to(ROOT).as_posix();files.append(dict(path=relative,sha256=digest))
            for value,info in literals(text):
                if len(index.setdefault(value,[]))<4:index[value].append(dict(path=relative,sha256=digest,**info))
    return index,files


def main():
    if EVIDENCE.resolve()!=(ROOT/'evidence/lanes/parallel-wave20261106/whole-character-read-only').resolve()or not EVIDENCE.resolve().is_relative_to(ROOT.resolve()):raise ValueError('Exact read-only character evidence path differs')
    EVIDENCE.mkdir(parents=True,exist_ok=True);image_path=ROOT/'extract/arm9/arm9.bin';image=image_path.read_bytes();symbols_path=ROOT/'config/arm9/symbols.txt';relocs_path=ROOT/'config/arm9/relocs.txt';symbols=symbols_path.read_text();relocs=relocs_path.read_text();data_symbols={};all_addresses=[]
    for line in symbols.splitlines():
        match=re.fullmatch(r'(\S+) kind:(.+) addr:(0x[0-9a-f]+)',line)
        if match:
            address=int(match[3],0);all_addresses.append(address)
            if match[2]in('data','data(any)'):data_symbols[address]=line
    all_addresses=sorted(set(all_addresses));pointers={}
    for line in relocs.splitlines():
        match=re.fullmatch(r'from:(0x[0-9a-f]+) kind:load to:(0x[0-9a-f]+) module:main',line)
        if not match:continue
        origin,target=int(match[1],0),int(match[2],0)
        if 0x2000000<=origin<0x2000000+len(image)-3 and int.from_bytes(image[origin-0x2000000:origin-0x2000000+4],'little')==target:pointers.setdefault(target,[]).append(dict(origin=hex(origin),originalRecord=line,literalWordHex=image[origin-0x2000000:origin-0x2000000+4].hex()))
    index,source_pins=primary_literals();print(dict(primaryFiles=len(source_pins),distinctLiteralObjects=len(index)),flush=True);intervals,pins=protected(('','arm9','main'),REVISION);candidates=[];rejections={};raw_printable=0
    for address,record in sorted(data_symbols.items()):
        limit=next((a+n for a,n in RANGES if a<=address<a+n),None)
        if limit is None:continue
        end=image.find(b'\0',address-0x2000000,min(limit-0x2000000,address-0x2000000+4096))
        if end<0:continue
        value=image[address-0x2000000:end+1]
        if len(value)<5 or not all(x in(9,10,13)or 32<=x<127 for x in value[:-1]):continue
        raw_printable+=1;next_symbol=all_addresses[bisect.bisect_right(all_addresses,address)]if bisect.bisect_right(all_addresses,address)<len(all_addresses)else None
        reasons=[]
        if value not in index:reasons.append('no-complete-primary-C-literal-expression')
        if address not in pointers:reasons.append('no-actual-original-pointer-relocation')
        if next_symbol is not None and next_symbol<address+len(value):reasons.append('configured-interior-boundary')
        if any(max(address,a)<min(address+len(value),b)for a,b in intervals):reasons.append('accepted-pending-function-data-linkage-or-reservation-overlap')
        if reasons:
            for reason in reasons:rejections[reason]=rejections.get(reason,0)+1
            continue
        candidates.append(dict(program='',processor='arm9',module='main',kind='data',mode='data',address=hex(address),bytes=len(value),endExclusive=hex(address+len(value)),characterValue=value[:-1].decode('ascii'),targetSha256=hashlib.sha256(value).hexdigest(),nulTerminatorAddress=hex(address+len(value)-1),configuredDataRecord=record,nextConfiguredSymbolAddress=hex(next_symbol)if next_symbol else None,originalPointerWitnesses=pointers[address],primaryCompleteCLiteralExpressions=index[value],objectQualification='Configured start, exact entire primary C literal expression plus terminator, no internal configured boundary, actual original native pointer words; storage still requires coordinator object/context review.',sourceCredit=0,dataCredit=0))
    changed=[p['path']for p in pins if p.get('path')and sha256(ROOT/p['path'])!=p['sha256']]
    if changed:
        intervals,pins=protected(('','arm9','main'),REVISION);candidates=[x for x in candidates if not any(max(int(x['address'],0),a)<min(int(x['endExclusive'],0),b)for a,b in intervals)]
        if any(p.get('path')and sha256(ROOT/p['path'])!=p['sha256']for p in pins):raise ValueError('Protection epoch remained unstable')
    families={}
    for row in candidates:
        path=row['primaryCompleteCLiteralExpressions'][0]['path'];family='GameSpy'if 'gamespy'in path.lower()else 'NintendoDWC'if 'dwc'in path.lower()else 'NitroSDK'if 'nitrosdk'in path.lower()else 'MSL'or'other';families.setdefault(family,[]).append(row)
    value=dict(status='read-only-proposed-whole-character-objects-no-admission',sourceCredit=0,dataCredit=0,newSourceAuthored=False,newStorageClaimsCreated=False,sourceRevision=REVISION,namespace=dict(program='',processor='arm9',module='main',mode='data'),requestedRanges=[dict(address=hex(a),bytes=n)for a,n in RANGES],module=dict(path=image_path.relative_to(ROOT).as_posix(),sha256=sha256(image_path)),symbols=dict(path=symbols_path.relative_to(ROOT).as_posix(),sha256=sha256(symbols_path)),relocations=dict(path=relocs_path.relative_to(ROOT).as_posix(),sha256=sha256(relocs_path)),protectionPins=pins,protectionEpochStableAtPublication=True,protectedIntervals=len(intervals),primarySourcePins=source_pins,rawConfiguredPrintableCandidates=raw_printable,rejections=rejections,wholeCharacterCandidates=candidates,candidateObjects=len(candidates),candidateBytes=sum(x['bytes']for x in candidates),familySummary={k:dict(objects=len(v),bytes=sum(x['bytes']for x in v))for k,v in families.items()},limitations=['Native printable bytes alone were never accepted as data.','Explicit nonexact or unresolved array bounds, embedded NUL fragments, wide/invalid literals, configured interior symbols and all protected overlaps were refused.','Matching primary literals and pointer geometry support read-only triage; exact declaration/API context, primary snapshot provenance and coordinator fresh admission still required.','No source, arbitrary array slice, original input, shared registry or storage claim was written.'])
    write_json(EVIDENCE/'inventory.json',value);print(dict(objects=value['candidateObjects'],bytes=value['candidateBytes'],families=value['familySummary'],sha256=sha256(EVIDENCE/'inventory.json')),flush=True)


if __name__=='__main__':main()
