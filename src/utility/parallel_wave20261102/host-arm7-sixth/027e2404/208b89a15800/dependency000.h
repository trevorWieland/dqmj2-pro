typedef unsigned char u8;

typedef unsigned short int u16;

typedef unsigned long u32;

extern const u16 (*ctrdgi_fl_maxtime);

typedef	struct {
	u16		code;
	u16		length;
} WlCmdHeader;

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
	WlCmdHeader		header;
	u16				resultCode;
} WlParamSetCfm;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				buf[2];
} WlCmdReq;

u16 *native_host_arm7_arm_027e01cc(u16 *request);

WlParamSetCfm *native_host_arm7_main_027e2404(WlParamSetAllReq *req);
