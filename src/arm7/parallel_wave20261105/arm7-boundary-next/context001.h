typedef struct WMMpRecvHeader {
	u16 bitmap;
	u16 errBitmap;
	u16 count;
	u16 length;
	u16 txCount;
	WMMpRecvData data[1];
} WMMpRecvHeader, WMmpRecvHeader;

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

typedef struct WMStartParentCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
	u16 state;
	u8 macAddress[6 ];
	u16 aid;
	u16 reason;
	u8 ssid[24 ];
	u16 parentSize;
	u16 childSize;
} WMStartParentCallback, WMstartParentCallback;

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

typedef struct WMStartDCFCallback {
	u16 apiid;
	u16 errcode;
	u16 state;
	u8 reserved[2];
	WMDcfRecvBuf * recvBuf;
} WMStartDCFCallback, WMstartDCFCallback;

typedef struct WMIndCallback {
	u16 apiid;
	u16 errcode;
	u16 state;
	u16 reason;
} WMIndCallback, WMindCallback;

typedef struct WMBeaconRecvIndCallback {
	u16 apiid;
	u16 errcode;
	u16 state;
	u16 tgid;
	u16 wmstate;
	u16 gameInfoLength;
	WMGameInfo gameInfo;
} WMBeaconRecvIndCallback;

extern const u16 (*ctrdgi_fl_maxtime);

typedef	struct {
	u16			frameId;
	u8			rsv1[4];
	u16			length;
	u16			status;
	u16			rsvm2;
	u16			timeStamp;
	u8			rate;
	u8			rssi;
	u32			rsvm3;
	u8			rsv4[4];
	u16			destAdrs[3];
	u16			srcAdrs[3];
	u8			rsv5[8];
	u8			data[4];
} WlRxFrame;

typedef	struct {
	u8			rsv1[6];
	u16			length;
	u16			txKeySts;
	u16			ackTimeStamp;
	u16			timeStamp;
	u8			rate;
	u8			rssi;
	u8			rsv3[4];
	u8			rsv4[4];
	u16			destAdrs[3];
	u16			srcAdrs[3];
	u8			rsv5[6];
	u16			seqCtrl;
	u16			txop;
	u16			bitmap;
	u16			data[1];
} WlRxMpFrame;

typedef	struct {
	u8			rsv1[6];
	u16			length;
	u16			txKeySts;
	u16			rsv3;
	u16			timeStamp;
	u8			rate;
	u8			rssi;
	u8			rsv4[4];
	u8			rsv5[4];
	u16			destAdrs[3];
	u16			srcAdrs[3];
	u8			rsv6[6];
	u16			seqCtrl;
	u16			tmptt;
	u16			bitmap;
} WlRxMpAckFrame;

typedef	struct {
	u16			length;
	u8			rate;
	u8			rssi;
	u16			aid;
	u16			noResponse;
	u8			cdata[4];
} WlMpKeyData;

typedef	struct {
	u16			bitmap;
	u16			errBitmap;
	u16			count;
	u16			length;
	u16			txCount;
	WlMpKeyData	data[1];
} WlMpKey;

typedef	struct {
	u16		code;
	u16		length;
} WlCmdHeader;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				peerMacAdrs[3];
	u16				reasonCode;
} WlMlmeDeAuthInd;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				peerMacAdrs[3];
	u16				aid;
	u16				ssidLength;
	u8				ssid[32];
} WlMlmeAssInd;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				reserved1[3];
	u16				gameInfoLength;
	u16				reserved2[3];
	u8				rate;
	u8				rssi;
	u16				reserved3[4];
	u16				reserved4[3];
	u16				srcMacAdrs[3];
	u16				reserved5[4];
	u16				gameInfo[1];
} WlMlmeBeaconRecvInd;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	WlRxFrame		frame;
} WlMaDataInd;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	WlRxMpFrame		frame;
} WlMaMpInd;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	WlMpKey			mpKey;
} WlMaMpEndInd;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	WlRxMpAckFrame	ack;
} WlMaMpAckInd;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				errCode;
} WlMaFatalErrInd;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				buf[2];
} WlCmdReq;
