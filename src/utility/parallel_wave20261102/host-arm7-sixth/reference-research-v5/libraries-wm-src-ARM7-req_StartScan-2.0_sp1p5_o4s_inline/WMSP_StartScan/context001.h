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

typedef struct WMStartScanReq {
	u16 apiid;
	u16 channel;
	WMBssDesc * scanBuf;
	u16 maxChannelTime;
	u8 bssid[6 ];
} WMStartScanReq, WMstartScanReq;

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

static inline void MI_WriteByte (void * address, u8 value)
    {
        *(u8 *)address = value;
    }

extern const u16 (*ctrdgi_fl_maxtime);

typedef	struct {
	u16		code;
	u16		length;
} WlCmdHeader;

typedef	struct {
	u16		length;
	u16		rssi;
	u16		bssid[3];
	u16		ssidLength;
	u8		ssid[32];
	u16		capaInfo;
	struct {
		u16	basic;
		u16	support;
	} rateSet;
	u16		beaconPeriod;
	u16		dtimPeriod;
	u16		channel;
	u16		cfpPeriod;
	u16		cfpMaxDuration;
	u16		gameInfoLength;
	u16		otherElementCount;
	union _element {
		u8		gameInfo[4];
		u8		otherElement[4];
	};
} WlBssDesc;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMlmePowerMgtCfm;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				bssid[3];
	u16				ssidLength;
	u8				ssid[32];
	u16				scanType;
	u8				channelList[16];
	u16				maxChannelTime;
	u16				bssidMaskCount;
	u16				bssidMask[3];
} WlMlmeScanReq;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				foundMap;
	u16				bssDescCount;
	WlBssDesc		bssDescList[1];
} WlMlmeScanCfm;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlDevClass1Cfm;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				state;
} WlDevGetStateCfm;

typedef struct WMSPWork {
    OSMessageQueue toWLmsgQ;
    OSMessage toWLmsg[2 ];
    OSMessageQueue fromWLmsgQ;
    OSMessage fromWLmsg[4 ];
    OSMessageQueue confirmQ;
    OSMessage confirm[4 ];
    OSMessageQueue requestQ;
    OSMessage request[32 ];
    u32 requestStack[4096 / sizeof(u32)];
    u32 indicateStack[1024 / sizeof(u32)];
    OSMutex fifoExclusive;
    u32 dmaNo;
    OSArenaId arenaId;
    OSHeapHandle heapHandle;
    WMArm7Buf *wm7buf;
    WMStatus *status;
    u8 rssiHistory[32 ];
    u32 rssiIndex;
    u32 indPrio_high;
    u32 wlPrio_high;
    u32 reqPrio_high;
    u32 indPrio_low;
    u32 wlPrio_low;
    u32 reqPrio_low;
} WMSPWork;

extern WMSPWork wmspW;

typedef WlMlmePowerMgtCfm WlMlmePowerManagementCfm;

typedef WlDevGetStateCfm WlDevGetStationStateCfm;

void WMSP_ReturnResult2Wm9(void *ptr);

void *WMSP_GetBuffer4Callback2Wm9(void);

BOOL WMSP_SetAllParams(u16 wmApiID, u16 *buf);

u16 WMSP_GetLinkLevel(u32 rssi);

void WMSP_StartScan(OSMessage msg);

WlMlmePowerManagementCfm *WMSP_WL_MlmePowerManagement(u16 *buf, u16 pwrMgtMode, u16 wakeUp, u16 recieveDtims);

WlMlmeScanCfm *WMSP_WL_MlmeScan(u16 *buf, u32 bufSize, u16 *bssid, u16 ssidLength, u8 *ssid, u16 scanType, u8 *channelList, u16 maxChannelTime);

WlDevClass1Cfm *WMSP_WL_DevClass1(u16 *buf);

WlDevGetStationStateCfm *WMSP_WL_DevGetStationState(u16 *buf);

static inline WMSPWork *WMSP_GetSystemWork(void)
{
    return &wmspW;
}

static inline WMStatus *WMSP_GetStatusStructure(void)
{
    return wmspW.status;
}

static inline u8 WMSP_GetRssi8(u8 rssi)
{
    if (rssi & 0x0002) {
        return (u8)(rssi >> 2);
    }
    return (u8)((rssi >> 2) + 25);
}

static inline void WMSP_AddRssiToRandomPool(u8 rssi8)
{
    u32 rssi_pool = (u32)(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->wm_rssi_pool << 1);
    rssi_pool ^= rssi8;
    rssi_pool ^= rssi_pool >> 16;
    ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->wm_rssi_pool = (u16)rssi_pool;
}

enum {
    SCAN_CHANNEL_MAX = 16
};

static void WmspError(u16 wlCommand, u16 wlResult, BOOL exFlag);
