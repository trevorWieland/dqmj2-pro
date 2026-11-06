typedef unsigned char u8;typedef unsigned int u32;typedef int BOOL;typedef unsigned int undefined4;typedef unsigned int uint;typedef unsigned long size_t;typedef unsigned long long u64;typedef void*(*DWCAuthAlloc)(unsigned long,long);typedef void(*DWCAuthFree)(unsigned long,void*,long);typedef struct DWCHttpBuffer{char*buffer;char*write_index;char*buffer_tail;unsigned long length;}DWCHttpBuffer;typedef struct DWCHttpParam{const char*url;int action;unsigned long len_recvbuf;DWCAuthAlloc alloc;DWCAuthFree free;BOOL ignoreca;int timeout;}DWCHttpParam;typedef struct DWCHttpLabelValue{char*label;char*value;}DWCHttpLabelValue;typedef struct DWCHttpParseResult{DWCHttpLabelValue*entry;int len,index;}DWCHttpParseResult;typedef struct Mutex{u32 words[6];}Mutex;typedef struct Thread{u32 prefix[27];u32 state;u32 tail[20];}Thread;typedef struct DWCHttp{u8 stack[4096];u8 initflag;DWCHttpParam param;volatile int error;char url[256];char*hostname;char*filepath;u32 hostip;BOOL ssl_enabled;unsigned short port;u8 unknown1136[2198];u8*lowrecvbuf;u8*lowsendbuf;u32 lowentropydata[8];int num_postitem;DWCHttpBuffer req,rep;Mutex content_len_mutex;int content_len,receivedbody_len;DWCHttpLabelValue labelvalue[32];Thread thread;Mutex mutex;BOOL abort;}DWCHttp;
#define NULL ((void*)0)
#define DWC_Printf(...) ((void)0)
extern void native_fn_02008d78(void*,u8,u32);extern void MI_CpuCopy8(const void*,void*,u32);extern void OS_LockMutex(void*);extern void OS_UnlockMutex(void*);extern void OS_JoinThread(void*);extern u32 Base64Decode(const char*,u32,char*,u32);extern char*DWC_Http_GetResult(DWCHttp*,char*);
extern int native_fn_02098a7c(DWCHttp*,DWCHttpBuffer*,int);extern void native_fn_02098ab4(DWCHttp*,DWCHttpBuffer*);extern int native_fn_02098adc(DWCHttp*,DWCHttpBuffer*,int);extern void native_fn_02098f74(DWCHttp*,DWCHttpLabelValue*,int);extern int native_fn_02098b44(DWCHttp*,const char*);extern int native_fn_02098830(DWCHttp*);extern int native_fn_020988bc(DWCHttp*,const char*,const char*);extern int native_fn_020061ac(char*,unsigned long,const char*,...);extern int native_fn_0209a738(const char*,unsigned long,char*,unsigned long);extern void native_fn_02007074(void*);extern int native_fn_020068c0(void*);extern void native_fn_020065f0(void*,void(*)(void*),void*,void*,u32,u32);extern void native_fn_0200698c(void*);extern void native_fn_02098574(void*);extern int native_data_021d1910;
#include "string.h"
extern const char native_data_020ded8c[];
extern const char native_data_020deda4[];
extern const char native_data_020dedbc[];
extern const char native_data_020dedc8[];
extern const char native_data_020dedd0[];
extern const char native_data_020dedd8[];
extern const char native_data_020deddc[];
extern const char native_data_020dee04[];
extern const char native_data_020dee1c[];
extern const char native_data_020deeb4[];
extern const char native_data_020deeb8[];
