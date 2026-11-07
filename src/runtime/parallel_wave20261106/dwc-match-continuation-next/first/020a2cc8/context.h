#include "types.h"
extern DWCGameMatchKeyData stGameMatchKeys[DWC_QR2_GAME_RESERVED_KEYS];
typedef struct{u8 opaque[8];char*addFilter;}MatchGlobalsView;
#define stpAddFilter (native_data_021d1b88.addFilter)
extern DWCMatchControl*native_fn_020a3d70(void);
extern int DWCi_GetDefaultMatchFilter(char*,int,u8,u8);
extern int OS_SNPrintf(char*,u32,const char*,...);
extern void ServerBrowserClear(ServerBrowser);
extern SBError ServerBrowserLimitUpdate(ServerBrowser,BOOL,BOOL,const u8*,int,const char*,int);
extern OSTick native_fn_02007a9c(void);
extern void MI_CpuCopy32(const void*,void*,u32);
#define ne_noerror 0
#define ne_socketerror 2
#define nr_success 0
extern BOOL SBServerHasPrivateAddress(SBServer);
extern u32 SBServerGetPublicInetAddress(SBServer),ServerBrowserGetMyPublicIPAddr(ServerBrowser),SBServerGetPrivateInetAddress(SBServer),SO_GetHostID(void);
extern u16 SBServerGetPrivateQueryPort(SBServer),SBServerGetPublicQueryPort(SBServer),gt2GetLocalPort(GT2Socket);
extern u32 DWCi_GetMathRand32(u32);
extern int native_fn_020a00ac(u8,int,u32,u16,const u32*,int);
extern NegotiateError DWCi_DoNatNegotiationAsync(DWCNNInfo*);
extern SOCKET native_fn_020b45a0(GT2Socket);
extern void native_fn_020a3a4c(NegotiateResult,SOCKET,struct sockaddr_in*,void*);
extern SBServer native_fn_020a699c(ServerBrowser,int);
extern int SBServerGetIntValue(SBServer,const char*,int);
#define DWC_MATCH_COMMAND_ADD_MESSAGE_MAX 512
#define SDK_ASSERTMSG(...)
typedef char gsi_char;
typedef struct{char identifier[4];u32 version;u8 command,size;u16 qr2Port;u32 qr2IP;int profileID;}DWCSBMessageHeader;
typedef struct{DWCSBMessageHeader header;u32 data[32];}DWCSBMessage;
#include "string.h"
extern char*gt2AddressToString(u32,u16,char*);
extern SBError ServerBrowserSendMessageToServer(ServerBrowser,const char*,u16,const char*,int);
extern SBError DWCi_SendSBMsgCommand(u8,u32,u16,const u32*,int);
extern GPResult DWCi_SendGPBuddyMsgCommand(GPConnection*,u8,int,const char*);
extern void MI_CpuCopy8(const void*,void*,u32);
extern void native_fn_020b748c(qr2_t);
typedef enum {
    DWC_MATCH_RESET_ALL = 0,
    DWC_MATCH_RESET_RESTART,
    DWC_MATCH_RESET_CONTINUE,
    DWC_MATCH_RESET_NUM
} DWCMatchResetLevel;
extern BOOL native_fn_020a1edc (const u32 pidList[], u32 pidListLen);
extern int native_fn_020a2150 (void);
extern void native_fn_020a21e0 (DWCMatchResetLevel level);
extern void native_fn_020a2290 (void);
extern int native_fn_020a22b4 (void);
extern BOOL DWCi_CloseCancelHostAsync (int profileID);
extern BOOL DWCi_CloseShutdownClientSC (u32 bitmap);
extern BOOL DWCi_SendCancelMatchSynCommand (int profileID, u8 command);
extern BOOL native_fn_020a2b44 (int profileID);
extern void DWCi_FinishCancelMatching (void);
extern void DWCi_ResetMatchParam (DWCMatchResetLevel level);
extern SBError native_fn_020a304c (SBError error);
extern SBError native_fn_0209fc38 (int profileID);
extern int native_fn_020a13d8 (BOOL delay, BOOL init, int resendPid);
extern void native_fn_020a2394 (void);
extern void native_fn_020a3d7c (DWCMatchState state);
extern int DWCi_SendResvCommand (int profileID, BOOL delay);
extern int native_fn_020a1258 (int error);
extern BOOL DWCi_DeleteHostByProfileID (int profileID, int numHost);
extern u8 native_fn_020a2c38 (int profileID, BOOL idx0);
extern int native_fn_0209d168(int);
extern GT2Connection*DWCi_GetGT2ConnectionByProfileID(int,int);
extern void gt2CloseConnectionHard(GT2Connection);
extern int native_fn_0209bba0(u8);
enum {
    DWC_MATCH_CLOSE_STATE_INIT = 0,
    DWC_MATCH_CLOSE_STATE_CHANGE_TO_CLIENT,
    DWC_MATCH_CLOSE_STATE_TIMEOUT,
    DWC_MATCH_CLOSE_STATE_FORCED,
    DWC_MATCH_CLOSE_STATE_NUM
};
enum {
    DWC_MATCH_CANCEL_STATE_INIT = 0,
    DWC_MATCH_CANCEL_STATE_EXEC,
    DWC_MATCH_CANCEL_STATE_NUM
};
#define DWC_STATUS_ONLINE 1
extern GPResult DWCi_HandleGPError (GPResult result);
extern void DWCi_CloseMatching (void);
extern GPResult DWCi_SetGPStatus(int,const char*,const char*);
extern void native_fn_020b4540(GT2Socket);
extern void native_fn_020b6c90(int);
#define DWC_MATCH_COMMAND_ADD_MESSAGE_NUM 128
#define GP_NO_ERROR 0
#define DWC_STATUS_MATCH_SC_SV 6
#define DWC_GP_SSTR_KEY_MATCH_VERSION       "VER"
#define DWC_GP_SSTR_KEY_MATCH_SC_MAX        "SCM"
#define DWC_GP_SSTR_KEY_MATCH_SC_NUM        "SCN"
extern void DWCi_MatchGPRecvBuddyMsgCallback (GPConnection * pconnection, int profileID, char * message);
extern void native_fn_0209f130 (DWCError error, int errorCode);
extern void DWCi_ProcessMatchSCClosing (int clientPid);
extern BOOL DWCi_DeleteHostByProfileID (int profileID, int numHost);
extern int DWCi_DeleteHostByIndex (int index, int numHost);
extern int DWCi_GetAllAIDList (u8 ** aidList);
extern int DWCi_GetValidAIDList (u8 ** aidList);
extern GPResult DWCi_GPSetServerStatus (void);
extern BOOL native_fn_020a16e4 (int clientPid);
extern void DWCi_SetNumValidConnection (void);
extern int DWCi_GetGPBuddyAdditionalMsg (char * dstMsg, const char * srcMsg, int index);
extern BOOL DWCi_ProcessRecvMatchCommand (u8 command,
                                          int srcPid,
                                          u32 srcIP,
                                          u16 srcPort,
                                          const u32 data[],
                                          int len);
