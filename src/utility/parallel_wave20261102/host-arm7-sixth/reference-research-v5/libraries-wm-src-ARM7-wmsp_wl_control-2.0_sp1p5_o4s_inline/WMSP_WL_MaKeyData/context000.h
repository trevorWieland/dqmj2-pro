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

u16 *WMSP_WlRequest(u16 *request);

WlMaKeyDataCfm *WMSP_WL_MaKeyData(u16 *buf, u16 length, u16 wmHeader, u16 *keyDatap);
