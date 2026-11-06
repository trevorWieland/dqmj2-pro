typedef unsigned char u8;typedef unsigned int u32;typedef int BOOL;typedef unsigned int undefined4;typedef unsigned int uint;typedef unsigned long size_t;typedef unsigned long long u64;typedef void*(*DWCAuthAlloc)(unsigned long,long);typedef void(*DWCAuthFree)(unsigned long,void*,long);typedef struct DWCHttpBuffer{char*buffer;char*write_index;char*buffer_tail;unsigned long length;}DWCHttpBuffer;typedef struct DWCHttpParam{const char*url;int action;unsigned long len_recvbuf;DWCAuthAlloc alloc;DWCAuthFree free;BOOL ignoreca;int timeout;}DWCHttpParam;typedef struct DWCHttpLabelValue{char*label;char*value;}DWCHttpLabelValue;typedef struct DWCHttpParseResult{DWCHttpLabelValue*entry;int len,index;}DWCHttpParseResult;typedef struct Mutex{u32 words[6];}Mutex;typedef struct Thread{u32 prefix[27];u32 state;u32 tail[20];}Thread;typedef struct DWCHttp{u8 stack[4096];u8 initflag;DWCHttpParam param;volatile int error;char url[256];char*hostname;char*filepath;u32 hostip;BOOL ssl_enabled;unsigned short port;u8 unknown1136[2198];u8*lowrecvbuf;u8*lowsendbuf;u32 lowentropydata[8];int num_postitem;DWCHttpBuffer req,rep;Mutex content_len_mutex;int content_len,receivedbody_len;DWCHttpLabelValue labelvalue[32];Thread thread;Mutex mutex;BOOL abort;}DWCHttp;
#define NULL ((void*)0)
#define DWC_Printf(...) ((void)0)
extern void MI_CpuFill8(void*,u8,u32);extern void MI_CpuCopy8(const void*,void*,u32);extern void native_fn_0200708c(void*);extern void native_fn_02007110(void*);extern void OS_JoinThread(void*);extern u32 Base64Decode(const char*,u32,char*,u32);extern char*DWC_Http_GetResult(DWCHttp*,char*);
extern int DWCi_Http_AllocBuffer(DWCHttp*,DWCHttpBuffer*,int);extern void DWCi_Http_FreeBuffer(DWCHttp*,DWCHttpBuffer*);extern int DWCi_Http_ReallocBuffer(DWCHttp*,DWCHttpBuffer*,int);extern void DWCi_Http_DestroyResult(DWCHttp*,DWCHttpLabelValue*,int);extern undefined4 DWCi_Http_SetHostinfo(DWCHttp*,char*);extern int DWCi_Http_WriteBasicHeader(DWCHttp*);extern int DWC_Http_Add_HeaderItem(DWCHttp*,const char*,const char*);extern int OS_SNPrintf(char*,unsigned long,const char*,...);extern int DWC_Auth_Base64Encode(const char*,unsigned long,char*,unsigned long);extern void OS_InitMutex(void*);extern int OS_IsThreadTerminated(void*);extern void OS_CreateThread(void*,void(*)(void*),void*,void*,u32,u32);extern void OS_WakeupThreadDirect(void*);extern void DWCi_Http_Thread(void*);extern int DWChttpignoreca;
#include "string.h"
#define TRUE 1
#define FALSE 0
extern int DWCi_Http_AddResult(DWCHttp*,DWCHttpParseResult*,char*,char*);extern int native_fn_0201f274(const char*);extern int strncmp(const char*,const char*,unsigned long);
extern const char native_data_020dedd0[];extern const char native_data_020dedec[];
extern const char native_data_020dedd0[];
extern const char native_data_020dedec[];
extern const char native_data_020dee00[];
extern const char native_data_020deefc[];
extern const char native_data_020def04[];
extern const char native_data_020def10[];
extern const char native_data_020def14[];

extern char* native_fn_0201d780(char*,const char*,unsigned long);
extern undefined4 native_main_02098b44(DWCHttp*http,char*url);