extern void DWCi_SetError(DWCError,int);
extern int DWC_SetCommonKeyValueString(const char*,const char*,char*,char);
extern int DWC_AddCommonKeyValueString(const char*,const char*,char*,char);
extern unsigned long strtoul(const char*,char**,int);
extern const char DWCUnsignedFormat[];
extern void MI_CpuFill8(void*,u8,u32);
static inline void MI_CpuClear8(void*dest,u32 size){MI_CpuFill8(dest,0,size);}
enum {
    DWC_SEND_TYPE_INVALID,
    DWC_SEND_TYPE_USERDATA,
    DWC_SEND_TYPE_MATCH_SYN,
    DWC_SEND_TYPE_MATCH_SYN_ACK,
    DWC_SEND_TYPE_MATCH_ACK,
    DWC_SEND_TYPE_MAX
};
typedef enum {
    DWC_PP_CONNECTION_SV_CONNECT = 0,
    DWC_PP_CONNECTION_CL_GT2_CONNECT,
    DWC_PP_CONNECTION_CL_GT2_ACCEPT,
    DWC_PP_CONNECTION_CL_FINISH_CONNECT,
    DWC_PP_CONNECTION_SYN_FINISH,
    DWC_PP_CONNECTION_NUM
} DWCMatchPpConnectionType;
typedef enum {
    DWC_STATE_INIT = 0,
    DWC_STATE_AVAILABLE_CHECK,
    DWC_STATE_LOGIN,
    DWC_STATE_ONLINE,
    DWC_STATE_UPDATE_SERVERS,
    DWC_STATE_MATCHING,
    DWC_STATE_CONNECTED,
    DWC_STATE_NUM
} DWCState;
extern DWCState native_fn_0209bc88(void);
#define DWC_ECODE_SEQ_MATCH (-80000)
#define DWC_ECODE_TYPE_SC_CL_FAIL (-430)
extern BOOL DWCi_SendReliable(u16,u8,const void*,int);
extern void DWCi_ProcessMatchSynPacket (u8 aid, u16 type, u8 * data);
extern BOOL DWCi_ProcessMatchClosing (DWCError error, int errorCode, int profileID);
extern void DWCi_SendMatchSynPacket (u8 aid, u16 type);
extern u32 DWCi_GetAIDBitmask (BOOL valid);
extern void native_fn_020a19b4 (DWCMatchPpConnectionType type);
extern int native_fn_020a22b4 (void);
#define OS_SYSTEM_CLOCK 33514000
#define OS_TicksToMilliSeconds(tick) (((u64)(tick)*64)/(OS_SYSTEM_CLOCK/1000))
extern DWCMatchOptMinCompleteIn*native_data_021d1b88;
extern DWCMatchOptSCBlock stOptSCBlock;
#define DWC_ECODE_TYPE_OTHER (-410)
extern int native_fn_020a10d0 (int profileID, u32 ip, u16 port);
extern BOOL native_fn_020a1608 (int resendPid);
extern BOOL DWCi_ProcessMatchSynTimeout (void);
extern BOOL native_fn_020a277c (int profileID, u8 command, u32 data);
extern void native_fn_020a19b4 (DWCMatchPpConnectionType type);
extern u8 DWCi_GetAIDFromList (void);
extern void DWCi_InitOptMinCompParam (BOOL reset);
extern BOOL native_fn_020a1878 (int serverPid);
extern void native_fn_020a21e0 (DWCMatchResetLevel level);
extern BOOL DWCi_CloseShutdownClientSC (u32 bitmap);
extern BOOL native_fn_020a16e4 (int clientPid);
extern BOOL DWCi_SendCancelMatchSynCommand (int profileID, u8 command);
extern void DWCi_SetMatchCommonParam (u8 matchType,
                                      u8 numEntry,
                                      DWCMatchedSCCallback callback,
                                      void * param);
