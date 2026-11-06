typedef unsigned char u8;typedef unsigned int u32;typedef int BOOL;typedef unsigned int undefined4;typedef unsigned int uint;typedef unsigned long size_t;typedef unsigned long long u64;typedef void*(*DWCAuthAlloc)(unsigned long,long);typedef void(*DWCAuthFree)(unsigned long,void*,long);typedef struct DWCHttpBuffer{char*buffer;char*write_index;char*buffer_tail;unsigned long length;}DWCHttpBuffer;typedef struct DWCHttpParam{const char*url;int action;unsigned long len_recvbuf;DWCAuthAlloc alloc;DWCAuthFree free;BOOL ignoreca;int timeout;}DWCHttpParam;typedef struct DWCHttpLabelValue{char*label;char*value;}DWCHttpLabelValue;typedef struct DWCHttpParseResult{DWCHttpLabelValue*entry;int len,index;}DWCHttpParseResult;typedef struct Mutex{u32 words[6];}Mutex;typedef struct Thread{u32 prefix[27];u32 id;u32 tail[20];}Thread;typedef struct DWCHttp{u8 stack[4096];u8 initflag;DWCHttpParam param;volatile int error;char url[256];char*hostname;char*filepath;u32 hostip;BOOL ssl_enabled;unsigned short port;u8 unknown1136[2198];u8*lowrecvbuf;u8*lowsendbuf;u32 lowentropydata[8];int num_postitem;DWCHttpBuffer req,rep;Mutex content_len_mutex;int content_len,receivedbody_len;DWCHttpLabelValue labelvalue[32];Thread thread;Mutex mutex;BOOL abort;}DWCHttp;
#define NULL ((void*)0)
#define DWC_Printf(...) ((void)0)
extern void native_fn_02008d78(void*,u8,u32);extern void MI_CpuCopy8(const void*,void*,u32);extern void native_fn_0200708c(void*);extern void native_fn_02007110(void*);extern void native_fn_02006890(void*);extern u32 Base64Decode(const char*,u32,char*,u32);extern char*DWC_Http_GetResult(DWCHttp*,char*);
extern int DWCi_Http_AllocBuffer(DWCHttp*,DWCHttpBuffer*,int);extern void DWCi_Http_FreeBuffer(DWCHttp*,DWCHttpBuffer*);extern int DWCi_Http_ReallocBuffer(DWCHttp*,DWCHttpBuffer*,int);extern void DWCi_Http_DestroyResult(DWCHttp*,DWCHttpLabelValue*,int);extern int DWCi_Http_SetHostinfo(DWCHttp*,const char*);extern int DWCi_Http_WriteBasicHeader(DWCHttp*);extern int DWC_Http_Add_HeaderItem(DWCHttp*,const char*,const char*);extern int OS_SNPrintf(char*,unsigned long,const char*,...);extern int DWC_Auth_Base64Encode(const char*,unsigned long,char*,unsigned long);extern void native_fn_02007074(void*);extern int OS_IsThreadTerminated(void*);extern void OS_CreateThread(void*,void(*)(void*),void*,void*,u32,u32);extern void OS_WakeupThreadDirect(void*);extern void DWCi_Http_Thread(void*);extern int DWChttpignoreca;
#include "string.h"
typedef int DWCNetcheckError;typedef struct{DWCAuthAlloc alloc;DWCAuthFree free;void*bmworkarea;}DWCNetcheckParam;typedef struct{u8 stack[4096];int error;int returncode;DWCHttpLabelValue http_labelvalue[32];DWCNetcheckParam param;char*body_302;char*body_wayport;Thread thread;Mutex mutex;}DWCNetcheck;typedef struct{DWCNetcheck*netcheck;int hotspot;u32 unknown[3];DWCHttp*http;}NetcheckStorage;extern NetcheckStorage native_data_021d1914;
#define DWCnetcheck native_data_021d1914.netcheck
#define DWCishotspot native_data_021d1914.hotspot
#define DWChttp native_data_021d1914.http
extern void native_fn_02099178(void);extern void native_fn_02097618(void);extern void native_fn_020975b8(void);
#define TRUE 1
#define FALSE 0
#define DWCNETCHECK_E_MEMERR 4
#define DWCNETCHECK_E_NOERR 0
#define ALLOC_DWC_NETCHECK ((u32)native_data_020df010)
#define ALLOC_DWC_HTTP ((u32)native_data_020df024)
extern const char native_data_020df010[];
extern const char native_data_020df024[];
extern const char native_data_020df034[];
extern const char native_data_020df044[];
extern const char native_data_020df060[];
extern const char native_data_020df080[];

extern void native_fn_020983d0(DWCHttp*);
extern void native_main_020990f0(void);
