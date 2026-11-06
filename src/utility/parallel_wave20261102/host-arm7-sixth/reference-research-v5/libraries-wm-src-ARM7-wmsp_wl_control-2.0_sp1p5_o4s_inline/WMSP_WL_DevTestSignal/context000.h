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
	u16				buf[2];
} WlCmdReq;

u16 *WMSP_WlRequest(u16 *request);

WlDevTestSignalCfm *WMSP_WL_DevTestSignal(u16 *buf, u16 control, u16 signal, u16 rate, u16 channel);
