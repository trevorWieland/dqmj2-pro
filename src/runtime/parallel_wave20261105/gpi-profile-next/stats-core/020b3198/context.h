typedef unsigned int u32;typedef void*DArray;typedef enum{rt_authcb,rt_datacb,rt_savecb,rt_profilecb}reqtype_t;typedef int persisttype_t;typedef struct{reqtype_t reqtype;int localid,profileid;persisttype_t pdtype;int pdindex;void*instance,*callback;}serverreq_t;
#define NULL ((void*)0)
extern char*native_data_020e15f0;extern char native_data_020e163c[];
typedef struct{unsigned char opaque[20];DArray serverreqs;}StatsReqGlobalView;extern StatsReqGlobalView native_data_021d2514;
#define enc native_data_020e15f0
#define enc1 native_data_020e163c
#define serverreqs native_data_021d2514.serverreqs
int native_fn_020a8640(DArray);void*native_fn_020a8644(DArray,int);char*native_fn_020b326c(char*,int);void native_fn_020b3198(char*,int);void native_fn_020b34f8(char*,int);
#define ArrayLength native_fn_020a8640
#define ArrayNth native_fn_020a8644
#define FindFinal native_fn_020b326c
#define xcode_buf native_fn_020b3198
#define ProcessStatement native_fn_020b34f8
#define DOXCODE(b,l,e) enc=e;xcode_buf(b,l);
typedef int time_t;typedef char gsi_char;typedef void(*PersAuthCallbackFn)(int,int,int,char*,void*);typedef void(*PersDataCallbackFn)(int,int,persisttype_t,int,int,time_t,char*,int,void*);typedef void(*PersDataSaveCallbackFn)(int,int,persisttype_t,int,int,time_t,void*);typedef void(*ProfileCallbackFn)(int,int,int,void*);
#define GSI_UNUSED(x) ((void)(x))
int native_fn_0201f274(const char*);int native_fn_0201d914(const char*,const char*,u32);char*native_fn_020b3250(const char*,const char*);int native_fn_020b32c4(reqtype_t,int,int);void native_fn_020b35dc(int,int,time_t,char*,int);void native_fn_020b331c(char*,int);void native_fn_020b338c(char*,int);void native_fn_020b33ec(char*,int);void native_fn_020b348c(char*,int);void native_fn_020a8720(DArray,int);
#define atoi native_fn_0201f274
#define strncmp native_fn_0201d914
#define value_for_key_safe native_fn_020b3250
#define FindRequest native_fn_020b32c4
#define CallReqCallback native_fn_020b35dc
#define ProcessPlayerAuth native_fn_020b331c
#define ProcessGetPid native_fn_020b338c
#define ProcessGetData native_fn_020b33ec
#define ProcessSetData native_fn_020b348c
#define ArrayDeleteAt native_fn_020a8720
