typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef int BOOL;
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
int native_main_02018828(const void * buf, int len, int pollbmp);
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
unsigned char padding_0002[2];
u8 * field_0004;
MBiParam * field_0008;
MB_CommCommonWork * field_000c;
unsigned char padding_0010[16];
__attribute__ ((aligned(32))) WMscanParam field_0020;
} NativeStorage_020ec360;
extern NativeStorage_020ec360 native_data_main_020ec360;
static inline int conv_errcode (int errcode)
{
    return (errcode == WM_ERRCODE_OPERATING) ? WM_ERRCODE_SUCCESS : errcode;
}
void native_fn_020176d0 (void * arg);
int native_fn_020187dc (WMCallbackFunc callback, const u16 * sendData, u16 sendDataSize, u16 tmptt, u16 pollbmp);
