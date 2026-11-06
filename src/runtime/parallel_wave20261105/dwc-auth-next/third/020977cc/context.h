#define OS_GetTick native_fn_02007a9c
#define OS_Sleep native_fn_02006b7c
#define DWCi_Auth_SetError native_fn_02097d94
#define DWCi_Auth_ParseHttp native_fn_0209798c
#define DWC_Http_Abort native_fn_020983d0
#define DWC_Http_Destroy native_fn_020987b0
#define DWCi_Auth_Start native_fn_0209770c
#define DWCi_Auth_StartThread native_fn_02097540
#define OS_JoinThread native_fn_02006890
#define OS_LockMutex native_fn_0200708c
#define OS_UnlockMutex native_fn_02007110
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

typedef u64 OSTick;struct DWCHttp{u8 beforeError[4128];int error;u8 beforeThread[2836];OSThread thread;u8 trailing[28];};
#define OS_TicksToMilliSeconds(tick) ((u64)(tick)*64/33514)
#define DWCAUTH_RETRYWAIT 5000
#define DWCHTTP_E_NOERR 0
#define DWCHTTP_E_MEMERR 1
#define DWCHTTP_E_DNSERR 2
#define DWCHTTP_E_CONERR 3
#define DWCHTTP_E_SENDTOUT 4
#define DWCHTTP_E_SENDERR 5
#define DWCHTTP_E_RECVTOUT 6
#define DWCHTTP_E_ABORT 7
#define DWCHTTP_E_FINISH 8
#define DWCHTTP_E_MAX 9
u64 OS_GetTick(void);void OS_Sleep(u32),DWCi_Auth_SetError(DWCAuthError);DWCAuthError DWCi_Auth_ParseHttp(void);void native_main_020977cc(void*);
#define DWCAUTH_E_BMINITERR 1
#define DWCAUTH_E_ACERR 3
#define DWCAUTH_E_HTTPINITERR 4
#define DWCAUTH_E_CALERR 5
#define DWCAUTH_E_INVALIDPARAM 6
#define DWCAUTH_E_CANTADDHTTPHEADER 7
#define DWCAUTH_E_CANTADDPOSTITEM 8
#define DWCAUTH_E_DNSERR 9
#define DWCAUTH_E_CANTSTARTHTTPTHREAD 10
#define DWCAUTH_E_HTTPCONERR 11
#define DWCAUTH_E_HTTPPARSEERR 12
#define DWCAUTH_E_HTTPERR 13
#define DWCAUTH_E_NASPARSEERR 14
#define DWCAUTH_E_BMERR 15
#define DWCAUTH_E_NASALREADYEXIST 16
#define DWCAUTH_E_NASACCTEXPIRE 17
#define DWCAUTH_E_NASERR 18
#define DWCAUTH_E_TOOMANYRETRY 19
#define DWCAUTH_E_ABORT 20
#define DWCAUTH_E_FINISH 21
#define DWCAUTH_E_NOTINITIALIZED 22
#define DWCAUTH_E_MAX 23
