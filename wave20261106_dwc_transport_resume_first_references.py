import re
from project import ROOT,read_json,sha256

LANE='evidence/lanes/parallel-wave20261106/dwc-transport-resume-next/first'
PRIMARY='deps/reference/nitrodwc-transport-ba548986500a6628ec37c0603bdb94245ff12a63/libraries/base/src/dwc_transport.c'
HEADER='deps/reference/nitrodwc-transport-ba548986500a6628ec37c0603bdb94245ff12a63/include/base/dwc_transport.h'
SOURCES={0x020a3f84:'DWCi_SendReliable',0x020a40a4:'DWC_SetUserSendCallback',0x020a40c0:'DWC_SetUserRecvCallback',0x020a40dc:'DWC_SetUserRecvTimeoutCallback',0x020a4114:'DWCs_DecodeHeader',0x020a4144:'DWCs_GetRequiredHeaderSize',0x020a4158:'DWC_SetRecvTimeoutTime',0x020a41dc:'DWCi_PingCallback',0x020a431c:'DWCi_ClearTransConnection',0x020a4404:'DWCs_HandleReliableMessage',0x020a449c:'DWCs_HandleUnreliableMessage',0x020a44f4:'DWCs_RecvDataHeader',0x020a456c:'DWCs_RecvDataBody',0x020a45fc:'DWCs_RecvSystemDataBody'}


def clean(text):return re.sub(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|(/\*[\s\S]*?\*/|//[^\n]*)',lambda m:m[1]or'',text)


def tokens(text):return re.findall(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[A-Za-z_][A-Za-z_0-9]*|0x[0-9a-fA-F]+|[0-9]+[uU]?|[^\s]',text)


def function(a):
    name=SOURCES[a];text=clean((ROOT/PRIMARY).read_text(encoding='utf-8'));m=re.search(r'^(?:static\s+)?(?:BOOL|void|s32|u16)\s+'+name+r'\s*\([^;]*?\)\s*\{',text,re.M)
    if m is None:raise ValueError('Complete primary transport body missing:'+name)
    start=text.index('{',m.start());end=start+1;depth=1
    while depth:depth+=(text[end]=='{')-(text[end]=='}');end+=1
    body=text[m.start():end].replace('static ','',1).replace(name,'native_main_%08x'%a,1);body=re.sub(r'\bDWC_MAGIC_STRINGS\b','native_data_020e02d0',body)
    if a==0x020a431c:
        body='void native_main_020a431c(u8 aid){if(!sTransInfo)return;'+''.join('sTransInfo->connections[aid].'+field+' = '+value+';'for field,value in [('sendingSize','0'),('recvingSize','0'),('requestSendSize','0'),('requestRecvSize','0'),('sendState','0'),('recvBuffer','NULL'),('recvBufferSize','0'),('recvState','DWC_TRANSPORT_RECV_NOBUF'),('lastRecvType','0')])+'}'
    return body


def qualify():
    evidence=read_json(ROOT/(LANE+'/derivation.json'));image=(ROOT/'extract/arm9/arm9.bin').read_bytes()
    for pin in evidence['primaryPins']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Pinned complete transport/header/error lineage changed')
    if sha256(ROOT/'extract/arm9/arm9.bin')!=evidence['imageSha256']:raise ValueError('Full measured original main image differs')
    error=(ROOT/'deps/reference/nitrodwc-match-ba548986500a/include/base/dwc_error.h').read_text(encoding='utf-8');values=re.findall(r'^\s*(DWC_ECODE_\w+)\s*=\s*(\([^\n,]+\))',error,re.M);expected='\n'.join('#define '+n+' '+v for n,v in values)+'\n'
    for a in SOURCES:
        directory=ROOT/('src/runtime/parallel_wave20261106/dwc-transport-resume-next/first/%08x'%a);source=(directory/'match.c').read_text(encoding='utf-8').removeprefix('#include "context.h"\n')
        if tokens(source)!=tokens(function(a)):raise ValueError('Complete primary-derived/native-corrected transport body differs:'+hex(a))
        if tokens((directory/'transport.h').read_text(encoding='utf-8'))!=tokens(clean((ROOT/HEADER).read_text(encoding='utf-8')).replace('#include <darray.h>','')):raise ValueError('Actual complete transport header tokens differ')
        if(directory/'errors.h').read_text(encoding='utf-8')!=expected:raise ValueError('Actual complete primary error enum constants differ')
    for fact in evidence['nativeFacts']:
        a=int(fact['address'],0)-0x02000000
        if image[a:a+fact['bytes']].hex()!=fact['nativeHex']:raise ValueError('Actual complete native body/context fact differs')
    return dict(origin='Complete pinned same-commit DWC Transport C/H; measured SDK_FINALROM32-by48-byte DS context and explicit clear72 native revision',fullPrimarySourceTokensVerified=True,sourceGenerationAndCHeaderDependenciesSeparate=True,originalProviderAndStorageCredit=0,pins=evidence['primaryPins'],sourceCorrespondenceCorrections=evidence['sourceCorrespondenceCorrections'])
