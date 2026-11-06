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
	u16				buf[2];
} WlCmdReq;

u16 *native_host_arm7_arm_027e01cc(u16 *request);

WlMaKeyDataCfm *native_host_arm7_main_027e22ac(u16 *buf, u16 length, u16 wmHeader, u16 *keyDatap);
