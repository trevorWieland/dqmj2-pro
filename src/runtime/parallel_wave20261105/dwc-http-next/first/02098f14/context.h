typedef unsigned char u8;typedef unsigned int u32;typedef int BOOL;typedef unsigned int undefined4;typedef unsigned int uint;typedef unsigned long size_t;typedef unsigned long long u64;typedef void*(*DWCAuthAlloc)(unsigned long,long);typedef void(*DWCAuthFree)(unsigned long,void*,long);typedef struct DWCHttpBuffer{char*buffer;char*write_index;char*buffer_tail;unsigned long length;}DWCHttpBuffer;typedef struct DWCHttpParam{const char*url;int action;unsigned long len_recvbuf;DWCAuthAlloc alloc;DWCAuthFree free;BOOL ignoreca;int timeout;}DWCHttpParam;typedef struct DWCHttpLabelValue{char*label;char*value;}DWCHttpLabelValue;typedef struct DWCHttpParseResult{DWCHttpLabelValue*entry;int len,index;}DWCHttpParseResult;typedef struct Mutex{u32 words[6];}Mutex;typedef struct Thread{u32 prefix[27];u32 state;u32 tail[20];}Thread;typedef struct DWCHttp{u8 stack[4096];u8 initflag;DWCHttpParam param;int error;u8 unknown1024[2548];Mutex content_len_mutex;int content_len,receivedbody_len;DWCHttpLabelValue labelvalue[32];Thread thread;Mutex mutex;BOOL abort;}DWCHttp;
#define NULL ((void*)0)
#define DWC_Printf(...) ((void)0)
extern void native_fn_02008d78(void*,u8,u32);extern void native_fn_02008e0c(const void*,void*,u32);extern unsigned long native_fn_0201d69c(const char*);extern char*native_fn_0201d6b8(char*,const char*);extern int native_fn_0201d800(const char*,const char*);extern void native_fn_0200708c(void*);extern void native_fn_02007110(void*);extern void native_fn_02006890(void*);extern u32 native_fn_0209a83c(const char*,u32,char*,u32);extern char*native_fn_02098ed8(DWCHttp*,char*);
extern const char native_data_020deec4[];
extern const char native_data_020deed8[];
extern const char native_data_020deeec[];
extern const char native_data_020def18[];
extern const char native_data_020def38[];
extern const char native_data_020def58[];
extern const char native_data_020def74[];
extern const char native_data_020defb0[];
extern const char native_data_020defcc[];
