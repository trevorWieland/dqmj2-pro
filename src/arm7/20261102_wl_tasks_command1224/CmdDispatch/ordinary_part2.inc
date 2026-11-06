} WlMlmeAssReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				statusCode;
	u16				aid;
} WlMlmeAssCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				newApMacAdrs[3];
	u16				listenInterval;
	u16				timeOut;
} WlMlmeReAssReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				statusCode;
	u16				aid;
} WlMlmeReAssCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				peerMacAdrs[3];
	u16				reasonCode;
} WlMlmeDisAssReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMlmeDisAssCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				ssidLength;
	u8				ssid[32];
	u16				beaconPeriod;
	u16				dtimPeriod;
	u16				channel;
	u16				basicRateSet;
	u16				supportRateSet;
	u16				gameInfoLength;
	u8				gameInfo[2];
} WlMlmeStartReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMlmeStartCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				rsv;
	u16				ccaMode;
	u16				edThreshold;
	u16				measureTime;
	u8				channelList[16];
} WlMlmeMeasChanReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				reserved;
	u16				ccaBusyInfo[16];
} WlMlmeMeasChanCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	WlTxFrame		frame;
} WlMaDataReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				txStatus;
} WlMaDataCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				length;
	u16				wmHeader;
	u16*			keyDatap;
} WlMaKeyDataReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMaKeyDataCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				resume;
	u16				retryLimit;
	u16				txop;
	u16				pollBitmap;
	u16				tmptt;
	u16				currTsf;
	u16				dataLength;
	u16				wmHeader;
	u16*			datap;
} WlMaMpReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMaMpCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	WlTestFrame		frame;
} WlMaTestDataReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMaTestDataCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				flag;
} WlMaClrDataReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMaClrDataCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	WlMpKey			mpKey;
} WlMaMpEndInd;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				staMacAdrs[3];
	u16				retryLimit;
	u16				enableChannel;
	u16				rsv;
	u16				mode;
	u16				rate;
	u16				wepMode;
	u16				wepKeyId;
	u16				wepKey[4][10];
	u16				beaconType;
	u16				probeRes;
	u16				beaconLostTh;
	u16				activeZoneTime;
	u8				ssidMask[32];
	u16				preambleType;
	u16				authAlgo;
} WlParamSetAllReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				staMacAdrs[3];
} WlParamSetMacAdrsReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				retryLimit;
} WlParamSetRetryLimitReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				enableChannel;
} WlParamSetEnableChannelReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				mode;
} WlParamSetModeReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				rate;
} WlParamSetRateReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				wepMode;
} WlParamSetWepModeReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				wepKeyId;
} WlParamSetWepKeyIdReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				wepKey[4][10];
} WlParamSetWepKeyReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				beaconType;
} WlParamSetBeaconTypeReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				probeRes;
} WlParamSetProbeResReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				beaconLostTh;
} WlParamSetBeaconLostThReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				activeZoneTime;
} WlParamSetActiveZoneReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u8				mask[32];
} WlParamSetSsidMaskReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				type;
} WlParamSetPreambleTypeReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				type;
} WlParamSetAuthAlgoReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				ccaMode;
	u16				edThreshold;
	u16				agcLimit;
} WlParamSetCCAModeEDThReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				tableNumber;
	u16				camLifeTime;
	u16				frameLifeTime;
} WlParamSetLifeTimeReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				count;
} WlParamSetMaxConnReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				mainAntenna;
} WlParamSetMainAntennaReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				diversity;
	u16				useAntenna;
} WlParamSetDiversityReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				enableMessage;
} WlParamSetBeaconSendRecvIndReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				mode;
} WlParamSetNullKeyModeReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				bssid[3];
} WlParamSetBssidReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				ssidLength;
	u8				ssid[32];
} WlParamSetSsidReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				beaconPeriod;
} WlParamSetBeaconPeriodReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				dtimPeriod;
} WlParamSetDtimPeriodReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				listenInterval;
} WlParamSetIntervalReq;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				gameInfoLength;
	u16				gameInfo[1];
} WlParamSetGameInfoReq;


typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlParamSetCfm;


typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
} WlParamGetReq;
