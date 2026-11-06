typedef unsigned char u8;typedef unsigned int u32;typedef int BOOL;typedef unsigned int undefined4;typedef unsigned int uint;typedef unsigned long size_t;typedef unsigned long long u64;typedef void*(*DWCAuthAlloc)(unsigned long,long);typedef void(*DWCAuthFree)(unsigned long,void*,long);typedef struct DWCHttpBuffer{char*buffer;char*write_index;char*buffer_tail;unsigned long length;}DWCHttpBuffer;typedef struct DWCHttpParam{const char*url;int action;unsigned long len_recvbuf;DWCAuthAlloc alloc;DWCAuthFree free;BOOL ignoreca;int timeout;}DWCHttpParam;typedef struct DWCHttpLabelValue{char*label;char*value;}DWCHttpLabelValue;typedef struct DWCHttpParseResult{DWCHttpLabelValue*entry;int len,index;}DWCHttpParseResult;typedef struct Mutex{u32 words[6];}Mutex;typedef struct Thread{u32 prefix[27];u32 id;u32 tail[20];}Thread;typedef struct DWCHttp{u8 stack[4096];u8 initflag;DWCHttpParam param;volatile int error;char url[256];char*hostname;char*filepath;u32 hostip;BOOL ssl_enabled;unsigned short port;u8 unknown1136[2198];u8*lowrecvbuf;u8*lowsendbuf;u32 lowentropydata[8];int num_postitem;DWCHttpBuffer req,rep;Mutex content_len_mutex;int content_len,receivedbody_len;DWCHttpLabelValue labelvalue[32];Thread thread;Mutex mutex;BOOL abort;}DWCHttp;
#define NULL ((void*)0)
#define DWC_Printf(...) ((void)0)
extern void native_fn_02008d78(void*,u8,u32);extern void MI_CpuCopy8(const void*,void*,u32);extern void OS_LockMutex(void*);extern void OS_UnlockMutex(void*);extern void OS_JoinThread(void*);extern u32 Base64Decode(const char*,u32,char*,u32);extern char*native_fn_02098ed8(DWCHttp*,char*);
extern int DWCi_Http_AllocBuffer(DWCHttp*,DWCHttpBuffer*,int);extern void DWCi_Http_FreeBuffer(DWCHttp*,DWCHttpBuffer*);extern int DWCi_Http_ReallocBuffer(DWCHttp*,DWCHttpBuffer*,int);extern void DWCi_Http_DestroyResult(DWCHttp*,DWCHttpLabelValue*,int);extern int DWCi_Http_SetHostinfo(DWCHttp*,const char*);extern int DWCi_Http_WriteBasicHeader(DWCHttp*);extern int DWC_Http_Add_HeaderItem(DWCHttp*,const char*,const char*);extern int OS_SNPrintf(char*,unsigned long,const char*,...);extern int DWC_Auth_Base64Encode(const char*,unsigned long,char*,unsigned long);extern void OS_InitMutex(void*);extern int native_fn_020068c0(void*);extern void OS_CreateThread(void*,void(*)(void*),void*,void*,u32,u32);extern void OS_WakeupThreadDirect(void*);extern void DWCi_Http_Thread(void*);extern int DWChttpignoreca;
#include "string.h"
typedef int DWCSvlState;typedef int DWCHttpError;typedef struct{BOOL status;char svlhost[65];char svltoken[301];}DWCSvlResult;typedef struct{DWCAuthAlloc alloc;DWCAuthFree free;DWCHttp http;DWCSvlResult*result;}DWCSvlIntWorkarea;extern DWCSvlIntWorkarea*native_data_021d19a4;extern void native_fn_0209a9f8(int,int);extern int DWCi_Svl_ParseHttp(void);
#define DWCHTTP_E_ABORT 7
#define DWCHTTP_E_FINISH 8
typedef struct{u32 unknown;void*current;}Scheduler;extern Scheduler native_data_020e33e4;extern DWCHttpParam native_data_020deb2c;extern int native_fn_02006b74(void*);extern void native_fn_02008430(void);extern int native_fn_0209820c(DWCHttp*,DWCHttpParam*);extern int native_fn_02097dc4(void*);extern int native_fn_02097fac(DWCHttp*,const void*,int);extern int native_fn_02098954(DWCHttp*,const char*,const char*,u32);extern int native_fn_020982e4(DWCHttp*);extern void native_fn_0209834c(DWCHttp*,int);extern int native_fn_02098d0c(DWCHttp*,int);extern int native_fn_02098f14(DWCHttp*,const char*,char*,u32);extern u32 native_fn_02099bf8(char*);extern int native_fn_0201f274(const char*);
extern int native_data_020ec9b0;
extern const char native_data_020df23c[];
extern const char native_data_020df25c[];
extern const char native_data_020df264[];
extern const char native_data_020df26c[];
extern const char native_data_020df270[];
extern const char native_data_020df278[];
extern const char native_data_020df284[];
extern const char native_data_020df290[];
extern const char native_data_020df298[];
extern const char native_data_020df2a8[];

extern void native_fn_020987b0(DWCHttp*);
extern BOOL native_main_02099df4(char*svc,DWCSvlResult*result);
