typedef unsigned short int u16;

typedef unsigned long u32;

typedef void * OSMessage;

void native_host_arm7_arm_037fdf9c(const void * srcp, void * destp, u32 size);

static inline void MI_CpuCopy16 (const void * src, void * dest, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	native_host_arm7_arm_037fdf9c(src, dest, size);
}

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

typedef struct WMGetWirelessCounterCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
	u32 TX_Success;
	u32 TX_Failed;
	u32 TX_Retry;
	u32 TX_AckError;
	u32 TX_Unicast;
	u32 TX_Multicast;
	u32 TX_WEP;
	u32 TX_Beacon;
	u32 RX_RTS;
	u32 RX_Fragment;
	u32 RX_Unicast;
	u32 RX_Multicast;
	u32 RX_WEP;
	u32 RX_Beacon;
	u32 RX_FCSError;
	u32 RX_DuplicateError;
	u32 RX_MPDuplicateError;
	u32 RX_ICVError;
	u32 RX_FrameCtrlError;
	u32 RX_LengthError;
	u32 RX_PLCPError;
	u32 RX_BufferOverflowError;
	u32 RX_PathError;
	u32 RX_RateError;
	u32 RX_FCSOK;
	u32 TX_MP;
	u32 TX_KeyData;
	u32 TX_NullKey;
	u32 RX_MP;
	u32 RX_MPACK;
	u32 MPKeyResponseError[15];
} WMGetWirelessCounterCallback, WMgetWirelessCounterCallback;

extern const u16 (*ctrdgi_fl_maxtime);

typedef	struct {
	struct {
		u32		success;
		u32		failed;
		u32		retry;
		u32		ackErr;
		u32		unicast;
		u32		multicast;
		u32		wep;
		u32		beacon;
	} tx;
	struct {
		u32		rts;
		u32		fragment;
		u32		unicast;
		u32		multicast;
		u32		wep;
		u32		beacon;
		u32		fcsErr;
		u32		duplicateErr;
		u32		mpDuplicateErr;
		u32		icvErr;
		u32		fcErr;
		u32		lengthErr;
		u32		plcpErr;
		u32		bufOvfErr;
		u32		pathErr;
		u32		rateErr;
		u32		fcsOk;
	} rx;
	struct {
		u32		txMp;
		u32		txKey;
		u32		txNull;
		u32		rxMp;
		u32		rxMpAck;
		u32		keyResponseErr[15];
	} multiPoll;
} WlCounter;

typedef	struct {
	u16		code;
	u16		length;
} WlCmdHeader;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				rsv1;
	WlCounter		counter;
} WlDevGetInfoCfm;

typedef WlDevGetInfoCfm WlDevGetWirelessCounterCfm;

void native_host_arm7_arm_038073a4(void *ptr);

void *native_host_arm7_arm_038073f0(void);

void native_host_arm7_main_027e5b00(OSMessage msg);

WlDevGetWirelessCounterCfm *native_host_arm7_arm_027e290c(u16 *buf);

static void WmspError(u16 wlCommand, u16 wlResult);
