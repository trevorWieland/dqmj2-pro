typedef unsigned short int u16;

typedef unsigned long u32;

void native_host_arm7_arm_037fdf9c(const void * srcp, void * destp, u32 size);

static inline void MI_CpuCopy16 (const void * src, void * dest, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	native_host_arm7_arm_037fdf9c(src, dest, size);
}

extern const u16 (*ctrdgi_fl_maxtime);

typedef	struct {
	u16		code;
	u16		length;
} WlCmdHeader;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				peerMacAdrs[3];
	u16				algorithm;
	u16				timeOut;
} WlMlmeAuthReq;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				statusCode;
	u16				peerMacAdrs[3];
	u16				algorithm;
} WlMlmeAuthCfm;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				buf[2];
} WlCmdReq;

typedef WlMlmeAuthReq WlMlmeAuthenticateReq;

typedef WlMlmeAuthCfm WlMlmeAuthenticateCfm;

u16 *native_host_arm7_arm_027e01cc(u16 *request);

WlMlmeAuthenticateCfm *native_host_arm7_main_027e1f4c(u16 *buf, u16 *peerMacAdrs, u16 algorithm, u16 timeOut);
