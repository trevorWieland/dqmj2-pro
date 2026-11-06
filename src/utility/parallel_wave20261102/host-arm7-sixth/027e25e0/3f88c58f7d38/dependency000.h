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
	u16				tableNumber;
	u16				camLifeTime;
	u16				frameLifeTime;
} WlParamSetLifeTimeReq;

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

WlParamSetCfm *native_host_arm7_main_027e25e0(u16 *buf, u16 tableNumber, u16 camLifeTime, u16 frameLifeTime);
