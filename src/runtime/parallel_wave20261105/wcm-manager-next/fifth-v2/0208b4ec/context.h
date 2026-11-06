typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned long u32;typedef signed long s32;typedef unsigned long long u64;typedef int BOOL;typedef u32 OSIntrMode;typedef u64 OSTick;typedef int WMLinkLevel;typedef int WMErrCode;typedef struct{u32 opaque[11];}OSAlarm;
typedef struct{ s32 dmano;void*pbdbuffer;s32 nbdbuffer;s32 nbdmode;}WCMConfig;
typedef union{s32 n;void*p;}WCMNoticeParameter;typedef struct{s16 notify;s16 result;WCMNoticeParameter parameter[3];}WCMNotice;typedef void(*WCMNotify)(WCMNotice*);
typedef struct{u16 length,rssi;u8 bssid[6];u16 ssidLength;u8 ssid[32];u16 capaInfo;struct{u16 basic,support;}rateSet;u16 beaconPeriod,dtimPeriod,channel,cfpPeriod,cfpMaxDuration,gameInfoLength,otherElementCount;u32 opaqueGameInfo[32];}WMBssDesc;
typedef struct{WMBssDesc*scanBuf;u16 scanBufSize,channelList,maxChannelTime;u8 bssid[6];u16 scanType,ssidLength;u8 ssid[32];u16 ssidMatchLength,rsv2[7];}WMScanExParam;
typedef struct{u16 frameID,rsv1[2],length,rsv2[3],rate_rssi,rsv3[4];u8 destAdrs[6],srcAdrs[6];u16 rsv4[4],data[2];}WMDcfRecvBuf;
typedef struct{u16 apiid,errcode,state;u8 reserved[2];WMDcfRecvBuf*recvBuf;}WMStartDCFCallback;
typedef struct WCMWork{u8 wmWork[0xf00];u8 sendBuf[0x600];u8 recvBuf[0xc40];WMBssDesc bssDesc;struct{u8 key[80];u8 mode,keyId,reserved[14];}wepDesc;u32 phase;u32 option;u16 maxScanTime;u8 apListLock;u8 resetting;WCMConfig config;WCMNotify notify;s16 notifyId;u16 authId;u32 scanCount;WMScanExParam scanExParam;OSAlarm keepAliveAlarm;u16 wlStatusOnConnectFail;u8 reserved[6];}WCMWork;
typedef struct{u32 count;void*head;void*tail;}WCMApListHeader;
extern WCMWork*native_data_021cfcb4;
extern OSIntrMode native_fn_02007ff4(void);extern OSIntrMode native_fn_02008008(OSIntrMode);extern void native_fn_0208a4f0(void);extern void native_fn_0208b44c(void);extern BOOL native_fn_02007a24(void);extern void native_fn_020079ac(void);extern BOOL native_fn_02007c58(void);extern void native_fn_02007bd8(void);extern void native_fn_02007c68(OSAlarm*);extern void native_fn_02008d78(void*,u8,u32);extern void native_fn_02007e10(OSAlarm*);extern void native_fn_02007da4(OSAlarm*,OSTick,void(*)(void*),void*);extern void native_fn_0208a660(void*);extern int native_fn_020127ec(void(*)(void*));extern void native_fn_0208a5ac(u32);extern void native_fn_0208a550(s16,void*,void*,s32);extern void native_fn_0208af1c(void*);
#define WM_SIZE_BSSID 6
#define TRUE 1
#define FALSE 0
#define WM_ERRCODE_OPERATING 2
#define NULL ((void*)0)
#define SDK_ASSERT_ON_COMPILE(x) ((void)0)
#define WCMi_Warning(...) ((void)0)
#define WCMi_Printf(...) ((void)0)
#define MI_CpuClear8(dst,size) native_fn_02008d78(dst,0,size)
#define OS_SecondsToTicks(s) ((OSTick)(((33514000ULL)*(s))/64))
#define WCM_WORK_SIZE   8960
#define WCM_RESULT_SUCCESS          0
#define WCM_RESULT_FAILURE          1
#define WCM_RESULT_PROGRESS         2
#define WCM_RESULT_ACCEPT           3
#define WCM_RESULT_REJECT           4
#define WCM_RESULT_WMDISABLE        5
#define WCM_RESULT_NOT_ENOUGH_MEM   6
#define WCM_RESULT_FATAL_ERROR      7
#define WCM_PHASE_NULL              0
#define WCM_PHASE_WAIT              1
#define WCM_PHASE_WAIT_TO_IDLE      2
#define WCM_PHASE_IDLE              3
#define WCM_PHASE_IDLE_TO_WAIT      4
#define WCM_PHASE_IDLE_TO_SEARCH    5
#define WCM_PHASE_SEARCH            6
#define WCM_PHASE_SEARCH_TO_IDLE    7
#define WCM_PHASE_IDLE_TO_DCF       8
#define WCM_PHASE_DCF               9
#define WCM_PHASE_DCF_TO_IDLE       10
#define WCM_PHASE_FATAL_ERROR       11
#define WCM_PHASE_IRREGULAR         12
#define WCM_PHASE_TERMINATING       13
#define WCM_NOTIFY_COMMON           0
#define WCM_NOTIFY_STARTUP          1
#define WCM_NOTIFY_CLEANUP          2
#define WCM_NOTIFY_BEGIN_SEARCH     3
#define WCM_NOTIFY_END_SEARCH       4
#define WCM_NOTIFY_CONNECT          5
#define WCM_NOTIFY_DISCONNECT       6
#define WCM_NOTIFY_FOUND_AP         7
#define WCM_NOTIFY_SEARCH_AROUND    8
#define WCM_NOTIFY_TERMINATE        9
#define WCM_APLIST_UNLOCK           0
#define WCM_APLIST_LOCK             1
#define WCM_APLIST_MODE_IGNORE      0
#define WCM_APLIST_MODE_EXCHANGE    1
#define WCM_WEPMODE_NONE            0
#define WCM_WEPMODE_40              1
#define WCM_WEPMODE_104             2
#define WCM_WEPMODE_128             3
#define WCM_CAM_LIFETIME            80
#define WCM_BSSID_SIZE              WM_SIZE_BSSID
#define WCM_ESSID_SIZE              WM_SIZE_SSID
#define WCM_APLIST_SIZE             192
#define WCM_APLIST_EX_SIZE          16
#define WCM_APLIST_BLOCK_SIZE       (WCM_APLIST_EX_SIZE + WCM_APLIST_SIZE)
#define WCM_WEP_SIZE                WM_SIZE_WEPKEY
#define WCM_WEP_EX_SIZE             (1 + 1 + 14)
#define WCM_WEP_STRUCT_SIZE         (WCM_WEP_SIZE + WCM_WEP_EX_SIZE)
#define WCM_DCF_RECV_EXCESS_SIZE    (sizeof(WMDcfRecvBuf) - 4)
#define WCM_DCF_SEND_EXCESS_SIZE    0
#define WCM_DCF_RECV_SIZE           (WM_DCF_MAX_SIZE + WCM_DCF_RECV_EXCESS_SIZE)
#define WCM_DCF_RECV_BUF_SIZE       (WCM_ROUNDUP32(WCM_DCF_RECV_SIZE))
#define WCM_DCF_SEND_BUF_SIZE       (WCM_ROUNDUP32(WM_DCF_MAX_SIZE))
#define WCM_ETC_BUF_SIZE            108
#define WCM_ADDITIONAL_RATESET      0x0003
#define WCM_CAMOUFLAGE_RATESET      0x0024
#define WCM_AID_MIN                 1
#define WCM_AID_MAX                 2007
#define WCM_BSSID_ANY                  ((void *)native_data_020dc3c8)
#define WCM_ESSID_ANY                  ((void *)native_data_020dc3d0)
#define WCM_OPTION_TEST_CHANNEL        0x00008000
#define WCM_OPTION_FILTER_CHANNEL      0x00003ffe
#define WCM_OPTION_MASK_CHANNEL        (WCM_OPTION_TEST_CHANNEL | WCM_OPTION_FILTER_CHANNEL)
#define WCM_OPTION_CHANNEL_1           (WCM_OPTION_TEST_CHANNEL | 0x00000002)
#define WCM_OPTION_CHANNEL_2           (WCM_OPTION_TEST_CHANNEL | 0x00000004)
#define WCM_OPTION_CHANNEL_3           (WCM_OPTION_TEST_CHANNEL | 0x00000008)
#define WCM_OPTION_CHANNEL_4           (WCM_OPTION_TEST_CHANNEL | 0x00000010)
#define WCM_OPTION_CHANNEL_5           (WCM_OPTION_TEST_CHANNEL | 0x00000020)
#define WCM_OPTION_CHANNEL_6           (WCM_OPTION_TEST_CHANNEL | 0x00000040)
#define WCM_OPTION_CHANNEL_7           (WCM_OPTION_TEST_CHANNEL | 0x00000080)
#define WCM_OPTION_CHANNEL_8           (WCM_OPTION_TEST_CHANNEL | 0x00000100)
#define WCM_OPTION_CHANNEL_9           (WCM_OPTION_TEST_CHANNEL | 0x00000200)
#define WCM_OPTION_CHANNEL_10          (WCM_OPTION_TEST_CHANNEL | 0x00000400)
#define WCM_OPTION_CHANNEL_11          (WCM_OPTION_TEST_CHANNEL | 0x00000800)
#define WCM_OPTION_CHANNEL_12          (WCM_OPTION_TEST_CHANNEL | 0x00001000)
#define WCM_OPTION_CHANNEL_13          (WCM_OPTION_TEST_CHANNEL | 0x00002000)
#define WCM_OPTION_CHANNEL_ALL         (WCM_OPTION_TEST_CHANNEL | WCM_OPTION_FILTER_CHANNEL)
#define WCM_OPTION_CHANNEL_RDC         (WCM_OPTION_CHANNEL_1 | WCM_OPTION_CHANNEL_7 | WCM_OPTION_CHANNEL_13)
#define WCM_OPTION_TEST_POWER          0x00020000
#define WCM_OPTION_FILTER_POWER        0x00010000
#define WCM_OPTION_MASK_POWER          (WCM_OPTION_TEST_POWER | WCM_OPTION_FILTER_POWER)
#define WCM_OPTION_POWER_SAVE          (WCM_OPTION_TEST_POWER | 0x00000000)
#define WCM_OPTION_POWER_ACTIVE        (WCM_OPTION_TEST_POWER | 0x00010000)
#define WCM_OPTION_TEST_AUTH           0x00080000
#define WCM_OPTION_FILTER_AUTH         0x00040000
#define WCM_OPTION_MASK_AUTH           (WCM_OPTION_TEST_AUTH | WCM_OPTION_FILTER_AUTH)
#define WCM_OPTION_AUTH_OPENSYSTEM     (WCM_OPTION_TEST_AUTH | 0x00000000)
#define WCM_OPTION_AUTH_SHAREDKEY      (WCM_OPTION_TEST_AUTH | 0x00040000)
#define WCM_OPTION_TEST_SCANTYPE       0x00200000
#define WCM_OPTION_FILTER_SCANTYPE     0x00100000
#define WCM_OPTION_MASK_SCANTYPE       (WCM_OPTION_TEST_SCANTYPE | WCM_OPTION_FILTER_SCANTYPE)
#define WCM_OPTION_SCANTYPE_PASSIVE    (WCM_OPTION_TEST_SCANTYPE | 0x00000000)
#define WCM_OPTION_SCANTYPE_ACTIVE     (WCM_OPTION_TEST_SCANTYPE | 0x00100000)
#define WCM_OPTION_TEST_ROUNDSCAN      0x00800000
#define WCM_OPTION_FILTER_ROUNDSCAN    0x00400000
#define WCM_OPTION_MASK_ROUNDSCAN      (WCM_OPTION_TEST_ROUNDSCAN | WCM_OPTION_FILTER_ROUNDSCAN)
#define WCM_OPTION_ROUNDSCAN_IGNORE    (WCM_OPTION_TEST_ROUNDSCAN | 0x00000000)
#define WCM_OPTION_ROUNDSCAN_NOTIFY    (WCM_OPTION_TEST_ROUNDSCAN | 0x00400000)
#define WCM_ROUNDUP32(_x_)      (((_x_) + 0x01f) & ~(0x01f))
#define WCM_ROUNDDOWN32(_x_)    ((_x_) & ~(0x01f))
#define WCM_ROUNDUP4(_x_)       (((_x_) + 0x03) & ~(0x03))
#define WCM_ROUNDDOWN4(_x_)     ((_x_) & ~(0x03))
#define WCM_RESETTING_OFF          0
#define WCM_RESETTING_ON           1
#define WCM_APLIST_BLOCK_EMPTY     0
#define WCM_APLIST_BLOCK_OCCUPY    1
#define WCM_KEEP_ALIVE_SPAN       ((OSTick) 70)
#define WCM_CONNECT_STATUSCODE_ILLEGAL_RATESET  18
#define WCM_NETWORK_CAPABILITY_KIND_MASK        0x0003
#define WCM_NETWORK_CAPABILITY_KIND_ESS         0x0001
#define WCM_NETWORK_CAPABILITY_KIND_IBSS        0x0002
#define WCM_NETWORK_CAPABILITY_PRIVACY          0x0010
#define WCM_NETWORK_CAPABILITY_PREAMBLE_MASK    0x0020
#define WCM_NETWORK_CAPABILITY_PREAMBLE_LONG    0x0000
#define WCM_NETWORK_CAPABILITY_PREAMBLE_SHORT   0x0020
#define WCM_RSSI_COUNT_MAX                      16
#define WCM_RSSI_BORDER_HIGH                    28
#define WCM_RSSI_BORDER_MIDDLE                  22
#define WCM_RSSI_BORDER_LOW                     16
typedef struct{u16 state;}WMStatusPrefix;typedef struct{u16 apiid,errcode,wlCmdID,wlResult;}WMCallback;typedef struct{u16 apiid,errcode,state,reason;}WMIndCallback;
extern void native_fn_0208a328(WCMConfig*,WCMNotify);extern WMErrCode native_fn_020115b4(void*,u16);extern u16 native_fn_02012290(void);extern WMErrCode native_fn_020117c4(void);extern WMErrCode native_fn_02011f14(void(*)(void*));extern WMErrCode native_fn_02012630(void(*)(void*));extern WMErrCode native_fn_02012724(void(*)(void*));extern WMErrCode native_fn_020126a4(void(*)(void*));extern WMErrCode native_fn_020133f4(void(*)(void*));extern void native_fn_0208a6d8(void*);extern void native_fn_0208a730(void*);extern void native_fn_0208ae50(void*);extern const WMStatusPrefix*native_fn_02011e90(void);extern void native_fn_020072d0(void*,u32);extern void native_fn_0208a698(void);
#define WM_ERRCODE_SUCCESS 0
#define WM_ERRCODE_FAILED 1
#define WM_ERRCODE_ILLEGAL_STATE 3
#define WM_ERRCODE_WM_DISABLE 4
#define WM_ERRCODE_INVALID_PARAM 6
#define WM_ERRCODE_FIFO_ERROR 8
#define WM_STATE_READY 0
#define WM_STATE_STOP 1
#define WM_STATE_IDLE 2
#define WM_STATECODE_FIFO_ERROR 22
#define WM_APIID_AUTO_DISCONNECT 37
extern WMErrCode native_fn_020126e4(void(*)(void*));extern WMErrCode native_fn_020141b0(void(*)(void*),u16);extern WMErrCode native_fn_0201407c(void(*)(void*),u16,u16,const u8*);extern WMErrCode native_fn_02012cb8(void(*)(void*),const WMBssDesc*,const u8*,BOOL,u16);extern WMErrCode native_fn_02012d84(void(*)(void*),u16);extern void native_fn_0208ab60(void*);extern void native_fn_0208ad04(void*);extern void native_fn_0208b7f0(u8);extern void native_fn_0208b474(WMDcfRecvBuf*);extern void native_fn_0208a3e0(void*,void*,u32);extern WMErrCode native_fn_02012b28(void(*)(void*),const WMScanExParam*);extern void native_fn_0208a940(void*);
#define WM_ERRCODE_MAX 20
#define WM_APIID_ENABLE 3
#define WM_APIID_DISABLE 4
#define WM_APIID_POWER_ON 5
#define WM_APIID_POWER_OFF 6
#define WM_APIID_SET_LIFETIME 29
#define WM_APIID_SET_BEACON_IND 25
#define WM_APIID_SET_WEPKEY_EX 39
#define WM_AUTHMODE_SHARED_KEY 1
#define WM_AUTHMODE_OPEN_SYSTEM 0
#define WM_STATECODE_DCF_START 14
#define WM_STATECODE_DCF_IND 15
#define WM_SIZE_WEPKEY 80
#define WM_DCF_MAX_SIZE 1508
typedef struct{u8 mode,keyId,key[80];}WCMWepDesc;typedef struct WCMApList{u8 state,reserved;u16 linkLevel;u32 index;void*previous;void*next;u32 data[48];}WCMApList;typedef struct{u16 apiid,errcode,wlCmdID,wlResult,state,channelList;u8 reserved[2];u16 bssDescCount;WMBssDesc*bssDesc[16];u16 linkLevel[16];}WMStartScanExCallback;
extern u32 native_fn_0208a28c(u32);extern void native_fn_02008e0c(const void*,void*,u32);extern WMErrCode native_fn_02014200(void(*)(void*),u16,u16,u16,u16);extern u16 native_fn_020123d0(void);extern u16 native_fn_0208a508(u16);extern u32 native_fn_0208a66c(u32);extern u32 native_fn_0208a690(u32);extern void native_fn_0208b260(WMBssDesc*,u16);extern void native_fn_0208a57c(s16,s16,void*,void*,s32);extern WMErrCode native_fn_02012c78(void(*)(void*));extern void native_fn_0208ab0c(void*);extern WCMWork*native_fn_0208a31c(void);extern WCMApList*native_fn_0208b3a4(u32);
extern const u8 native_data_020dc3c8[6];extern const u8 native_data_020dc3d0[32];
#define WM_SIZE_SSID 32
#define WM_SIZE_SCAN_EX_BUF 1024
#define WM_SCANTYPE_ACTIVE 0
#define WM_SCANTYPE_PASSIVE 1
#define WM_STATECODE_PARENT_FOUND 5
typedef struct OSThread OSThread;typedef struct{OSThread*head,*tail;}OSThreadQueue;typedef struct{OSThreadQueue queue;OSThread*thread;int count;void*previous,*next;}OSMutex;typedef void(*WCMRecvInd)(const u8*,const u8*,const u8*,s32);typedef struct{u8 initialized,reserved[3];OSThreadQueue sendQ;OSMutex sendMutex;WMErrCode sendResult;WCMRecvInd recvCallback;}WCMCpsifWork;extern WCMCpsifWork native_data_021cfcb8;
typedef struct{u16 apiid,errcode,wlCmdID,wlResult,state,aid,reason,wlStatus;u8 macAddress[6];u16 parentSize,childSize;}WMStartConnectCallback;
extern WMErrCode native_fn_02013288(void(*)(void*),WMDcfRecvBuf*,u16);extern void native_fn_0208ad94(void*);extern WCMApList*native_fn_0208b35c(u8*);extern WCMApList*native_fn_0208b2c0(void);extern WCMApList*native_fn_0208b338(void);extern void native_fn_02008ca4(const void*,void*,u32);extern void native_fn_0208b3d8(WCMApList*);extern BOOL native_fn_0208b72c(u8*,u8*);extern BOOL native_fn_0208b6e0(OSMutex*);extern void native_fn_0208b70c(OSMutex*);extern WMErrCode native_fn_02013328(void(*)(void*),const u8*,const u16*,u16);extern void native_fn_0208b6d0(void*);extern void native_fn_0208b6a8(void*);extern void native_fn_0200708c(OSMutex*);extern void native_fn_02007110(OSMutex*);extern void native_fn_020068d4(OSThreadQueue*);
#define WM_ERRCODE_NO_ENTRY 11
#define WM_ERRCODE_OVER_MAX_ENTRY 12
#define WM_STATECODE_CONNECT_START 6
#define WM_STATECODE_CONNECTED 7
#define WM_STATECODE_BEACON_LOST 8
#define WM_STATECODE_DISCONNECTED 9
#define WM_STATECODE_DISCONNECTED_FROM_MYSELF 26
#define SDK_VERSION_MAJOR 4
#define SDK_VERSION_MINOR 2
#define SDK_VERSION_RELSTEP 30001
#define WCM_CPSIF_RESULT_BEFORE_INIT (-1)
#define WCM_CPSIF_RESULT_NO_CONNECTION (-4)
#define WCM_CPSIF_RESULT_SEND_FAILURE (-5)
u8 * native_main_0208b4ec (void);
