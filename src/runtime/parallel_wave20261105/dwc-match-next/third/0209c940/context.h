#include "string.h"
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef unsigned long long u64;typedef u64 OSTick;typedef int BOOL;typedef int DWCError;typedef int DWCLoginState;typedef int GPResult;typedef void*GPConnection;typedef void(*DWCLoginCallback)(DWCError,int,void*);typedef void(*GPCallback)(GPConnection*,void*,void*);typedef void(*DWCRemoteAuthCallback)(const char*,const char*,void*);
typedef struct{u32 id_data,userid_lo32,playerid;}DWCAccLoginId;typedef struct{int size;DWCAccLoginId pseudo,authentic;int gs_profile_id,flag;u32 gamecode;int reserved[5];u32 crc32;}DWCAccUserData;typedef DWCAccUserData DWCUserData;
typedef struct{GPResult result;int profile;char uniquenick[21];}GPConnectResponseArg;
typedef struct{GPConnection*pGpObj;DWCLoginState state;int productID;u32 gamecode;const u16*playerName;DWCLoginCallback callback;void*param;DWCUserData*userdata;void*bmwork,*http;OSTick startTick;u32 connectFlag;OSTick connectTick;DWCAccLoginId tempLoginId;char authToken[256],partnerChallenge[256],username[21];GPConnectResponseArg gpconnectresponsearg;}DWCLoginControl;
typedef struct{void*remoteParam;DWCLoginControl*control;DWCRemoteAuthCallback remoteCallback;}DWCLoginGlobals;extern DWCLoginGlobals native_data_021d1b68;
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

typedef void*(*DWCAuthAlloc)(unsigned long,long);typedef void(*DWCAuthFree)(unsigned long,void*,long);typedef struct{u16 ingamesn[26];char gsbrcd[12];DWCAuthAlloc alloc;DWCAuthFree free;}DWCAuthParam;typedef struct{u32 opaque[1797];}DWCHttp;typedef struct{int returncode;char retcode[4],datetime[15],locator[51],token[301],challenge[9],cookie[65];}DWCAuthResult;
#define SDK_ASSERTMSG(...) ((void)0)
#define DWC_ACC_USERNAME_GSBRCD_OFFSET 9
#define DWC_ALLOCTYPE_AUTH 0
#define DWC_LOGIN_AUTH_TIMEOUT 10000
#define DWCAUTH_E_NOERR 0
#define DWCAUTH_E_FINISH 21
#define DWC_ERROR_AUTH_ANY 2
BOOL native_fn_0209718c(const DWCUserData*),native_fn_02097178(const DWCAccLoginId*),native_fn_02097128(const DWCAccLoginId*);void native_fn_02096ffc(const DWCAccLoginId*,u32,char*),native_fn_020970b4(DWCAccLoginId*),native_fn_02096cd8(DWCAccLoginId*,u32);u32 native_fn_0209b438(const u16*);void native_fn_02008e0c(const void*,void*,u32);void*native_fn_0209aa39(int,u32),*native_fn_0209aa44(int,u32,int);void native_fn_0209aa65(int,void*,u32);int native_fn_02097488(DWCAuthParam*,void*);
#define DWCi_Acc_IsAuthentic native_fn_0209718c
#define DWCi_Acc_LoginIdToUserName native_fn_02096ffc
#define DWCi_Acc_IsValidLoginId native_fn_02097178
#define DWCi_Acc_CheckConsoleUserId native_fn_02097128
#define DWCi_Acc_CreateTempLoginId native_fn_020970b4
#define DWCi_Acc_SetPlayerId native_fn_02096cd8
#define DWCi_WStrLen native_fn_0209b438
#define MI_CpuCopy8 native_fn_02008e0c
#define DWC_Alloc native_fn_0209aa39
#define DWC_Free native_fn_0209aa65
#define DWC_AllocEx native_fn_0209aa44
#define DWC_Auth_Create native_fn_02097488

typedef struct {
	u64 x;
	u64 mul;
	u64 add;
} MATHRandContext32;
static inline void MATH_InitRand32 (MATHRandContext32 * context, u64 seed)
{
	context->x = seed;
	context->mul = (1566083941LL << 32) + 1812433253LL;
	context->add = 2531011;
}
static inline u32 MATH_Rand32 (MATHRandContext32 * context, u32 max)
{
	context->x = context->mul * context->x + context->add;

	if (max == 0) {
		return (u32)(context->x >> 32);
	} else {
		return (u32)(((context->x >> 32) * max) >> 32);
	}
}

int native_fn_02097674(void);void native_fn_020976ac(DWCAuthResult*),native_fn_02097618(void),native_fn_0209aa64(int,void*,u32),native_fn_0209c7b0(const char*,const char*,GPCallback,DWCLoginState),native_fn_0209c6e5(GPConnection*,GPConnectResponseArg*,void*),native_fn_0209c6e4(GPConnection*,GPConnectResponseArg*,void*);
#define DWC_Auth_GetError native_fn_02097674
#define DWC_Auth_GetResult native_fn_020976ac
#define DWC_Auth_Destroy native_fn_02097618
#undef DWC_Free
#define DWC_Free native_fn_0209aa64
#define DWCi_GPConnect native_fn_0209c7b0
#define DWCi_GPConnectCallback native_fn_0209c6e5
#define DWC_ACC_USERNAME_STRING_BUFSIZE 21
#define GP_LASTNAME 1797
typedef struct{GPResult result;int profile;char nick[31],uniquenick[21],email[51],firstname[31],lastname[31],homepage[76];int icquin;char zipcode[11],countrycode[3];float longitude,latitude;char place[128];int birthday,birthmonth,birthyear,sex,publicmask;char aimname[51];int pic,occupationid,industryid,incomeid,marriedid,childcount,interests1,ownership1,conntypeid;}GPGetInfoResponseArg;
GPResult native_fn_020aa194(GPConnection*,int,const char*);void native_fn_020aa068(GPConnection*),native_fn_0209725c(DWCUserData*,const DWCAccLoginId*,int);
#define gpSetInfos native_fn_020aa194
#define gpDisconnect native_fn_020aa068
#define DWCi_Acc_SetLoginIdToUserData native_fn_0209725c

void native_main_0209c940(void);void native_main_0209caa0(GPConnection*,GPGetInfoResponseArg*,void*);
