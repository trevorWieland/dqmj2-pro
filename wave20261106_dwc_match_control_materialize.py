import re
import ast
from project import ROOT,read_json

SOURCE=ROOT/'src/runtime/parallel_wave20261106/dwc-match-control-next'
LANE=ROOT/'evidence/lanes/parallel-wave20261106/dwc-match-control-next'
PRIMARY=ROOT/'deps/reference/nitrodwc-match-ba548986500a/libraries/base/src/dwc_match.c'
NAMES={0x0209dfd8:'DWCi_QR2Startup',0x0209e0fc:'DWCi_ConnectToAnybodyAsync',0x0209e258:'DWCi_ConnectToFriendsAsync',0x0209e408:'DWCi_SendStateChanged',0x0209ed44:'DWCi_GT2ConnectAttemptCallback',0x0209ef04:'DWCi_GT2ConnectedCallback'}


def function(a):
    name=NAMES[a];text=PRIMARY.read_text(encoding='utf-8');text=re.sub(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|(/\*[\s\S]*?\*/|//[^\n]*)',lambda m:m[1]or'',text);m=re.search(r'^(?:static\s+)?(?:void|qr2_error_t)\s+'+name+r'\s*\([^;]*?\)\s*\{',text,re.M);start=text.index('{',m.start());end=start+1;depth=1
    while depth:depth+=(text[end]=='{')-(text[end]=='}');end+=1
    return text[m.start():end].replace('static ','',1).replace(name,'native_main_%08x'%a,1)


def main():
    if SOURCE.resolve()!=(ROOT/'src/runtime/parallel_wave20261106/dwc-match-control-next').resolve()or LANE.resolve()!=(ROOT/'evidence/lanes/parallel-wave20261106/dwc-match-control-next').resolve():raise ValueError('Exact new Match-control source/evidence scope differs')
    base=ROOT/'src/runtime/parallel_wave20261106/dwc-match-continuation-next/first/020a2afc';context=(base/'context.h').read_text(encoding='utf-8').replace('extern DWCMatchOptMinCompleteIn*native_data_021d1b88;','extern MatchGlobalsView native_data_021d1b88;')
    context=context.replace('typedef void*qr2_buffer_t;','typedef struct qr2_buffer_s*qr2_buffer_t;').replace('typedef struct{u8 opaque[8];char*addFilter;}MatchGlobalsView;','typedef struct{DWCMatchOptMinCompleteIn*option;u32 opaque4;char*addFilter;}MatchGlobalsView;')
    context+='''
typedef int GT2Bool,SBCallbackReason;
typedef struct qr2_keybuffer_s*qr2_keybuffer_t;
typedef enum{key_server,key_player,key_team}qr2_key_type;
typedef struct{u8 index,aid;u16 reserve;void*param;}DWCConnectionInfo;
#define DWC_ALLOCTYPE_BASE 4
#define GT2False 0
#define GT2Success 0
#define GT2OutOfMemory 1
#define GT2DuplicateAddress 5
#define GT2TimedOut 6
#define QVERSION_QR2 1
#define e_qrnoerror 0
#define e_qrdnserror 3
extern void*DWC_Alloc(int,u32);
extern void DWC_Free(int,void*,u32);
extern void DWCi_QR2ServerKeyCallback(int,qr2_buffer_t,void*);
extern void DWCi_QR2PlayerKeyCallback(int,int,qr2_buffer_t,void*);
extern void DWCi_QR2TeamKeyCallback(int,int,qr2_buffer_t,void*);
extern void DWCi_QR2KeyListCallback(qr2_key_type,qr2_keybuffer_t,void*);
extern int DWCi_QR2CountCallback(qr2_key_type,void*);
extern void DWCi_QR2AddErrorCallback(qr2_error_t,gsi_char*,void*);
extern void DWCi_QR2PublicAddrCallback(unsigned int,unsigned short,void*);
extern void DWCi_QR2NatnegCallback(int,void*);
extern void DWCi_QR2ClientMsgCallback(gsi_char*,int,void*);
extern void DWCi_SBCallback(ServerBrowser,SBCallbackReason,SBServer,void*);
extern ServerBrowser ServerBrowserNew(const gsi_char*,const gsi_char*,const gsi_char*,int,int,int,BOOL,void(*)(ServerBrowser,SBCallbackReason,SBServer,void*),void*);
extern qr2_error_t qr2_init_socket(qr2_t*,SOCKET,u16,const gsi_char*,const gsi_char*,int,int,void(*)(int,qr2_buffer_t,void*),void(*)(int,int,qr2_buffer_t,void*),void(*)(int,int,qr2_buffer_t,void*),void(*)(qr2_key_type,qr2_keybuffer_t,void*),int(*)(qr2_key_type,void*),void(*)(qr2_error_t,gsi_char*,void*),void*);
extern void qr2_shutdown(qr2_t);
extern void qr2_register_publicaddress_callback(qr2_t,void(*)(unsigned int,unsigned short,void*));
extern void qr2_register_natneg_callback(qr2_t,void(*)(int,void*));
extern void qr2_register_clientmessage_callback(qr2_t,void(*)(gsi_char*,int,void*));
extern void qr2_send_statechanged(qr2_t);
extern void qr2_think(qr2_t);
extern SOCKET gt2GetSocketSOCKET(GT2Socket);
extern qr2_error_t DWCi_HandleQR2Error(qr2_error_t);
extern qr2_error_t DWCi_QR2Startup(int);
extern SBError DWCi_SBUpdateAsync(int);
extern void DWCi_SetMatchStatus(DWCMatchState);
extern int DWCi_SendResvCommandToFriend(BOOL,BOOL,int);
extern void gt2Reject(GT2Connection,const GT2Byte*,int);
extern GT2Bool gt2Accept(GT2Connection,GT2ConnectionCallbacks*);
extern int DWCi_GT2GetConnectionListIdx(void);
extern GT2Connection*DWCi_GetGT2ConnectionByIdx(int);
extern DWCConnectionInfo*DWCi_GetConnectionInfoByIdx(int);
extern void gt2SetConnectionData(GT2Connection,void*);
extern GT2Result gt2Connect(GT2Socket,GT2Connection*,const char*,const GT2Byte*,int,int,GT2ConnectionCallbacks*,GT2Bool);
extern void DWCi_StopResendingMatchCommand(void);
extern GT2Result DWCi_HandleGT2Error(GT2Result);
extern BOOL DWCi_CancelPreConnectedServerProcess(int);
extern void DWCi_PostProcessConnection(DWCMatchPpConnectionType);
#define DWC_STATUS_MATCH_ANYBODY 3
#define stpOptMinComp (native_data_021d1b88.option)
'''
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();claims={int(e['address'],0):e for e in read_json(LANE/'claim.json')['claimedFunctions']}
    for a in NAMES:
        directory=SOURCE/'first'/format(a,'08x')
        if directory.exists():raise ValueError('New materializer refuses existing source directory')
        body=function(a);ctx=context
        strings={}
        for record in claims[a]['originalRelocationRecords']:
            if'kind:load'not in record:continue
            target=int(record.split()[2][3:],0);raw=image[target-0x02000000:].split(b'\0',1)[0]
            if raw and len(raw)<100 and all(b in[9,10,13]or 32<=b<127 for b in raw):strings[raw.decode('ascii')]=target
        for literal in set(re.findall(r'"(?:\\.|[^"\\])*"',body)):
            value=ast.literal_eval(literal)
            if value in strings:body=body.replace(literal,'native_data_%08x'%strings[value])
        for value,target in strings.items():
            symbol='native_data_%08x'%target;ctx+='extern const char '+symbol+'[];\n'
            ctx=ctx.replace('"'+value+'"',symbol)
        directory.mkdir(parents=True);(directory/'match.c').write_text('#include "context.h"\n'+body+'\n',encoding='utf-8');(directory/'context.h').write_text(ctx,encoding='utf-8')
        for name in['types.h','errors.h','string.h']:(directory/name).write_bytes((base/name).read_bytes())


if __name__=='__main__':main()
