typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed long s32;
void native_fn_02008e0c(const void * src, void * dest, u32 size);
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
typedef enum WMState {
	WM_STATE_READY = 0,
	WM_STATE_STOP,
	WM_STATE_IDLE,
	WM_STATE_CLASS1,
	WM_STATE_TESTMODE,
	WM_STATE_SCAN,
	WM_STATE_CONNECT,
	WM_STATE_PARENT,
	WM_STATE_CHILD,
	WM_STATE_MP_PARENT,
	WM_STATE_MP_CHILD,
	WM_STATE_DCF_CHILD,
	WM_STATE_TESTMODE_RX,
	WM_STATE_MAX
} WMState;
typedef void (*WMCallbackFunc) (void * arg);
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
typedef struct WMScanExParam {
	WMBssDesc * scanBuf;
	u16 scanBufSize;
	u16 channelList;
	u16 maxChannelTime;
	u8 bssid[6 ];
	u16 scanType;
	u16 ssidLength;
	u8 ssid[32 ];
	u16 ssidMatchLength;
	u16 rsv2[7];
} WMScanExParam, WMscanExParam;
typedef struct WMStartScanExReq {
	u16 apiid;
	u16 channelList;
	WMBssDesc * scanBuf;
	u16 scanBufSize;
	u16 maxChannelTime;
	u8 bssid[6 ];
	u16 scanType;
	u16 ssidLength;
	u8 ssid[32 ];
	u16 ssidMatchLength;
	u16 rsv[2];
} WMStartScanExReq, WMstartScanExReq;
WMErrCode native_main_02012b28(WMCallbackFunc callback, const WMScanExParam * param);
extern const u16 (*ctrdgi_fl_maxtime);
void native_fn_02011834(WMApiid id, WMCallbackFunc callback);
WMErrCode native_fn_02011950(void * data, u32 length);
WMErrCode native_fn_02011a34(s32 paramNum, ...);
WMErrCode native_main_02012b28 (WMCallbackFunc callback, const WMScanExParam * param)
{
    WMErrCode result;
    result = native_fn_02011a34(3, WM_STATE_IDLE, WM_STATE_CLASS1, WM_STATE_SCAN);
    if((result) != WM_ERRCODE_SUCCESS ) { return (result); } ;
    if (param == ((void *)0) ) {
        ((void) 0) ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    if (param->scanBuf == ((void *)0) ) {
        ((void) 0) ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    if (param->scanBufSize > 1024 ) {
        ((void) 0)
            ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    if ((u32)(param->scanBuf) & 0x01f) {
        ((void) 0) ;
    }
    if (param->ssidLength > 32 ) {
        ((void) 0) ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    if (param->scanType != 0 && param->scanType != 1
        && param->scanType != 2
        && param->scanType != 3 ) {
        ((void) 0)
            ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    if ((param->scanType == 2
         || param->scanType == 3 ) && param->ssidMatchLength > 32 ) {
        ((void) 0)
            ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    native_fn_02011834(WM_APIID_START_SCAN_EX, callback);
    {
        WMStartScanExReq Req;
        Req.apiid = WM_APIID_START_SCAN_EX;
        Req.channelList = param->channelList;
        Req.scanBuf = param->scanBuf;
        Req.scanBufSize = param->scanBufSize;
        Req.maxChannelTime = param->maxChannelTime;
        native_fn_02008e0c(param->bssid, Req.bssid, 6 );
        Req.scanType = param->scanType;
        Req.ssidMatchLength = param->ssidMatchLength;
        Req.ssidLength = param->ssidLength;
        native_fn_02008e0c(param->ssid, Req.ssid, 32 );
        result = native_fn_02011950(&Req, sizeof(Req));
        if((result) != WM_ERRCODE_SUCCESS ) { return (result); } ;
    }
    return WM_ERRCODE_OPERATING;
}
