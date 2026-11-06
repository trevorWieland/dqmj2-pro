typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef int BOOL;
void native_fn_02008430();
extern void native_fn_02008430(void);
void native_fn_02008bf8(const void * srcp, void * destp, u32 size);
static inline void MI_CpuCopy16 (const void * src, void * dest, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	native_fn_02008bf8(src, dest, size);
}
void native_fn_020072d0(void * startAddr, u32 nBytes);
typedef enum WMApiid {
	WM_APIID_INITIALIZE = 0,
	WM_APIID_RESET,
	WM_APIID_END,
	WM_APIID_ENABLE,
	WM_APIID_DISABLE,
	WM_APIID_POWER_ON,
	WM_APIID_POWER_OFF,
	WM_APIID_SET_P_PARAM,
	WM_APIID_START_PARENT,
	WM_APIID_END_PARENT,
	WM_APIID_START_SCAN,
	WM_APIID_END_SCAN,
	WM_APIID_START_CONNECT,
	WM_APIID_DISCONNECT,
	WM_APIID_START_MP,
	WM_APIID_SET_MP_DATA,
	WM_APIID_END_MP,
	WM_APIID_START_DCF,
	WM_APIID_SET_DCF_DATA,
	WM_APIID_END_DCF,
	WM_APIID_SET_WEPKEY,
	WM_APIID_START_KS,
	WM_APIID_END_KS,
	WM_APIID_GET_KEYSET,
	WM_APIID_SET_GAMEINFO,
	WM_APIID_SET_BEACON_IND,
	WM_APIID_START_TESTMODE,
	WM_APIID_STOP_TESTMODE,
	WM_APIID_VALARM_MP,
	WM_APIID_SET_LIFETIME,
	WM_APIID_MEASURE_CHANNEL,
	WM_APIID_INIT_W_COUNTER,
	WM_APIID_GET_W_COUNTER,
	WM_APIID_SET_ENTRY,
	WM_APIID_AUTO_DEAUTH,
	WM_APIID_SET_MP_PARAMETER,
	WM_APIID_SET_BEACON_PERIOD,
	WM_APIID_AUTO_DISCONNECT,
	WM_APIID_START_SCAN_EX,
	WM_APIID_SET_WEPKEY_EX,
	WM_APIID_SET_PS_MODE,
	WM_APIID_START_TESTRXMODE,
	WM_APIID_STOP_TESTRXMODE,
	WM_APIID_KICK_MP_PARENT,
	WM_APIID_KICK_MP_CHILD,
	WM_APIID_KICK_MP_RESUME,
	WM_APIID_ASYNC_KIND_MAX,
	WM_APIID_INDICATION = 128,
	WM_APIID_PORT_SEND,
	WM_APIID_PORT_RECV,
	WM_APIID_READ_STATUS,
	WM_APIID_UNKNOWN = 255
} WMApiid;
typedef enum WMPort {
	WM_PORT_RAWDATA = 0,
	WM_PORT_BT = 1,
	WM_PORT_RESERVE_02 = 2,
	WM_PORT_RESERVE_03 = 3,
	WM_PORT_RESERVE_10 = 8,
	WM_PORT_RESERVE_11 = 9,
	WM_PORT_RESERVE_12 = 10,
	WM_PORT_RESERVE_13 = 11
} WMPort;
typedef enum WMErrCode {
	WM_ERRCODE_SUCCESS               = 0,
	WM_ERRCODE_FAILED                = 1,
	WM_ERRCODE_OPERATING             = 2,
	WM_ERRCODE_ILLEGAL_STATE         = 3,
	WM_ERRCODE_WM_DISABLE            = 4,
	WM_ERRCODE_NO_KEYSET             = 5,
	WM_ERRCODE_NO_DATASET            = 5,
	WM_ERRCODE_INVALID_PARAM         = 6,
	WM_ERRCODE_NO_CHILD              = 7,
	WM_ERRCODE_FIFO_ERROR            = 8,
	WM_ERRCODE_TIMEOUT               = 9,
	WM_ERRCODE_SEND_QUEUE_FULL       = 10,
	WM_ERRCODE_NO_ENTRY              = 11,
	WM_ERRCODE_OVER_MAX_ENTRY        = 12,
	WM_ERRCODE_INVALID_POLLBITMAP    = 13,
	WM_ERRCODE_NO_DATA               = 14,
	WM_ERRCODE_SEND_FAILED           = 15,
	WM_ERRCODE_DCF_TEST,
	WM_ERRCODE_WL_INVALID_PARAM,
	WM_ERRCODE_WL_LENGTH_ERR,
	WM_ERRCODE_FLASH_ERROR,
	WM_ERRCODE_MAX
} WMErrCode;
typedef enum WMStateCode {
	WM_STATECODE_PARENT_START                = 0,
	WM_STATECODE_BEACON_SENT                 = 2,
	WM_STATECODE_SCAN_START                  = 3,
	WM_STATECODE_PARENT_NOT_FOUND            = 4,
	WM_STATECODE_PARENT_FOUND                = 5,
	WM_STATECODE_CONNECT_START               = 6,
	WM_STATECODE_BEACON_LOST                 = 8,
	WM_STATECODE_CONNECTED                   = 7,
	WM_STATECODE_CHILD_CONNECTED             = 7,
	WM_STATECODE_DISCONNECTED                = 9,
	WM_STATECODE_DISCONNECTED_FROM_MYSELF    = 26,
	WM_STATECODE_MP_START                    = 10,
	WM_STATECODE_MPEND_IND                   = 11,
	WM_STATECODE_MP_IND                      = 12,
	WM_STATECODE_MPACK_IND                   = 13,
	WM_STATECODE_DCF_START                   = 14,
	WM_STATECODE_DCF_IND                     = 15,
	WM_STATECODE_BEACON_RECV                 = 16,
	WM_STATECODE_DISASSOCIATE                = 17,
	WM_STATECODE_REASSOCIATE                 = 18,
	WM_STATECODE_AUTHENTICATE                = 19,
	WM_STATECODE_PORT_INIT                   = 25,
	WM_STATECODE_PORT_SEND                   = 20,
	WM_STATECODE_PORT_RECV                   = 21,
	WM_STATECODE_FIFO_ERROR                  = 22,
	WM_STATECODE_INFORMATION                 = 23,
	WM_STATECODE_UNKNOWN                     = 24,
	WM_STATECODE_MAX                         = 27
} WMStateCode;
typedef void (*WMCallbackFunc) (void * arg);
typedef struct WMMpRecvBuf {
	u16 rsv1[3];
	u16 length;
	u16 rsv2[1];
	u16 ackTimeStamp;
	u16 timeStamp;
	u16 rate_rssi;
	u16 rsv3[2];
	u16 rsv4[2];
	u8 destAdrs[6];
	u8 srcAdrs[6];
	u16 rsv5[3];
	u16 seqCtrl;
	u16 txop;
	u16 bitmap;
	u16 wmHeader;
	u16 data[2];
} WMMpRecvBuf, WMmpRecvBuf;
typedef struct WMParentParam {
	u16 * userGameInfo;
	u16 userGameInfoLength;
	u16 padding;
	u32 ggid;
	u16 tgid;
	u16 entryFlag;
	u16 maxEntry;
	u16 multiBootFlag;
	u16 KS_Flag;
	u16 CS_Flag;
	u16 beaconPeriod;
	u16 rsv1[8 / sizeof(u16)];
	u16 rsv2[16 / sizeof(u16)];
	u16 channel;
	u16 parentMaxSize;
	u16 childMaxSize;
	u16 rsv[4];
} WMParentParam, WMpparam;
typedef struct WMGameInfo {
	u16 magicNumber;
	u8 ver;
	u8 platform;
	u32 ggid;
	u16 tgid;
	u8 userGameInfoLength;
	union {
		u8 gameNameCount_attribute;
		u8 attribute;
	};
	u16 parentMaxSize;
	u16 childMaxSize;
	union {
		u16 userGameInfo[112 / sizeof(u16)];
		struct {
			u16 userName[8 / sizeof(u16)];
			u16 gameName[16 / sizeof(u16)];
			u16 padd1[44];
		} old_type;
	};
} WMGameInfo, WMgameInfo;
typedef struct WMBssDesc {
        u16 length;
        u16 rssi;
        u8 bssid[6 ];
        u16 ssidLength;
        u8 ssid[32 ];
        u16 capaInfo;
        struct {
            u16 basic;
            u16 support;
        } rateSet;
        u16 beaconPeriod;
        u16 dtimPeriod;
        u16 channel;
        u16 cfpPeriod;
        u16 cfpMaxDuration;
        u16 gameInfoLength;
        u16 otherElementCount;
        WMGameInfo gameInfo;
    } WMBssDesc, WMbssDesc;
