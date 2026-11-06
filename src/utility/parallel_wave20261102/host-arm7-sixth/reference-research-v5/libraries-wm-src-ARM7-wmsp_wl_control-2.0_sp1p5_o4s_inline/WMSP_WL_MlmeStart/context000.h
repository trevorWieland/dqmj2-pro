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

extern const u16 (*ctrdgi_fl_maxtime);

typedef	struct {
	u16		code;
	u16		length;
} WlCmdHeader;

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
	u16				buf[2];
} WlCmdReq;

u16 *WMSP_WlRequest(u16 *request);

WlMlmeStartCfm *WMSP_WL_MlmeStart(u16 *buf, u16 ssidLength, u8 *ssid, u16 beaconPeriod, u16 dtimPeriod, u16 channel, u16 basicRateSet, u16 supportRateSet, u16 gameInfoLength, WMGameInfo *gameInfo);
