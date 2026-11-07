import re
import ast
from project import ROOT,read_json,sha256

LANE='evidence/lanes/parallel-wave20261106/dwc-match-continuation-next/first'
PRIMARY='deps/reference/nitrodwc-match-ba548986500a/libraries/base/src/dwc_match.c'
SOURCES={0x020a2afc:'DWCi_GetAIDFromList',0x020a2b44:'DWCi_IsFriendByIdxList',0x020a2b98:'DWCi_CheckDWCServer',0x020a2c38:'DWCi_GetAIDFromProfileID',0x020a2c80:'DWCi_GetAIDBitmask',0x020a2cc8:'DWCi_InitClWaitTimeout',0x020a2ff8:'DWCi_HandleGPError',0x020a304c:'DWCi_HandleSBError',0x020a30b4:'DWCi_HandleQR2Error',0x020a3528:'DWCi_EvaluateServers',0x020a3694:'DWCi_RandomizeServers',0x020a37ac:'DWCi_QR2ServerKeyCallback'}


def tokens(text):return re.findall(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[A-Za-z_][A-Za-z_0-9]*|0x[0-9a-fA-F]+|[0-9]+[uU]?|[^\s]',text)


def function(a):
    name=SOURCES[a];text=(ROOT/PRIMARY).read_text(encoding='utf-8');clean=re.sub(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|(/\*[\s\S]*?\*/|//[^\n]*)',lambda m:m[1]or'',text);m=re.search(r'^(?:static\s+)?(?:BOOL|void|int|u8|u32|GPResult|SBError|qr2_error_t)\s+'+name+r'\s*\([^;]*?\)\s*\{',clean,re.M)
    if m is None:raise ValueError('Complete primary Match function missing')
    start=clean.index('{',m.start());end=start+1;depth=1
    while depth:depth+=(clean[end]=='{')-(clean[end]=='}');end+=1
    body=clean[m.start():end].replace('static ','',1).replace(name,'native_main_%08x'%a,1);entry=next(e for e in read_json(ROOT/(LANE+'/native-inputs.json'))['entries']if int(e['address'],0)==a);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();strings={}
    for record in entry['originalRelocationRecords']:
        if'kind:load'not in record:continue
        target=int(record.split()[2][3:],0);raw=image[target-0x02000000:].split(b'\0',1)[0]
        if raw and len(raw)<100 and all(b in[9,10,13]or 32<=b<127 for b in raw):strings[raw.decode('ascii')]=target
    for literal in set(re.findall(r'"(?:\\.|[^"\\])*"',body)):
        value=ast.literal_eval(literal)
        if value in strings:body=body.replace(literal,'native_data_%08x'%strings[value])
    for key,value in{'DWC_QR2_PID_KEY_STR':'dwc_pid','DWC_QR2_MATCH_TYPE_KEY_STR':'dwc_mtype','DWC_QR2_MATCH_RESV_KEY_STR':'dwc_mresv','DWC_QR2_MATCH_VER_KEY_STR':'dwc_mver','DWC_QR2_MATCH_EVAL_KEY_STR':'dwc_eval'}.items():
        if value in strings:body=body.replace(key,'native_data_%08x'%strings[value])
    if a==0x020a2c80:body=body.replace('bitmask |= 1 <<','bitmask |= 1U <<')
    return body


def qualify():
    evidence=read_json(ROOT/(LANE+'/derivation.json'))
    for pin in evidence['primaryPins']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Pinned complete Match/SDK/type lineage changed')
    for a in SOURCES:
        path=ROOT/('src/runtime/parallel_wave20261106/dwc-match-continuation-next/first/%08x/match.c'%a);source=path.read_text(encoding='utf-8').removeprefix('#include "context.h"\n')
        if tokens(source)!=tokens(function(a)):raise ValueError('Complete primary-derived Match function tokens differ:'+hex(a))
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes()
    if sha256(ROOT/'extract/arm9/arm9.bin')!=evidence['imageSha256']:raise ValueError('Full measured original main image differs')
    for fact in evidence['nativeFacts']:
        a=int(fact['address'],0)-0x02000000
        if image[a:a+fact['bytes']].hex()!=fact['nativeHex']:raise ValueError('Actual full native context/body fact differs')
    error=(ROOT/'deps/reference/nitrodwc-match-ba548986500a/include/base/dwc_error.h').read_text(encoding='utf-8');values=re.findall(r'^\s*(DWC_ECODE_\w+)\s*=\s*(\([^\n,]+\))',error,re.M);expected='\n'.join('#define '+n+' '+v for n,v in values)+'\n'
    for a in SOURCES:
        if(ROOT/('src/runtime/parallel_wave20261106/dwc-match-continuation-next/first/%08x/errors.h'%a)).read_text(encoding='utf-8')!=expected:raise ValueError('Actual complete primary error enum constants differ')
    return dict(origin='Complete pinned DWC Match C,measured record/enum/NOFILE contexts and preserved original ABI',fullPrimarySourceTokensVerified=True,sourceGenerationAndCHeaderDependenciesSeparate=True,originalProviderAndStorageCredit=0,pins=evidence['primaryPins'],unsignedAIDShiftPreservesDefined32BitOperationAndNativeBytes=True,correctedSourceCorrespondence=evidence['sourceCorrespondenceCorrections'])