typedef struct WMScanParam {
	WMBssDesc * scanBuf;
	u16 channel;
	u16 maxChannelTime;
	u8 bssid[6 ];
	u16 rsv[9];
} WMScanParam, WMscanParam;
typedef struct WMCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
} WMCallback;
typedef struct WMStartScanCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
	u16 state;
	u8 macAddress[6 ];
	u16 channel;
	u16 linkLevel;
	u16 ssidLength;
	u16 ssid[32 / sizeof(u16)];
	u16 gameInfoLength;
	WMGameInfo gameInfo;
} WMStartScanCallback, WMstartScanCallback;
typedef struct WMStartConnectCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
	u16 state;
	u16 aid;
	u16 reason;
	u16 wlStatus;
	u8 macAddress[6 ];
	u16 parentSize;
	u16 childSize;
} WMStartConnectCallback, WMstartConnectCallback;
typedef struct WMStartMPCallback {
	u16 apiid;
	u16 errcode;
	u16 state;
	u8 reserved[2];
	WMMpRecvBuf * recvBuf;
	u16 timeStamp;
	u16 rate_rssi;
	u8 destAdrs[6];
	u8 srcAdrs[6];
	u16 seqNum;
	u16 tmptt;
	u16 pollbmp;
	u16 reserved2;
} WMStartMPCallback, WMstartMPCallback;
typedef struct WMIndCallback {
	u16 apiid;
	u16 errcode;
	u16 state;
	u16 reason;
} WMIndCallback, WMindCallback;
WMErrCode native_fn_02011f58(u16 port, WMCallbackFunc callback, void * arg);
WMErrCode native_fn_02012824(WMCallbackFunc callback);
WMErrCode native_fn_02012a3c(WMCallbackFunc callback, const WMScanParam * param);
WMErrCode native_fn_02012cb8(WMCallbackFunc callback, const WMBssDesc * pInfo, const u8 * ssid, BOOL powerSave, u16 authMode);
static inline WMErrCode WM_StartConnect (WMCallbackFunc callback, const WMBssDesc * pInfo, const u8 * ssid)
{
	return native_fn_02012cb8(callback, pInfo, ssid, 1 , 0 );
}
WMErrCode native_fn_02012fdc(WMCallbackFunc callback,
                       u16 * recvBuf,
                       u16 recvBufSize,
                       u16 * sendBuf,
                       u16 sendBufSize,
                       u16 mpFreq,
                       u16 defaultRetryCount,
                       BOOL minPollBmpMode,
                       BOOL singlePacketMode, BOOL fixFreqMode, BOOL ignoreFatalError);
