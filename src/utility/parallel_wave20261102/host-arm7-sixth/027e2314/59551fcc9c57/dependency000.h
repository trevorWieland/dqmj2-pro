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
	u16				buf[2];
} WlCmdReq;

u16 *native_host_arm7_arm_027e01cc(u16 *request);

WlMaMpCfm *native_host_arm7_main_027e2314(u16 *buf, u16 resume, u16 retryLimit, u16 txop, u16 pollBitmap, u16 tmptt, u16 currTsf, u16 dataLength, u16 wmHeader, u16 *datap);
