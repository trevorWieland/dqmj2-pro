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

typedef struct WMStartMPReq {
	u16 apiid;
	u16 rsv1;
	u32 * recvBuf;
	u32 recvBufSize;
	u32 * sendBuf;
	u32 sendBufSize;
	WMMPParam param;
	WMMPTmpParam tmpParam;
} WMStartMPReq;

typedef struct WMCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
} WMCallback;

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

typedef	struct {
	u16		code;
	u16		length;
} WlCmdHeader;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlParamSetCfm;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				buf[2];
} WlCmdCfm;

extern const u16 (*ctrdgi_fl_maxtime);

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

extern WMSPWork native_host_arm7_data_027f7884;

void native_host_arm7_arm_038073a4(void *ptr);

void *native_host_arm7_arm_038073f0(void);

void native_host_arm7_arm_027e637c(void);

void native_host_arm7_arm_027e7828(u16 aidBitmap);

void native_host_arm7_arm_027e06a0(void);

WMErrCode native_host_arm7_arm_027e8428(const WMMPParam *param, WMMPParam *old_param);

void native_host_arm7_main_027e4be0(OSMessage msg);

void native_host_arm7_arm_027e5bac(void);

WlParamSetCfm *native_host_arm7_arm_027e2700(u16 *buf, u16 mode);

static inline WMSPWork *WMSP_GetSystemWork(void)
{
    return &native_host_arm7_data_027f7884;
}

static inline WMStatus *WMSP_GetStatusStructure(void)
{
    return native_host_arm7_data_027f7884.status;
}

static inline int WMSP_GetMPSendBufferSize(int sendSize)
{
    return (sendSize + 31) & ~0x1f;
}

static inline int WMSP_GetMPOneReceiveBufferSizeParent(int recvSize, int nChildlen)
{
    return (int)((sizeof(WMmpRecvHeader) - sizeof(WMmpRecvData) + ((sizeof(WMmpRecvData) + recvSize - 2 + 2) * nChildlen) + 31) & ~0x1f);
}

static inline int WMSP_GetMPOneReceiveBufferSizeChild(int recvSize)
{
    return (int)((sizeof(WMMpRecvBuf) + recvSize - 4 + 31) & ~0x1f);
}

static void WMSP_SetMPTmpParameter(WMMPTmpParam *tmpParam)
{
    WMStatus *status = WMSP_GetStatusStructure();
    u32 mask = tmpParam->mask;
    if (status->state != WM_STATE_MP_PARENT && status->state != WM_STATE_MP_CHILD) {
        OSIntrMode e = native_host_arm7_arm_037fdd00();
        u16 maxFreq = (mask & 0x0004 ) ? tmpParam->maxFrequency : status->mp_maxFreq;
        if (!maxFreq) {
            maxFreq = 16 ;
        }
        u16 minFreq = (mask & 0x0001 ) ? tmpParam->minFrequency : status->mp_minFreq;
        if (!minFreq) {
            minFreq = 16 ;
        }
        if (minFreq > maxFreq) {
            minFreq = maxFreq;
        }
        u16 freq = (mask & 0x0002 ) ? tmpParam->frequency : status->mp_freq;
        if (!freq) {
            freq = 16 ;
        }
        if (freq > maxFreq) {
            freq = maxFreq;
        }
        status->mp_current_maxFreq = maxFreq;
        status->mp_current_minFreq = minFreq;
        status->mp_current_freq = freq;
        if (status->mp_count > maxFreq) {
            status->mp_count = maxFreq;
        }
        status->mp_current_defaultRetryCount = (mask & 0x0200 ) ? tmpParam->defaultRetryCount : status->mp_defaultRetryCount;
        status->mp_current_minPollBmpMode = (mask & 0x0400 ) ? tmpParam->minPollBmpMode : status->mp_minPollBmpMode;
        status->mp_current_singlePacketMode = (mask & 0x0800 ) ? tmpParam->singlePacketMode : status->mp_singlePacketMode;
        status->mp_current_ignoreFatalErrorMode = (mask & 0x1000 ) ? tmpParam->ignoreFatalErrorMode : status->mp_ignoreFatalErrorMode;
        native_host_arm7_arm_037fdd14(e);
    }
}
