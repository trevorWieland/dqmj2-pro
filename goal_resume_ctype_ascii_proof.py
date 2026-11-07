import copy
import gzip
import hashlib
import importlib.util
import json
import struct
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
from goal_resume_ctype_ascii_data import SOURCE,LANE,WORK,AUDIT,TABLES,guarded_render
from goal_resume_ctype_ascii_build import build


def native_reader():
    path=AUDIT/'native_bounds.py';spec=importlib.util.spec_from_file_location('frozen_ascii_native_bounds',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def inputs():
    if sha256(LANE/'claim.json')!='9bedf34d3fe30396ab7c0ad80b6166fd9c5e49a186e0913d78d5407e9f712e7a':raise ValueError('Admitted ctype claim changed')
    for p in read_json(AUDIT/'seal.json')['files']:
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Preserved read-only audit changed')
    if(LANE/'inputs.json').exists():
        for p in read_json(LANE/'inputs.json')['files']:
            if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError(('Frozen data replay input changed',p['path']))
    return read_json(LANE/'claim.json')['claimedStorage']


def identity(row,admitted):
    scope=lambda x:((x.get('program')or''),x['processor'],x['module'],x['mode'],x.get('targetSection',x.get('section')),int(x['address'],0),x['bytes'],x.get('elementBytes',x.get('width')))
    if scope(row)!=scope(admitted):raise ValueError('Bounded physical data identity/geometry changed')


def pair_readers(image,replaced):
    reader=native_reader();traces=[]
    for point in sorted(set(range(-256,256))|{-0x80000000,256,65535,0x7fffffff}):
        setup=[(reader.SP,struct.pack('<III',0x02600100,0x02600104,0x02600108))]
        args=[36,3,reader.CALLBACK,0x02600000];a=reader.execute(image,0x0201ed2c,args,setup,point);b=reader.execute(replaced,0x0201ed2c,args,setup,point)
        expected=point-48 if 48<=point<=57 else point-65+10 if 65<=point<=90 else point-97+10 if 97<=point<=122 else 0
        if a!=b or a['returned']!=expected or(not 0<=point<128 and a['reads']):raise ValueError(('Compiled ASCII data changes original signed reader/model',point))
        traces.append(dict(reader='0x0201ed2c',signedCodepoint=point,result=a))
    for point in list(range(256))+[256,0x7fff,0xfffe,0xffff]:
        setup=[(0x02600000,struct.pack('<4H',ord('%'),point,ord('d'),0)),(0x02600100,struct.pack('<I',0x02600200)),(0x02600200,bytes(64)),(0x02600300,bytes(64))]
        args=[0x02600000,0x02600100,0x02600300];a=reader.execute(image,0x0201f2c0,args,setup);b=reader.execute(replaced,0x0201f2c0,args,setup)
        if a!=b or(point>=128 and a['reads']):raise ValueError(('Compiled wide ASCII data changes original reader/bounds',point))
        if 49<=point<=57 and a['returned']!=0x02600006:raise ValueError('Independent wide decimal-width format route differs')
        traces.append(dict(reader='0x0201f2c0',wideCodepoint=point,result=a))
    return traces


def wrong_predicates(image):
    variants=[('upper-excludes-a',0,"#define ASCII_TO_UPPER(c) (ASCII_IS_LOWER(c)?(c)-'a'+'A':(c))","#define ASCII_TO_UPPER(c) ((ASCII_IS_LOWER(c)&&(c)!='a')?(c)-'a'+'A':(c))",97),('narrow-excludes-digit5',1,"#define ASCII_IS_DIGIT(c) ASCII_BETWEEN(c,'0','9')","#define ASCII_IS_DIGIT(c) (ASCII_BETWEEN(c,'0','9')&&(c)!='5')",53),('wide-excludes-digit5',2,"#define ASCII_IS_DIGIT(c) ASCII_BETWEEN(c,'0','9')","#define ASCII_IS_DIGIT(c) (ASCII_BETWEEN(c,'0','9')&&(c)!='5')",53)]
    reader=native_reader();results=[]
    for index,(name,which,before,after,point)in enumerate(variants):
        row=TABLES[which];source=SOURCE/row['filename'];text=source.read_text()
        if text.count(before)!=1:raise ValueError('Wrong ASCII predicate source edit is ambiguous')
        folder=WORK/'negative'/str(index);folder.mkdir(parents=True,exist_ok=True);bad=folder/source.name;bad.write_text(text.replace(before,after));payload,proof=build(bad,row,folder/'build')
        start=int(row['address'],0)-0x02000000;mutated=bytearray(image);mutated[start:start+row['bytes']]=payload
        if payload==image[start:start+row['bytes']]:raise ValueError('Wrong predicate failed to change actual compiled data')
        observations=[]
        for codepoint in[point,ord('6')if which==2 else ord('B'),128]:
            if which==2:
                setup=[(0x02600000,struct.pack('<4H',37,codepoint,100,0)),(0x02600100,struct.pack('<I',0x02600200)),(0x02600200,bytes(64)),(0x02600300,bytes(64))];args=[0x02600000,0x02600100,0x02600300];entry=0x0201f2c0;callback=None
            else:setup=[(reader.SP,struct.pack('<III',0x02600100,0x02600104,0x02600108))];args=[36,3,reader.CALLBACK,0x02600000];entry=0x0201ed2c;callback=codepoint
            original=reader.execute(image,entry,args,setup,callback);wrong=reader.execute(bytes(mutated),entry,args,setup,callback);observations.append(dict(codepoint=codepoint,original=original,wrong=wrong,rejected=original['returned']!=wrong['returned']))
        if not observations[0]['rejected']or any(o['rejected']for o in observations[1:]):raise ValueError('Compiled wrong predicate is not independently distinguished from unaffected controls')
        results.append(dict(name=name,wrongData=proof,changedSourcePredicate=True,sourceCredit=0,observations=observations))
    return results


def main():
    admitted=inputs();common,generated,blocked=guarded_render()
    if(SOURCE/'ascii.h').read_text()!=common:raise ValueError('Semantic specification header changed')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();module_sha=hashlib.sha256(image).hexdigest()
    if module_sha!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':raise ValueError('Original physical main image changed')
    replaced=bytearray(image);rows=[];controls=[]
    for row,text,expected in generated:
        source=SOURCE/row['filename'];claim=next(c for c in admitted if c['address']==row['address'])
        if source.read_text()!=text or hashlib.sha256(expected).hexdigest()!=claim['targetSha256']:raise ValueError('Typed C or independent ASCII predicates changed from admitted geometry')
        payload,actual=build(source,row,WORK/'positive'/f'{int(row["address"],0):08x}',expected);start=int(row['address'],0)-0x02000000
        if payload!=image[start:start+row['bytes']]:raise ValueError('Fresh genuine native data differs from original table')
        actual.update(section=actual['section'],targetSection='.rodata',sourceSymbolType='STT_OBJECT',inputModuleSha256=module_sha,targetSha256=hashlib.sha256(payload).hexdigest(),outputSha256=hashlib.sha256(payload).hexdigest(),exactBytes=True,exactAfterDeclaredRelocation=True,exactAfterRealMwLink=True,sourceCredit=0,boundedOriginalStorageView=True,originalObjectDeclarationAlignmentClaimed=False)
        identity(actual,claim);replaced[start:start+row['bytes']]=payload;rows.append(actual);rejected=[]
        for key,value in [('program','child'),('processor','arm7'),('module','ov000'),('mode','arm'),('targetSection','.text'),('address',hex(int(row['address'],0)+1)),('bytes',row['bytes']+1),('elementBytes',8)]:
            wrong=dict(actual,**{key:value})
            try:identity(wrong,claim)
            except ValueError:rejected.append(key)
            else:raise ValueError('Wrong data namespace/extent/element width escaped identity gate')
        controls.append(dict(address=row['address'],rejected=rejected))
    if rows[1]['name']==rows[2]['name']or rows[1]['address']==rows[2]['address']or rows[1]['targetSha256']!=rows[2]['targetSha256']:raise ValueError('Duplicate class bytes lost distinct physical symbol/storage identity')
    if bytes(replaced)!=image:raise ValueError('Positive data replacement unexpectedly changes any original initialized byte')
    traces=pair_readers(image,bytes(replaced));negative=wrong_predicates(image);raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();trace=LANE/'traces.json.gz';trace.write_bytes(gzip.compress(raw,mtime=0))
    limits=['Only the three bounded128/256/256B storage views are proposed. Native labels do not disclose original enclosing object size or declaration alignment.','The776 original/compiled-data pairs execute complete signed numeric and wide-format native readers, with original runtime arithmetic and an explicit callback stream. Other known consumers retain the sealed native range audit; this is not whole-scene or all-format proof.','Code, functions, BSS, encoded assets, generated alignment padding and denominator credit are zero. The two byte-identical class maps remain distinct physical objects.','Shared data-aware admission, all20-module/container checks, accepted source closure and publication remain coordinator-owned. No registry/preferences/ledger or shared gate is changed.']
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm9',module='main',moduleSha256=module_sha,allPassed=True,functionMatched=0,functionMatches=[],dataMatches=rows,nativeSymbols={},dataAliases={r['nativeAlias']:r['address']for r in rows},initializedDataObjects=3,initializedDataBytes=640,typedConstantDataBytes=640,ordinaryFunctionCredit=0,executableSectionBytes=0,allocatedZeroFillBytes=0,encodedAssetBytes=0,measuredZeroAlignmentBytes=0,sourceCredit=0,generatedFromIndependentMathematics=True,generationGuard=dict(blockedOriginalReads=blocked,sourceUnitFormat='self-contained readable ASCII predicates and domain-index initializers'),actualOriginalAndCompiledDataReaderPairs=len(traces),actualReaderReturns=2*len(traces),nativeAccessWidths=[1,2,2],namespaceGeometryControls=controls,negativeControls=negative,generatedTrace=dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace),uncompressedSha256=hashlib.sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=limits)
    write_json(LANE/'qualification.json',report);write_json(ROOT/'evidence/matches/goal-resume20261107-ctype-ascii-data640.json',report)
    print(dict(dataObjects=3,initializedDataBytes=640,readerPairs=len(traces),readerReturns=2*len(traces),compiledWrongPredicateControls=len(negative),namespaceGeometryControls=sum(len(c['rejected'])for c in controls),sourceCredit=0),flush=True)


if __name__=='__main__':main()