WMErrCode native_fn_02014200(WMCallbackFunc callback, u16 tableNumber, u16 camLifeTime, u16 frameLifeTime, u16 mpLifeTime);
static inline BOOL WM_IsBssidEqual (const u8 * idp1, const u8 * idp2)
{
	return ((*idp1 == *idp2) &&
	        (*(idp1 + 1) == *(idp2 + 1)) &&
	        (*(idp1 + 2) == *(idp2 + 2)) &&
	        (*(idp1 + 3) == *(idp2 + 3)) &&
	        (*(idp1 + 4) == *(idp2 + 4)) && (*(idp1 + 5) == *(idp2 + 5)));
}
void native_fn_0200854c(u32 dmaNo, const void * src, void * dest, u32 size);
typedef struct {
	u8 favoriteColor : 4;
	u8 playerNo : 4;
	u8 nameLength;
	u16 name[10 ];
} MBUserInfo;
extern const u16 (*ctrdgi_fl_maxtime);
typedef struct ParentInfo {
	union {
		WMBssDesc parentInfo[1];
__attribute__ ((aligned(32))) u8 parentInfo_area[192 ];
	};
	WMStartScanCallback scan_data;
	u8 reserved1[8];
} ParentInfo;
typedef void (*MBCallbackFunc) (u16 type, void * arg);
typedef struct {
	union {
		WMParentParam parentParam;
__attribute__ ((aligned(32))) u8 parentParam_area[64 ];
	};
__attribute__ ((aligned(32))) u16 sendBuf[(0x400) / sizeof(u16)];
	union {
		WMBssDesc parentInfoBuf;
__attribute__ ((aligned(32))) u8 parentInfoBuf_area[192 ];
	};
	u16 p_sendlen;
	u16 p_recvlen;
	WMMpRecvBuf * recvBuf;
	void (*callback_ptr) (void * arg);
	u8 mpBusy;
	u8 mbIsStarted;
	u8 reserved0[10];
	u16 sendBufSize;
	u16 recvBufSize;
	MBCallbackFunc callback;
	const WMBssDesc * pInfo;
	u16 mode;
	u16 endReq;
	u16 mpStarted;
	u16 child_bitmap;
	u16 contSend;
	u8 reserved1[2];
__attribute__ ((aligned(4))) u8 uname[8 ];
__attribute__ ((aligned(4))) u8 gname[16 ];
	u16 currentTgid;
	u8 reserved2[22];
__attribute__ ((aligned(32))) u16 userGameInfo[((112 + 32) & ~(32 - 1)) / sizeof(u16)];
	struct {
		u16 found_parent_count;
		u16 my_aid;
		BOOL scanning_flag;
		BOOL scan_channel_flag;
		int last_found_parent_no;
		u8 reserved8[16];
		ParentInfo parent_info[16 ];
	};
} MBiParam;
int native_fn_02018570(void);
typedef struct MB_CommCommonWork {
__attribute__ ((aligned(32))) u32 sendbuf[(0x400) / sizeof(u32)];
__attribute__ ((aligned(32))) u32 recvbuf[(0x80) * 15 * 2 / sizeof(u32)];
	MBUserInfo user;
	u16 isMbInitialized;
	int block_size_max;
	BOOL start_mp_busy;
	BOOL is_started_ex;
	u8 padding[28];
} MB_CommCommonWork;
typedef struct {
u16 field_0000;
u16 field_0002;
u16 field_0004;
u16 field_0006;
unsigned char field_0008[4];
BOOL field_000c;
unsigned char field_0010[20];
} NativeStorage_020dce94;
extern NativeStorage_020dce94 native_data_main_020dce94;
void native_fn_020189b0(u16 apiid, int errcode);
typedef struct {
u16 field_0000;
unsigned char padding_0002[2];
u8 * field_0004;
MBiParam * field_0008;
MB_CommCommonWork * field_000c;
unsigned char padding_0010[16];
__attribute__ ((aligned(32))) WMscanParam field_0020;
} NativeStorage_020ec360;
extern NativeStorage_020ec360 native_data_main_020ec360;
BOOL native_fn_02016ca4 (WMscanParam * p);
BOOL native_fn_02016d14 (void);
void native_fn_02016dc4 (void * arg);
void native_fn_02017660 (void * arg);
int native_fn_02018570 (void);
void native_fn_020189b0 (u16 apiid, int errcode);
