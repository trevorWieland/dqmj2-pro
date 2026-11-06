#define DWC_Http_Create native_fn_0209820c
#define DWCi_BM_GetWiFiInfo native_fn_020a4660
#define DWCi_Auth_Prepare_FirstPost native_fn_02097c80
#define DWC_Http_FinishHeader native_fn_020982e4
#define OS_GetThreadPriority native_fn_02006b74
#define DWC_Http_StartThread native_fn_0209834c
#include "string.h"
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef unsigned long long u64;typedef int BOOL;typedef int DWCAuthError;typedef void*(*DWCAuthAlloc)(unsigned long,long);typedef void(*DWCAuthFree)(unsigned long,void*,long);typedef struct DWCHttp DWCHttp;typedef struct{u32 opaque0[27],activityWord108,opaque1[20];}OSThread;typedef struct{u32 opaque[6];}OSMutex;
typedef struct{int returncode;char retcode[4],datetime[15],locator[51],token[301],challenge[9],cookie[65];}DWCAuthResult;
typedef struct{u16 ingamesn[26];char gsbrcd[12];DWCAuthAlloc alloc;DWCAuthFree free;}DWCAuthParam;
typedef struct{char*label,*value;}DWCHttpLabelValue;
typedef struct{u8 stack[4096];int retry;DWCAuthError error;DWCAuthResult result;DWCAuthParam param;DWCHttpLabelValue http_labelvalue[32];DWCHttp*http;OSThread thread;OSMutex mutex;BOOL abort;}DWCAuth;
typedef struct{u32 unknownReset0,unknownReset4;DWCAuth*auth;}DWCAuthGlobals;extern DWCAuthGlobals native_data_021d18f0;
#define DWCauth native_data_021d18f0.auth
#define NULL ((void*)0)
#define TRUE 1
#define FALSE 0
#define DWC_Printf(...) ((void)0)
#define DWCAUTH_E_NOERR 0
#define DWCAUTH_E_MEMERR 2
extern const char native_data_020deb70[14],native_data_020deb80[13];
void native_fn_02008d78(void*,int,u32);void OS_LockMutex(OSMutex*),OS_UnlockMutex(OSMutex*),OS_JoinThread(OSThread*),DWC_Http_Abort(DWCHttp*),DWC_Http_Destroy(DWCHttp*),DWCi_Auth_StartThread(void);DWCAuthError DWCi_Auth_Start(BOOL);
#define MI_CpuFill8(d,v,n) native_fn_02008d78(d,v,n)
void native_main_020975b8(void);
void native_main_02097618(void);
void native_main_02097654(void);
DWCAuthError native_main_02097488(DWCAuthParam*,void*);

typedef struct{const char*url;int action;u32 len_recvbuf;DWCAuthAlloc alloc;DWCAuthFree free;BOOL ignoreca;int timeout;}DWCHttpParam;extern DWCHttpParam native_data_020deb2c;
#define DWCauthhttpparam native_data_020deb2c
extern const char native_data_020deb90[];
#define DWC_AUTH_NAS_URL native_data_020deb90
typedef struct DWCWiFiInfo DWCWiFiInfo;extern DWCWiFiInfo native_data_021d18fc;
#define DWC_auth_wifiinfo native_data_021d18fc
typedef struct{u32 opaque;OSThread*current;}OSThreadInfoView;extern OSThreadInfoView native_data_020e33e4;
#define OS_GetCurrentThread() (native_data_020e33e4.current)
#define DWCHTTP_E_NOERR 0
#define DWCAUTH_E_HTTPINITERR 4
int DWC_Http_Create(DWCHttp*,DWCHttpParam*),DWC_Http_FinishHeader(DWCHttp*);void DWCi_BM_GetWiFiInfo(DWCWiFiInfo*),DWC_Http_StartThread(DWCHttp*,u32);u32 OS_GetThreadPriority(const OSThread*);DWCAuthError DWCi_Auth_Prepare_FirstPost(DWCHttp*,const char*,DWCAuthParam*);DWCAuthError native_main_0209770c(BOOL);



extern const char native_data_020deb48[];
