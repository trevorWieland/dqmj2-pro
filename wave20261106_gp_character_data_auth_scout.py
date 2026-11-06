import bisect
import concurrent.futures
import hashlib
import re
import urllib.request
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from initialized_storage_protection_v2_20261106 import protected
from wave20261106_itcm_reset_next_data_scout import literals,RANGES,REVISION

FOLDER=ROOT/'evidence/lanes/parallel-wave20261106/whole-character-auth-read-only'
OLD='c6622266a9388d854443c659daf316fd9d1f540d'
MODERN='ba548986500a6628ec37c0603bdb94245ff12a63'


def references():
    roots=[(ROOT/'deps/reference'/('libntrdwc-'+OLD),'cybervisi0n/libntrdwc',OLD),(ROOT/'deps/reference'/('libntrdwc-auth-utility-'+OLD),'cybervisi0n/libntrdwc',OLD),(ROOT/'deps/reference'/('libntrdwc-http-followup-'+OLD),'cybervisi0n/libntrdwc',OLD),(ROOT/'deps/reference'/('nitrodwc-inet-modern-'+MODERN),'ntrtwl/NitroDWC',MODERN)]
    index={};seen=set();files={}
    for root,repository,commit in roots:
        for path in sorted(root.rglob('*')):
            if not path.is_file()or path.suffix not in('.c','.h'):continue
            upstream=path.relative_to(root).as_posix()
            if '/auth/'not in '/'+upstream and path.name!='dwc_connectinet.c':continue
            digest=sha256(path)
            if digest in seen:continue
            seen.add(digest);relative=path.relative_to(ROOT).as_posix();source=dict(path=relative,sha256=digest,repository='https://github.com/'+repository,primaryCommit=commit,upstreamPath=upstream,primaryUrl='https://raw.githubusercontent.com/'+repository+'/'+commit+'/'+upstream)
            files[relative]=source
            for value,info in literals(path.read_text(encoding='utf-8-sig')):index.setdefault(value,[]).append(dict(source,**info))
    return index,files


def verify_primary(pin):
    with urllib.request.urlopen(pin['primaryUrl'],timeout=30)as stream:data=stream.read()
    if hashlib.sha256(data).hexdigest()!=pin['sha256']:raise ValueError('Actual commit-pinned complete primary public file differs: '+pin['path'])
    return dict(pin,bytes=len(data),actualPinnedPublicGetSha256Matches=True,noLocalSourceModified=True)


