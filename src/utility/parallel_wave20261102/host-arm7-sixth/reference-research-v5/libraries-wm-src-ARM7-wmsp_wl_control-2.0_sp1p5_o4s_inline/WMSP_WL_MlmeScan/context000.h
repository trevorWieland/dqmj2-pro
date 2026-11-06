typedef unsigned char u8;

typedef unsigned short int u16;

typedef unsigned long u32;

void MIi_CpuCopy16(const void * srcp, void * destp, u32 size);

static inline void MI_CpuCopy16 (const void * src, void * dest, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	MIi_CpuCopy16(src, dest, size);
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
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				buf[2];
} WlCmdReq;

u16 *WMSP_WlRequest(u16 *request);

WlMlmeScanCfm *WMSP_WL_MlmeScan(u16 *buf, u32 bufSize, u16 *bssid, u16 ssidLength, u8 *ssid, u16 scanType, u8 *channelList, u16 maxChannelTime);
