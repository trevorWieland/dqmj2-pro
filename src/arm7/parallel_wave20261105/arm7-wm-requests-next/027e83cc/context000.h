typedef unsigned char u8;

typedef unsigned short int u16;

typedef unsigned long u32;

typedef void * OSMessage;

void native_host_arm7_arm_037fe12c(const void * src, void * dest, u32 size);

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

typedef struct WMMPParam {
	u32 mask;
	u16 minFrequency;
	u16 frequency;
	u16 maxFrequency;
	u16 parentSize;
	u16 childSize;
	u16 parentInterval;
	u16 childInterval;
	u16 parentVCount;
	u16 childVCount;
	u16 defaultRetryCount;
	u8 minPollBmpMode;
	u8 singlePacketMode;
	u8 ignoreFatalErrorMode;
	u8 ignoreSizePrecheckMode;
} WMMPParam;

typedef struct WMSetMPParameterReq {
	u16 apiid;
	u16 reserved;
	WMMPParam param;
} WMSetMPParameterReq;

typedef struct WMSetMPParameterCallback {
	u16 apiid;
	u16 errcode;
	u32 mask;
	WMMPParam oldParam;
} WMSetMPParameterCallback;

extern const u16 (*ctrdgi_fl_maxtime);

void native_host_arm7_arm_038073a4(void *ptr);

void *native_host_arm7_arm_038073f0(void);

WMErrCode native_host_arm7_arm_027e8428(const WMMPParam *param, WMMPParam *old_param);

void native_host_arm7_main_027e83cc(OSMessage msg);
