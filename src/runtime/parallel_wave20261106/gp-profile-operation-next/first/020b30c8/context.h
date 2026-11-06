typedef unsigned int u32;
#define NULL ((void*)0)
#define INVALID_SOCKET (-1)
#define init_complete 5
typedef struct{char*enc;int sock;}StatsInitializedView;extern StatsInitializedView native_data_020e15f0;
typedef struct{unsigned char opaque0[8];int rcvlen;unsigned char opaque12[12];int rcvmax;unsigned char opaque28[12];char*rcvbuffer;int state;}StatsReceiveView;extern StatsReceiveView native_data_021d2514;
#define sock native_data_020e15f0.sock
#define stats_initstate native_data_021d2514.state
#define rcvlen native_data_021d2514.rcvlen
#define rcvmax native_data_021d2514.rcvmax
#define rcvbuffer native_data_021d2514.rcvbuffer
int native_fn_020b3264(int);void*native_fn_020a928c(void*,u32);int native_fn_020a8bf0(int,void*,int,int);void native_fn_020b3068(void);int native_fn_020b3588(char*,int);void*native_fn_0201b1bc(void*,const void*,u32);
#define SocketReadable native_fn_020b3264
#define gsirealloc native_fn_020a928c
#define recv native_fn_020a8bf0
#define CloseStatsConnection native_fn_020b3068
#define ProcessInBuffer native_fn_020b3588
#define memmove native_fn_0201b1bc

int native_main_020b30c8(void);