extern void DWCi_ClearQR2Key (void);
extern void native_fn_020a2cc8 (void);
extern GPResult DWCi_GPSetServerStatus (void);
extern NegotiateError native_fn_0209fde8 (int isQR2, int cookie, SBServer server);
extern int native_fn_020a1908 (void);
#define DWC_GP_PROCESS_INTERVAL 300
#define DWC_STATUS_PLAYING 2
typedef struct{int profile,status;char statusString[256],locationString[256];unsigned int ip;int port,quietModeFlags;}GPBuddyStatus;
typedef struct DWCstUserData DWCUserData;
extern DWCUserData*DWCi_GetUserData(void);
extern int DWC_GetGsProfileId(const DWCUserData*,const DWCFriendData*);
extern BOOL DWCi_Acc_IsValidFriendData(const DWCFriendData*);
extern GPResult gpGetBuddyIndex(GPConnection*,int,int*);
extern GPResult gpGetBuddyStatus(GPConnection*,int,GPBuddyStatus*);
extern int DWC_GetCommonValueString(const char*,char*,const char*,char);
#define DWC_STATUS_MATCH_FRIEND 4
#define DWC_GP_SSTR_KEY_MATCH_FRIEND_NUM    "FME"
#define DWC_GP_SSTR_KEY_DISTANT_FRIEND      "MDF"
extern int gpIsBuddy(GPConnection*,int);
extern u8 native_fn_020a0e88 (int profileID, u32 qr2IP, u16 qr2Port, u32 matchType, BOOL priorFlag);
extern int native_fn_020a10d0 (int profileID, u32 ip, u16 port);
extern BOOL DWCi_ProcessRecvMatchCommand (u8 command,
                                          int srcPid,
                                          u32 srcIP,
                                          u16 srcPort,
                                          const u32 data[],
                                          int len);
struct sockaddr_in{u8 sin_len,sin_family;u16 sin_port;struct{u32 s_addr;}sin_addr;};
#define DWC_MATCH_RESV_DENY_REASON_SV_FULL 0x10
#define DWC_MATCH_COMMAND_FRIEND_ACCEPT 0x20
#define SO_HtoNs(n) ((unsigned char)((n)>>8)|(((n)<<8)&0xff00))
extern int native_fn_020a16a8 (int profileID);
extern NegotiateError native_fn_020a3154 (NegotiateError error);
extern void native_fn_020a121c (int profileID, const u32 data[]);
extern void ServerBrowserFree(ServerBrowser);
BOOL native_main_020a039c (u8 command,
                                          int srcPid,
                                          u32 srcIP,
                                          u16 srcPort,
                                          const u32 data[],
                                          int len)
;

#include "errors.h"
#define DWCi_GetMatchCnt native_fn_020a3d70
#define DWCi_StopMatching native_fn_0209f130
#define DWC_GetState native_fn_0209bc88
extern void DWCi_StopLogin(DWCError,int);
extern void DWCi_StopFriendProcess(DWCError,int);
extern int DWCi_GetProfileIDFromList(int);
extern int ServerBrowserCount(ServerBrowser);
extern void ServerBrowserRemoveServer(ServerBrowser,SBServer);
extern SBServer ServerBrowserGetServer(ServerBrowser,int);
extern void ServerBrowserSort(ServerBrowser,int,const char*,int);
extern void SBServerAddIntKeyValue(SBServer,const char*,int);
#define sbcm_int 0
#define GP_MEMORY_ERROR 1
#define GP_PARAMETER_ERROR 2
#define GP_NETWORK_ERROR 3
#define GP_SERVER_ERROR 4
#define sbe_socketerror 1
#define sbe_connecterror 3
#define sbe_dataerror 4
#define sbe_allocerror 5
#define sbe_paramerror 6
typedef int qr2_error_t;
#define e_qrnoerror 0
#define e_qrwsockerror 1
#define e_qrbinderror 2
#define e_qrdnserror 3
#define e_qrconnerror 4
#define e_qrnochallengeerror 5
typedef void*qr2_buffer_t;
extern void qr2_buffer_add_int(qr2_buffer_t,int);
extern void qr2_buffer_add(qr2_buffer_t,const char*);



#define OS_GetTick native_fn_02007a9c
void native_main_020a2cc8 (void);