def main():
    if FOLDER.resolve()!=(ROOT/'evidence/lanes/parallel-wave20261106/whole-character-auth-read-only').resolve():raise ValueError('Exact new read-only Auth evidence path differs')
    FOLDER.mkdir(parents=True,exist_ok=True);index,sources=references();image_path=ROOT/'extract/arm9/arm9.bin';image=image_path.read_bytes();symbols_path=ROOT/'config/arm9/symbols.txt';relocations_path=ROOT/'config/arm9/relocs.txt';symbols=symbols_path.read_text().splitlines();relocations=relocations_path.read_text().splitlines();all_addresses=[];data_symbols={};functions=[];pointers={}
    for line in symbols:
        match=re.fullmatch(r'(\S+) kind:(.+) addr:(0x[0-9a-f]+)',line)
        if match:
            address=int(match[3],0);all_addresses.append(address)
            if match[2]in('data','data(any)'):data_symbols[address]=line
        match=re.fullmatch(r'(\S+) kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)',line)
        if match:functions.append((int(match[4],0),int(match[4],0)+int(match[3],0),match[2],line))
    all_addresses=sorted(set(all_addresses));functions.sort();function_starts=[r[0]for r in functions]
    for line in relocations:
        match=re.fullmatch(r'from:(0x[0-9a-f]+) kind:load to:(0x[0-9a-f]+) module:main',line)
        if not match:continue
        origin,target=int(match[1],0),int(match[2],0);literal=image[origin-0x2000000:origin-0x2000000+4]
        if origin<0x2000000 or len(literal)!=4 or int.from_bytes(literal,'little')!=target:continue
        number=bisect.bisect_right(function_starts,origin)-1;fn=functions[number]if number>=0 and functions[number][0]<=origin<functions[number][1]else None
        pointers.setdefault(target,[]).append(dict(origin=hex(origin),originalRecord=line,literalWordHex=literal.hex(),containingConfiguredFunction=dict(program='',processor='arm9',module='main',mode=fn[2],address=hex(fn[0]),bytes=fn[1]-fn[0],canonicalRecord=fn[3])if fn else None))
    candidates=[]
    for address,record in sorted(data_symbols.items()):
        limit=next((a+n for a,n in RANGES if a<=address<a+n),None)
        if limit is None or address not in pointers:continue
        end=image.find(b'\0',address-0x2000000,min(limit-0x2000000,address-0x2000000+4096))
        if end<0:continue
        payload=image[address-0x2000000:end+1]
        if payload not in index:continue
        position=bisect.bisect_right(all_addresses,address);next_symbol=all_addresses[position]if position<len(all_addresses)else None
        if next_symbol and next_symbol<address+len(payload):continue
        reference=index[payload][0]
        candidates.append(dict(program='',processor='arm9',module='main',mode='data',kind='data',formatKind='whole-primary-c-character-object',address=hex(address),bytes=len(payload),endExclusive=hex(address+len(payload)),characterValue=payload[:-1].decode('ascii'),targetSha256=hashlib.sha256(payload).hexdigest(),nulTerminatorAddress=hex(address+len(payload)-1),configuredDataRecord=record,nextConfiguredSymbolAddress=hex(next_symbol)if next_symbol else None,originalPointerWitnesses=pointers[address],primaryReference=reference,objectType='narrow char[sizeof(complete primary C literal expression)]',includesExactlyOneFinalNulTerminator=True,sourceCredit=0,dataCredit=0))
    intervals,pins=protected(('','arm9','main'),REVISION);rows=[r for r in candidates if not any(max(int(r['address'],0),a)<min(int(r['endExclusive'],0),b)for a,b in intervals)];chosen={r['primaryReference']['path']:sources[r['primaryReference']['path']]for r in rows}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:primary=list(pool.map(verify_primary,chosen.values()))
    provenance=FOLDER/'primary-source-provenance.json';write_json(provenance,dict(textOnly=True,noPublicBinaryInputs=True,readOnlyActualPinnedPublicGetComparison=True,files=primary));snapshot=dict(path=provenance.relative_to(ROOT).as_posix(),sha256=sha256(provenance))
    for row in rows:row['primaryReference']['snapshot']=snapshot
    if any(sha256(ROOT/p['path'])!=p['sha256']for p in pins if p.get('path')):
        intervals,pins=protected(('','arm9','main'),REVISION);rows=[r for r in rows if not any(max(int(r['address'],0),a)<min(int(r['endExclusive'],0),b)for a,b in intervals)]
    if any(sha256(ROOT/p['path'])!=p['sha256']for p in pins if p.get('path')):raise ValueError('Auth character protection epoch unstable')
    for left,right in zip(rows,rows[1:]):
        if int(left['endExclusive'],0)>int(right['address'],0):raise ValueError('Whole Auth character objects internally overlap')
    document=dict(status='read-only-proposed-whole-Nintendo-DWC-authentication-and-HTTP-character-objects-needs-admission',sourceRevision=REVISION,scope=dict(program='',processor='arm9',module='main',mode='data'),objects=rows,objectCount=len(rows),opportunityBytes=sum(r['bytes']for r in rows),sourceCredit=0,dataCredit=0,newSourceAuthored=False,newClaimsCreated=False,configuredWholeObjectsWithFinalNulAndNoInteriorConfiguredBoundaries=True,actualOriginalFullPointerWords=True,primarySourceSnapshot=snapshot,sourcePins=primary,protectionPins=pins,protectedIntervals=len(intervals),protectionEpochStableAtPublication=True,allAcceptedPendingCurrentHistoricalFunctionDataLinkageAndStorageClaimsExcluded=True,gp259ClaimExcluded=True,authParameter020deb2c28BytesProtected=True,includesPreviouslyUncreditedNasTestUrl020deb48=any(int(r['address'],0)==0x20deb48 for r in rows),module=dict(path=image_path.relative_to(ROOT).as_posix(),sha256=sha256(image_path)),symbols=dict(path=symbols_path.relative_to(ROOT).as_posix(),sha256=sha256(symbols_path)),relocations=dict(path=relocations_path.relative_to(ROOT).as_posix(),sha256=sha256(relocations_path)),generator=dict(path=Path(__file__).name,sha256=sha256(__file__)),meaning='Whole primary C authentication/CAL/HTTP/NAS request field, format, diagnostic and URL character objects. Complete literal meaning and final NUL are retained; no executable bytes, arbitrary array slices or alignment are proposed.',limitations=['This is read-only object/context evidence and gives no storage ownership or byte credit.','Configured data(any) does not independently declare the original authors string-array type; coordinator must review actual complete source/API context and exact object boundaries.','Explicit nonexact/unresolved array capacities, embedded NUL fragments, wide literals, interior configured boundaries and protected overlaps are excluded.','New semantic source and real C generation require independent coordinator storage admission, followed by full typed-object/native/genuine-link/copied-root qualification.'])
    output=FOLDER/'proposal.json';write_json(output,document);print(dict(objects=len(rows),bytes=document['opportunityBytes'],primaryFiles=len(primary),originalPointerWords=sum(len(r['originalPointerWitnesses'])for r in rows),proposal=output.relative_to(ROOT).as_posix(),sha256=sha256(output)),flush=True)


if __name__=='__main__':main()
