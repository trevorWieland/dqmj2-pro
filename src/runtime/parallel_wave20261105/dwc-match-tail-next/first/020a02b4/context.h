typedef unsigned char u8;typedef unsigned int u32;typedef void*GPConnection;typedef int GPResult;
#define NULL ((void*)0)
#define DWC_MATCH_COMMAND_ADD_MESSAGE_MAX 512
#define DWC_GP_COMMAND_STRING native_data_020e02ac
#define DWC_GP_COMMAND_MATCH_STRING native_data_020e02b4
#define DWC_MATCHING_VERSION 3
#define SDK_ASSERTMSG(...)
#define DWC_Printf(...)
extern int native_fn_020061ac(char*,unsigned long,const char*,...);
extern unsigned long strlen(const char*);
extern char*strchr(const char*,int);
extern void native_fn_02008e0c(const void*,void*,u32);
extern GPResult native_fn_020aa7c0(GPConnection*,int,const char*);
extern const char native_data_020e02a4[];
extern const char native_data_020e02ac[];
extern const char native_data_020e02b4[];
GPResult native_main_020a02b4 (GPConnection * connection, u8 command, int profileID, const char * message)
;
