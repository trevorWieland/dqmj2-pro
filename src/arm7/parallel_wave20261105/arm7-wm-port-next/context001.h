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

typedef struct WMPortSendCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
	u16 state;
	u16 port;
	u16 destBitmap;
	u16 restBitmap;
	u16 sentBitmap;
	u16 rsv;
	const u16 * data;
	union {
		u16 size;
		u16 length;
	};
	u16 seqNo;
	WMCallbackFunc callback;
	void * arg;
	u16 maxSendDataSize;
	u16 maxRecvDataSize;
} WMPortSendCallback;

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

static s32 GX_GetVCount(void);

static inline s32 GX_GetVCount ()
{
	return (*( REGType16v *) (0x04000000 + 0x006)) ;
}

extern const u16 (*ctrdgi_fl_maxtime);

u8 native_host_arm7_arm_03803830(u32 x);

typedef	struct {
	u16		code;
	u16		length;
} WlCmdHeader;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMaKeyDataCfm;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMaMpCfm;

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

void native_host_arm7_main_027e692c(u16 pollBitmap);

void native_host_arm7_main_027e72d4(u16 pollBitmap);

void native_host_arm7_main_027e6434(void);

void native_host_arm7_main_027e637c(void);

int native_host_arm7_main_027e73c4(u32 childBitmap, u16 priority, u16 port, u32 destBitmap, const u16 *sendData, u16 sendDataSize, WMCallbackFunc callback, void *arg);

BOOL native_host_arm7_main_027e74f8(BOOL timeout, u16 pollBitmap);

void native_host_arm7_main_027e7828(u16 aidBitmap);

void native_host_arm7_main_027e7a1c(u16 aid, u16 wmHeader, u16 *data, u16 length, WMMpRecvBuf *recvBuf);

void native_host_arm7_arm_027e1a54(void);

WlMaKeyDataCfm *native_host_arm7_arm_027e22ac(u16 *buf, u16 length, u16 wmHeader, u16 *keyDatap);

WlMaMpCfm *native_host_arm7_arm_027e2314(u16 *buf, u16 resume, u16 retryLimit, u16 txop, u16 pollBitmap, u16 tmptt, u16 currTsf, u16 dataLength, u16 wmHeader, u16 *datap);

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

static int WmspMakePortPacket(u32 pollBitmap, u32 childBitmap, u32 mpReadyBitmap, u16 *wmHeader, u32 *destBitmap, u32 *dataLength);

u16 native_host_arm7_main_027e7c20(u32 dataLength, u32 txop, u32 pollBitmap, u32 targetVCount);

void native_host_arm7_main_027e637c(void)
{
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    u16 i;
    native_host_arm7_arm_037fc888(&status->sendQueueMutex);
    MI_CpuClear16(status->sendQueueData, sizeof(status->sendQueueData));
    for (i = 0; i < 32 - 1; i++) {
        status->sendQueueData[i].next = (u16)(i + 1);
    }
    status->sendQueueData[i].next = ((u16)0xffff) ;
    status->sendQueueFreeList.head = 0;
    status->sendQueueFreeList.tail = i;
    for (i = 0; i < 4 ; i++) {
        status->readyQueue[i].head = ((u16)0xffff) ;
        status->readyQueue[i].tail = ((u16)0xffff) ;
        status->sendQueue[i].head = ((u16)0xffff) ;
        status->sendQueue[i].tail = ((u16)0xffff) ;
    }
    native_host_arm7_arm_037fc90c(&status->sendQueueMutex);
}

void native_host_arm7_main_027e6434(void)
{
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    WlMaKeyDataCfm *wlResult;
    u32 destBitmap;
    u32 dataLength;
    u16 wmHeader;
    if (status->child_bitmap == 0) {
        ((void)0) ;
        return;
    }
    status->mp_setDataFlag = 1 ;
    wmHeader = 0;
    if (WmspMakePortPacket(0x0001U, 0x0001U, 0x0001U, &wmHeader, &destBitmap, &dataLength) == WM_ERRCODE_FAILED) {
        ((void)0) ;
        status->mp_setDataFlag = 0 ;
        return;
    }
    if (status->VSyncFlag == 1 ) {
        wmHeader |= 0x8000 ;
    }
    ((void)0) ;
    wlResult = native_host_arm7_arm_027e22ac((u16 *)wlBuf, (u16)dataLength, wmHeader, (u16 *)status->mp_sendBuf);
    if (wlResult->resultCode != 0x00 ) {
        ((void)0) ;
        if (wlResult->resultCode != 0x08 ) {
            status->mp_setDataFlag = 0 ;
        }
    }
}
