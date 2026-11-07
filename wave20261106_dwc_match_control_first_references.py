import re
import ast
from project import ROOT,read_json,sha256
from wave20261106_dwc_match_control_materialize import function,NAMES

LANE='evidence/lanes/parallel-wave20261106/dwc-match-control-next/first'


def tokens(text):return re.findall(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[A-Za-z_][A-Za-z_0-9]*|0x[0-9a-fA-F]+|[0-9]+[uU]?|[^\s]',text)


def expected(a):
    body=function(a);entry=next(e for e in read_json(ROOT/(LANE+'/native-inputs.json'))['entries']if int(e['address'],0)==a);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();strings={}
    for record in entry['originalRelocationRecords']:
        if'kind:load'not in record:continue
        target=int(record.split()[2][3:],0);offset=target-0x02000000
        if not 0<=offset<len(image)or target&1:continue
        raw=image[offset:].split(b'\0',1)[0]
        if len(raw)<100 and all(b in[9,10,13]or 32<=b<127 for b in raw):strings[raw.decode('ascii')]=target
    for literal in set(re.findall(r'"(?:\\.|[^"\\])*"',body)):
        value=ast.literal_eval(literal)
        if value in strings:body=body.replace(literal,'native_data_%08x'%strings[value])
    return body


def qualify():
    evidence=read_json(ROOT/(LANE+'/derivation.json'));image=(ROOT/'extract/arm9/arm9.bin').read_bytes();imports=read_json(ROOT/(LANE+'/original-imports.json'))
    for pin in evidence['primaryPins']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Complete primary Match/GT2/QR2/header lineage changed')
    if sha256(ROOT/'extract/arm9/arm9.bin')!=evidence['imageSha256']:raise ValueError('Full measured original main image differs')
    error=(ROOT/'deps/reference/nitrodwc-match-ba548986500a/include/base/dwc_error.h').read_text(encoding='utf-8');values=re.findall(r'^\s*(DWC_ECODE_\w+)\s*=\s*(\([^\n,]+\))',error,re.M);errors='\n'.join('#define '+n+' '+v for n,v in values)+'\n'
    for a in NAMES:
        directory=ROOT/('src/runtime/parallel_wave20261106/dwc-match-control-next/first/%08x'%a);body=(directory/'match.c').read_text(encoding='utf-8').removeprefix('#include "context.h"\n');context=(directory/'context.h').read_text(encoding='utf-8')
        if tokens(body)!=tokens(expected(a)):raise ValueError('Complete primary-derived Match-control function tokens differ:'+hex(a))
        if(directory/'errors.h').read_text(encoding='utf-8')!=errors:raise ValueError('Actual complete primary error enum constants differ')
        for address,name in imports['actualCallbacks'].items():
            alias='native_fn_%08x'%(int(address,0)&~1)
            if'#define '+name+' '+alias+'\n'not in context or imports['mapping'][alias]['address']!=hex(int(address,0)&~1):raise ValueError('Actual canonical native callback identity declaration differs')
        if 'typedef struct{DWCMatchOptMinCompleteIn*option;u32 opaque4;char*addFilter;}MatchGlobalsView;'not in context or '#define stpOptMinComp (native_data_021d1b88.option)'not in context or '#define stpAddFilter (native_data_021d1b88.addFilter)'not in context:raise ValueError('Actual shared-object pointer views differ')
    for fact in evidence['nativeFacts']:
        a=int(fact['address'],0)-0x02000000
        if image[a:a+fact['bytes']].hex()!=fact['nativeHex']:raise ValueError('Actual complete native body/context fact differs')
    return dict(origin='Complete pinned same-commit Match C/H with actually measured DS MatchControl,QR2+180 word and connection records',fullPrimarySourceTokensVerified=True,sourceGenerationAndCHeaderDependenciesSeparate=True,originalProviderAndStorageCredit=0,pins=evidence['primaryPins'],primaryAlgorithmsUnmodified=True,nativeCallbackNamesOnlyBindGenuineCanonicalEntries=True,sharedObjectViews=evidence['sharedObjectViews'],publicProvidersNotExecuted=True)
