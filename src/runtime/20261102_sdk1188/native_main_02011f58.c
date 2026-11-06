#include "native_main_02011f58_types.h"

static inline void MI_CpuClear8 (void * dest, u32 size)
{
	native_fn_02008d78(dest, 0, size);
}
void native_fn_020081fc(u8 * macAddress);
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
typedef struct {
	u16 next;
	u16 port;
	u16 destBitmap;
	u16 restBitmap;
	u16 sentBitmap;
	u16 sendingBitmap;
	u16 padding;
	u16 size;
	u16 seqNo;
	u16 retryCount;
	const u16 * data;
	WMCallbackFunc callback;
	void * arg;
} WMPortSendQueueData;
typedef struct {
	u16 head;
	u16 tail;
} WMPortSendQueue;
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
typedef struct WMDcfRecvBuf {
	u16 frameID;
	u16 rsv1[2];
	u16 length;
	u16 rsv2[3];
	u16 rate_rssi;
	u16 rsv3[4];
	u8 destAdrs[6];
	u8 srcAdrs[6];
	u16 rsv4[4];
	u16 data[2];
} WMDcfRecvBuf, WMdcfRecvBuf;
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
typedef struct WMStatus {
	u16 state;
	u16 BusyApiid;
	BOOL apiBusy;
	BOOL scan_continue;
	BOOL mp_flag;
	BOOL dcf_flag;
	BOOL ks_flag;
	BOOL dcf_sendFlag;
	BOOL VSyncFlag;
	u8 wlVersion[8 ];
	u16 macVersion;
	u16 rfVersion;
	u16 bbpVersion[4 / sizeof(u16)];
	u16 mp_parentSize;
	u16 mp_childSize;
	u16 mp_parentMaxSize;
	u16 mp_childMaxSize;
	u16 mp_sendSize;
	u16 mp_recvSize;
	u16 mp_maxSendSize;
	u16 mp_maxRecvSize;
	u16 mp_parentVCount;
	u16 mp_childVCount;
	u16 mp_parentInterval;
	u16 mp_childInterval;
	OSTick mp_parentIntervalTick;
	OSTick mp_childIntervalTick;
	u16 mp_minFreq;
	u16 mp_freq;
	u16 mp_maxFreq;
	u16 mp_vsyncOrderedFlag;
	u16 mp_vsyncFlag;
	s16 mp_count;
	s16 mp_limitCount;
	u16 mp_resumeFlag;
	u16 mp_prevPollBitmap;
	u16 mp_prevWmHeader;
	u16 mp_prevTxop;
	u16 mp_prevDataLength;
	u16 mp_recvBufSel;
	u16 mp_recvBufSize;
	WMMpRecvBuf * mp_recvBuf[2];
	u32 * mp_sendBuf;
	u16 mp_sendBufSize;
	u16 mp_ackTime;
	u16 mp_waitAckFlag;
	u16 mp_readyBitmap;
	u16 mp_newFrameFlag;
	u16 mp_setDataFlag;
	u16 mp_sentDataFlag;
	u16 mp_bufferEmptyFlag;
	u16 mp_isPolledFlag;
	u16 mp_minPollBmpMode;
	u16 mp_singlePacketMode;
	u8 reserved_c[2];
	u16 mp_defaultRetryCount;
	u16 mp_ignoreFatalErrorMode;
	u16 mp_ignoreSizePrecheckMode;
	u16 mp_pingFlag;
	u16 mp_pingCounter;
	u8 dcf_destAdr[6 ];
	u16 * dcf_sendData;
	u16 dcf_sendSize;
	u16 dcf_recvBufSel;
	WMDcfRecvBuf * dcf_recvBuf[2];
	u16 dcf_recvBufSize;
	u16 curr_tgid;
	u16 linkLevel;
	u16 minRssi;
	u16 rssiCounter;
	u16 beaconIndicateFlag;
	u16 wepKeyId;
	u16 pwrMgtMode;
	u32 miscFlags;
	u16 VSyncBitmap;
	u16 valarm_queuedFlag;
	u32 v_tsf;
	u32 v_tsf_bak;
	u32 v_remain;
	u16 valarm_counter;
	u8 reserved_e[2];
	u8 MacAddress[6 ];
	u16 mode;
	WMParentParam pparam;
	u8 childMacAddress[15 ][6 ];
	u16 child_bitmap;
	WMBssDesc * pInfoBuf;
	u16 aid;
	u8 parentMacAddress[6 ];
	u16 scan_channel;
	u8 reserved_f[4];
	u16 wepMode;
	BOOL wep_flag;
	u16 wepKey[80 / sizeof(u16)];
	u16 rate;
	u16 preamble;
	u16 tmptt;
	u16 retryLimit;
	u16 enableChannel;
	u16 allowedChannel;
	u16 portSeqNo[15 + 1][8 ];
	WMPortSendQueueData sendQueueData[32 ];
	WMPortSendQueue sendQueueFreeList;
	WMPortSendQueue sendQueue[4 ];
	WMPortSendQueue readyQueue[4 ];
	OSMutex sendQueueMutex;
	BOOL sendQueueInUse;
	OSTick mp_lastRecvTick[1 + 15 ];
	OSTick mp_lifeTimeTick;
	u16 mp_current_minFreq;
	u16 mp_current_freq;
	u16 mp_current_maxFreq;
	u16 mp_current_minPollBmpMode;
	u16 mp_current_singlePacketMode;
	u16 mp_current_defaultRetryCount;
	u16 mp_current_ignoreFatalErrorMode;
	u8 reserved[2];
} WMStatus, WMstatus;
typedef struct WMArm7Buf {
	WMStatus * status;
	u8 reserved_a[4];
	u32 * fifo7to9;
	u8 reserved_b[4];
	WMBssDesc connectPInfo;
	u32 requestBuf[512 / sizeof(u32)];
} WMArm7Buf, WMarm7Buf;
typedef struct WMArm9Buf {
	WMArm7Buf * WM7;
	WMStatus * status;
	u32 * indbuf;
	u32 * fifo9to7;
	u32 * fifo7to9;
	u16 dmaNo;
	u16 scanOnlyFlag;
	WMCallbackFunc CallbackTable[(WM_APIID_ASYNC_KIND_MAX - 2) ];
	WMCallbackFunc indCallback;
	WMCallbackFunc portCallbackTable[16 ];
	void * portCallbackArgument[16 ];
	u32 connectedAidBitmap;
	u16 myAid;
	u8 reserved1[512 -
	             (20 + 4 + 4 * (WM_APIID_ASYNC_KIND_MAX - 2) + 4 + (4 + 4) * 16 + 6)];
} WMArm9Buf, WMarm9Buf;
typedef struct WMPortRecvCallback {
	u16 apiid;
	u16 errcode;
	u16 state;
	u16 port;
	WMMpRecvBuf * recvBuf;
	u16 * data;
	u16 length;
	u16 aid;
	u8 macAddress[6 ];
	u16 seqNo;
	void * arg;
	u16 myAid;
	u16 connectedAidBitmap;
	u8 ssid[24 ];
	u16 reason;
	u16 rsv;
	u16 maxSendDataSize;
	u16 maxRecvDataSize;
} WMPortRecvCallback;
WMErrCode native_main_02011f58(u16 port, WMCallbackFunc callback, void * arg);
u16 native_fn_02011eb4(void);
u16 native_fn_02011ee4(void);
extern const u16 (*ctrdgi_fl_maxtime);
WMArm9Buf * native_fn_020119c0(void);
WMErrCode native_fn_020119d0(void);
WMErrCode native_main_02011f58 (u16 port, WMCallbackFunc callback, void * arg)
{
    WMErrCode result;
    OSIntrMode e;
    WMPortRecvCallback cb_Port;
    if (callback != ((void *)0) ) {
        MI_CpuClear8(&cb_Port, sizeof(WMPortRecvCallback));
        cb_Port.apiid = WM_APIID_PORT_RECV;
        cb_Port.errcode = WM_ERRCODE_SUCCESS;
        cb_Port.state = WM_STATECODE_PORT_INIT;
        cb_Port.port = port;
        cb_Port.recvBuf = ((void *)0) ;
        cb_Port.data = ((void *)0) ;
        cb_Port.length = 0;
        cb_Port.seqNo = 0xffff;
        cb_Port.arg = arg;
        cb_Port.aid = 0;
        native_fn_020081fc(cb_Port.macAddress);
    }
    e = native_fn_02007ff4();
    result = native_fn_020119d0();
    if (result != WM_ERRCODE_SUCCESS) {
        (void)native_fn_02008008(e);
        return result;
    }
    {
        WMArm9Buf * p = native_fn_020119c0();
        p->portCallbackTable[port] = callback;
        p->portCallbackArgument[port] = arg;
    }
    if (callback != ((void *)0) ) {
        cb_Port.connectedAidBitmap = native_fn_02011ee4();
        cb_Port.myAid = native_fn_02011eb4();
        (*callback)((void *)&cb_Port);
    }
    (void)native_fn_02008008(e);
    return WM_ERRCODE_SUCCESS;
}
