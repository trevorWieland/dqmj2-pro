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
	u16				buf[2];
} WlCmdReq;

typedef WlMlmeMeasChanReq WlMlmeMeasureChannelReq;

typedef WlMlmeMeasChanCfm WlMlmeMeasureChannelCfm;

u16 *WMSP_WlRequest(u16 *request);

WlMlmeMeasureChannelCfm *WMSP_WL_MlmeMeasureChannel(u16 *buf, u16 ccaMode, u16 edThreshold, u16 measureTime, u8 *channelList);
