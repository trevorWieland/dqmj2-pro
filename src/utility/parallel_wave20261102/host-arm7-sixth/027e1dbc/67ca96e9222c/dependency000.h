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
	u16				pwrMgtMode;
	u16				wakeUp;
	u16				recieveDtims;
} WlMlmePowerMgtReq;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMlmePowerMgtCfm;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				buf[2];
} WlCmdReq;

typedef WlMlmePowerMgtReq WlMlmePowerManagementReq;

typedef WlMlmePowerMgtCfm WlMlmePowerManagementCfm;

u16 *native_host_arm7_arm_027e01cc(u16 *request);

WlMlmePowerManagementCfm *native_host_arm7_main_027e1dbc(u16 *buf, u16 pwrMgtMode, u16 wakeUp, u16 recieveDtims);
