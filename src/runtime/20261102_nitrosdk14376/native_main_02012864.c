typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed long s32;
        typedef int BOOL;
void native_fn_020072ec(const void * startAddr, u32 nBytes);
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
WMErrCode native_main_02012864(WMCallbackFunc callback, const WMParentParam * pparaBuf);
extern const u16 (*ctrdgi_fl_maxtime);
void native_fn_02011834(WMApiid id, WMCallbackFunc callback);
WMErrCode native_fn_020118a4(WMApiid id, u16 paramNum, ...);
WMErrCode native_fn_02011a34(s32 paramNum, ...);
static inline WMErrCode WMi_CheckState (u32 state)
{
    return native_fn_02011a34(1, state);
}
extern BOOL native_fn_02012940(const WMParentParam * param);
WMErrCode native_main_02012864 (WMCallbackFunc callback, const WMParentParam * pparaBuf)
{
    WMErrCode result;
    result = WMi_CheckState(WM_STATE_IDLE);
    if((result) != WM_ERRCODE_SUCCESS ) { return (result); } ;
    if (pparaBuf == ((void *)0) ) {
        ((void) 0) ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    if ((u32)pparaBuf & 0x01f) {
        ((void) 0) ;
    }
    if (pparaBuf->userGameInfoLength > 0) {
        if (pparaBuf->userGameInfo == ((void *)0) ) {
            ((void) 0) ;
            return WM_ERRCODE_INVALID_PARAM;
        }
        if ((u32)(pparaBuf->userGameInfo) & 0x01f) {
            ((void) 0) ;
        }
    }
    if ((pparaBuf->parentMaxSize +
         (pparaBuf->KS_Flag ? (2 * 16 + 4) + (2 + 4) : 0) >
         512 )
        || (pparaBuf->childMaxSize +
            (pparaBuf->KS_Flag ? 2 + (2 + 2) : 0) >
            512 )) {
        ((void) 0) ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    (void)native_fn_02012940(pparaBuf);
    native_fn_02011834(WM_APIID_SET_P_PARAM, callback);
    native_fn_020072ec((void *)pparaBuf, 64 );
    if (pparaBuf->userGameInfoLength > 0) {
        native_fn_020072ec(pparaBuf->userGameInfo, pparaBuf->userGameInfoLength);
    }
    result = native_fn_020118a4(WM_APIID_SET_P_PARAM, 1, (u32)pparaBuf);
    if((result) != WM_ERRCODE_SUCCESS ) { return (result); } ;
    return WM_ERRCODE_OPERATING;
}
BOOL native_fn_02012940 (const WMParentParam * param);
