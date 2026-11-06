

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				staMacAdrs[3];
	u16				retryLimit;
	u16				enableChannel;
	u16				channel;
	u16				mode;
	u16				rate;
	u16				wepMode;
	u16				wepKeyId;
	u16				beaconType;
	u16				probeRes;
	u16				beaconLostTh;
	u16				activeZoneTime;
	u8				ssidMask[32];
	u16				preambleType;
	u16				authAlgo;
} WlParamGetAllCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				staMacAdrs[3];
} WlParamGetMacAdrsCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				retryLimit;
} WlParamGetRetryLimitCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				enableChannel;
	u16				channel;
} WlParamGetEnableChannelCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				mode;
} WlParamGetModeCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				rate;
} WlParamGetRateCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				wepMode;
} WlParamGetWepModeCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				wepKeyId;
} WlParamGetWepKeyIdCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				beaconType;
} WlParamGetBeaconTypeCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				probe;
} WlParamGetProbeResCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				beaconLostTh;
} WlParamGetBeaconLostThCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				activeZoneTime;
} WlParamGetActiveZoneCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u8				mask[32];
} WlParamGetSsidMaskCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				type;
} WlParamGetPreambleTypeCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				type;
} WlParamGetAuthAlgoCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				ccaMode;
	u16				edThreshold;
	u16				agcLimit;
} WlParamGetCCAModeEDThCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				count;
} WlParamGetMaxConnCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				mainAntenna;
} WlParamGetMainAntennaCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				diversity;
	u16				useAntenna;
} WlParamGetDiversityCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				enableMessage;
} WlParamGetBeaconSendRecvIndCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				mode;
} WlParamGetNullKeyModeCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				bssid[3];
} WlParamGetBssidCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				ssidLength;
	u8				ssid[32];
} WlParamGetSsidCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				beaconPeriod;
} WlParamGetBeaconPeriodCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				dtimPeriond;
} WlParamGetDtimPeriodCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				listenInterval;
} WlParamGetIntervalCfm;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				gameInfoLength;
	u16				gameInfo[1];
} WlParamGetGameInfoCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
} WlDevShutdownReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlDevShutdownCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
} WlDevIdleReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlDevIdleCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
} WlDevClass1Req;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlDevClass1Cfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
} WlDevRebootReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlDevRebootCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
} WlDevClrInfoReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlDevClrInfoCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
} WlDevGetVerInfoReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u8				wlVersion[8];
	u16				macVersion;
	u16				bbpVersion[2];
	u16				rfVersion;
} WlDevGetVerInfoCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
} WlDevGetInfoReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				rsv1;
	WlCounter		counter;
} WlDevGetInfoCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
} WlDevGetStateReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				state;
} WlDevGetStateCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				control;
	u16				signal;
	u16				rate;
	u16				channel;
} WlDevTestSignalReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlDevTestSignalCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				control;
	u16				channel;
} WlDevTestRxReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlDevTestRxCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				buf[2];
} WlCmdReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				buf[2];
} WlCmdCfm;


typedef struct {
	u16			state;
	u16			aid;
	u16			macAdrs[3];
	u16			rssi;
	u16			capaInfo;
	u16			authSeed;
	u16			supRateSet;
	u16			rsv;
	u16			lastSeqCtrl;
	u16			frameCount;
	u16			lifeTime;
	u16			maxLifeTime;
} WlStaElement;


typedef	struct {
	u16	rssi;
	u16	channel;
	u16	capaInfo;
	u16	bssid[3];
	u16	ssidLength;
	u8	ssid[32];
	u16	beaconInterval;
	u16	lifeTime;
} WlApElement;


extern const u16 (*ctrdgi_fl_maxtime);


typedef struct {
    u16 NextId;
    u16 Flag;
    void (*pTaskFunc)(void);
} TASK_TBL, *LPTASK_TBL;


typedef struct {
    u16 EnQ[4 ];
    u16 DeQ[4 ];
    vu16 NextPri;
