#include "string.h"
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef unsigned long long u64;typedef u64 OSTick;typedef int BOOL;typedef int DWCError;typedef int DWCLoginState;typedef int GPResult;typedef void*GPConnection;typedef void(*DWCLoginCallback)(DWCError,int,void*);typedef void(*GPCallback)(GPConnection*,void*,void*);typedef void(*DWCRemoteAuthCallback)(const char*,const char*,void*);
typedef struct{u32 id_data,userid_lo32,playerid;}DWCAccLoginId;typedef struct{int size;DWCAccLoginId pseudo,authentic;int gs_profile_id,flag;u32 gamecode;int reserved[5];u32 crc32;}DWCAccUserData;typedef DWCAccUserData DWCUserData;
typedef struct{GPResult result;int profile;char uniquenick[21];}GPConnectResponseArg;
typedef struct{GPConnection*pGpObj;DWCLoginState state;int productID;u32 gamecode;const u16*playerName;DWCLoginCallback callback;void*param;DWCUserData*userdata;void*bmwork,*http;OSTick startTick;u32 connectFlag;OSTick connectTick;DWCAccLoginId tempLoginId;char authToken[256],partnerChallenge[256],username[21];GPConnectResponseArg gpconnectresponsearg;}DWCLoginControl;
typedef struct{DWCRemoteAuthCallback remoteCallback;DWCLoginControl*control;void*remoteParam;}DWCLoginGlobals;extern DWCLoginGlobals native_data_021d1b68;
#define stpLoginCnt native_data_021d1b68.control
#define stRemoteAuthCallback native_data_021d1b68.remoteCallback
#define pStRemoteAuthParam native_data_021d1b68.remoteParam
#define NULL ((void*)0)
#define SDK_ASSERT(x) ((void)0)
#define DWC_Printf(...) ((void)0)
#define TRUE 1
#define FALSE 0
#define DWC_LOGIN_STATE_INIT 0
#define DWC_LOGIN_STATE_REMOTE_AUTH 1
#define DWC_LOGIN_STATE_CONNECTING 2
#define DWC_LOGIN_STATE_GPGETINFO 3
#define DWC_LOGIN_STATE_GPSETINFO 4
#define DWC_LOGIN_STATE_CONNECTED 5
#define DWC_LOGIN_GPCONNECT_TIMEOUT 60000
#define DWC_ERROR_NONE 0
#define DWC_ERROR_NETWORK 6
#define DWC_ERROR_FATAL 9
#define DWC_ECODE_SEQ_LOGIN (-60000)
#define DWC_ECODE_GS_GP (-1000)
#define DWC_ECODE_TYPE_ALLOC (-1)
#define DWC_ECODE_TYPE_PARAM (-2)
#define DWC_ECODE_TYPE_NETWORK (-10)
#define DWC_ECODE_TYPE_SERVER (-20)
#define DWC_ECODE_TYPE_TIMEOUT (-70)
#define GP_NO_ERROR 0
#define GP_MEMORY_ERROR 1
#define GP_PARAMETER_ERROR 2
#define GP_NETWORK_ERROR 3
#define GP_SERVER_ERROR 4
#define DWC_STATUS_ONLINE 1
#define GP_DONT_CHECK_CACHE 0
#define GP_NON_BLOCKING 0
#define GP_FIREWALL 1
#define OS_TicksToMilliSeconds(t) (((u64)(t)*64)/33514)
void native_fn_02008d78(void*,int,u32);void native_fn_0209c81c(DWCRemoteAuthCallback,void*),native_fn_0209c7a1(const char*,const char*,void*);BOOL native_fn_0209a9e4(void);void native_fn_0209c940(void);GPResult native_fn_020a9f60(GPConnection*);OSTick native_fn_02007a9c(void);void native_fn_0209c610(DWCError,int),native_fn_0209a9f8(DWCError,int),native_fn_0209c678(void);GPResult native_fn_020a9fc0(GPConnection*,const char*,const char*,int,int,GPCallback,void*),native_fn_0209c690(GPResult);GPResult native_fn_0209d1c8(int,const char*,const char*);int native_fn_0209bc9c(void),native_fn_0209dfd8(int);GPResult native_fn_020aa100(GPConnection*,int,int,int,GPCallback,void*);void native_fn_0209caa1(GPConnection*,void*,void*);
#define MI_CpuClear8(d,n) native_fn_02008d78(d,0,n)
#define DWCi_RemoteLogin native_fn_0209c81c
#define DWCi_RemoteAuthCallback native_fn_0209c7a1
#define DWCi_IsError native_fn_0209a9e4
#define DWCi_RemoteLoginProcess native_fn_0209c940
#define gpProcess native_fn_020a9f60
#define OS_GetTick native_fn_02007a9c
#define DWCi_StopLogin native_fn_0209c610
#define DWCi_SetError native_fn_0209a9f8
#define DWCi_CloseLogin native_fn_0209c678
#define gpConnectPreAuthenticated native_fn_020a9fc0
#define DWCi_HandleGPError native_fn_0209c690
#define DWCi_SetGPStatus native_fn_0209d1c8
#define DWCi_GT2Startup native_fn_0209bc9c
#define DWCi_QR2Startup native_fn_0209dfd8
#define gpGetInfo native_fn_020aa100
#define DWCi_GPGetInfoCallback native_fn_0209caa1
extern const char native_data_020e017c[];
