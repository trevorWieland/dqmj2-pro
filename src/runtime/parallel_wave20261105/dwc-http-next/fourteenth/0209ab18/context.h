typedef unsigned char u8;typedef unsigned short u16;typedef unsigned int u32;typedef int s32;typedef int BOOL;
#define NULL ((void*)0)
#define TRUE 1
#define FALSE 0
#define SDK_FINALROM 1
#define SDK_WIFI_VERSION_DATE 20051005
#define SDK_ASSERT(x)
#define SDK_ASSERTMSG(x,y)
#define DWC_Printf(...)
#define DWC_CONNECTINET_POWERMODE_ACTIVE 1
#define WCM_PHASE_DCF 9
#define DWC_ERROR_FATAL 9
#define DWC_ERROR_AC_ANY 5
#define DWC_AC_STATE_ERROR_FATAL (-10)
#define DWC_AC_STATE_COMPLETE 5
#define DWC_AC_AP_TYPE_NINTENDOSPOT 8
typedef enum{DWC_WDS_STATE_IDLE=0,DWC_WDS_STATE_PROCESS,DWC_WDS_STATE_COMPLETED,DWC_WDS_STATE_FAILED,DWC_WDS_STATE_ERROR}DWCWDSState;
typedef struct{u8 ssid[32],wep[32];int wepMode;char apnum[10];}DWCWDSData;
typedef void*(*DWCACAlloc)(u32,s32);typedef void(*DWCACFree)(u32,void*,s32);
typedef struct{u8 connectType,skipNetCheck;}DWCACOption;
typedef struct{void*(*alloc)(u32,s32);void(*free)(u32,void*,s32);u8 dmaNo,powerMode;DWCACOption option;}DWCACConfig;
typedef struct{volatile int ac_state;u16 state,online,dmaNo,powerMode;u8 wontExecuteWDS;DWCWDSState processWDSstate;DWCWDSData nspotInfo;}DWCInetControl;
typedef enum{DWC_CONNECTINET_STATE_NOT_INITIALIZED=0,DWC_CONNECTINET_STATE_IDLE,DWC_CONNECTINET_STATE_OPERATING,DWC_CONNECTINET_STATE_OPERATED,DWC_CONNECTINET_STATE_CONNECTED,DWC_CONNECTINET_STATE_DISCONNECTING,DWC_CONNECTINET_STATE_DISCONNECTED,DWC_CONNECTINET_STATE_ERROR,DWC_CONNECTINET_STATE_FATAL_ERROR,DWC_CONNECTINET_STATE_LAST}DWCInetResult;
typedef struct{int old;DWCInetControl*current;}InetGlobals;
extern InetGlobals native_data_021d19bc;
#define stpInetCntl (native_data_021d19bc.current)
#define stateOld (native_data_021d19bc.old)
extern void native_fn_02008d78(void*,u32,u32);
#define MI_CpuClear8(p,n) native_fn_02008d78(p,0,n)
extern void native_fn_02090b60(u32);
extern u32 native_fn_02090b54(void);
extern BOOL native_fn_02094284(DWCACConfig*);
typedef enum{DWC_ALLOCTYPE_AUTH=0,DWC_ALLOCTYPE_AC,DWC_ALLOCTYPE_BM,DWC_ALLOCTYPE_UTIL,DWC_ALLOCTYPE_BASE,DWC_ALLOCTYPE_GS,DWC_ALLOCTYPE_ND,DWC_ALLOCTYPE_LAST}DWCAllocType;
extern void*native_fn_0209aa38(DWCAllocType,u32);
extern void native_fn_0209aa64(DWCAllocType,void*,u32);
extern void native_fn_0209a9f8(int,int);
extern DWCWDSState native_fn_02096948(void);
extern void native_fn_02096b7c(void);
extern void native_fn_0209abec(const void*,const void*,int,const char*,int);
extern int native_fn_02094398(void);
extern int native_fn_0208a268(void);
extern int native_fn_02094420(void);
extern void native_fn_0209ae18(void);
extern BOOL native_fn_02096900(DWCWDSData*,int);
extern BOOL DWC_AC_Destroy(void);
extern void native_fn_0209ab18(DWCInetControl*,u16,u16,u16);
extern DWCInetResult DWC_GetInetStatus(void);
extern void native_fn_0209ac5c(void);
void native_main_0209ab18 (DWCInetControl * inetCntl, u16 dmaNo, u16 powerMode, u16 ssl_priority)
;
