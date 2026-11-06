typedef struct WMStartParentCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
	u16 state;
	u8 macAddress[6 ];
	u16 aid;
	u16 reason;
	u8 ssid[24 ];
	u16 parentSize;
	u16 childSize;
} WMStartParentCallback, WMstartParentCallback;
typedef struct WMStartConnectCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
	u16 state;
	u16 aid;
	u16 reason;
	u16 wlStatus;
	u8 macAddress[6 ];
	u16 parentSize;
	u16 childSize;
} WMStartConnectCallback, WMstartConnectCallback;
typedef struct WMStartMPCallback {
	u16 apiid;
	u16 errcode;
	u16 state;
	u8 reserved[2];
	WMMpRecvBuf * recvBuf;
	u16 timeStamp;
	u16 rate_rssi;
	u8 destAdrs[6];
	u8 srcAdrs[6];
	u16 seqNum;
	u16 tmptt;
	u16 pollbmp;
	u16 reserved2;
} WMStartMPCallback, WMstartMPCallback;
typedef struct WMPortSendCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
	u16 state;
	u16 port;
	u16 destBitmap;
	u16 restBitmap;
	u16 sentBitmap;
	u16 rsv;
	const u16 * data;
	union {
		u16 size;
		u16 length;
	};
	u16 seqNo;
	WMCallbackFunc callback;
	void * arg;
	u16 maxSendDataSize;
	u16 maxRecvDataSize;
} WMPortSendCallback;
typedef struct WMPortRecvCallback {
	u16 apiid;
	u16 errcode;
	u16 state;
	u16 port;
	WMMpRecvBuf * recvBuf;
	u16 * data;
	u16 length;
	u16 aid;
	u8 macAddress[6 ];
	u16 seqNo;
	void * arg;
	u16 myAid;
	u16 connectedAidBitmap;
	u8 ssid[24 ];
	u16 reason;
	u16 rsv;
	u16 maxSendDataSize;
	u16 maxRecvDataSize;
} WMPortRecvCallback;
WMErrCode native_fn_020117c4(void);
typedef enum {
	PXI_FIFO_TAG_EX = 0,
	PXI_FIFO_TAG_USER_0,
	PXI_FIFO_TAG_USER_1,
	PXI_FIFO_TAG_SYSTEM,
	PXI_FIFO_TAG_NVRAM,
	PXI_FIFO_TAG_RTC,
	PXI_FIFO_TAG_TOUCHPANEL,
	PXI_FIFO_TAG_SOUND,
	PXI_FIFO_TAG_PM,
	PXI_FIFO_TAG_MIC,
	PXI_FIFO_TAG_WM,
	PXI_FIFO_TAG_FS,
	PXI_FIFO_TAG_OS,
	PXI_FIFO_TAG_CTRDG,
	PXI_FIFO_TAG_CARD,
	PXI_FIFO_TAG_WVR,
	PXI_FIFO_TAG_CTRDG_Ex,
	PXI_FIFO_TAG_CTRDG_PHI,
	PXI_MAX_FIFO_TAG = 32
} PXIFifoTag;
extern const u16 (*ctrdgi_fl_maxtime);
void native_main_02011ac8(PXIFifoTag tag, u32 fifo_buf_adr, BOOL err);
void native_fn_02011e74(void);
WMErrCode native_fn_020117c4 (void);
typedef struct {
u16 field_0000;
unsigned char padding_0002[2];
WMArm9Buf * field_0004;
OSMessageQueue field_0008;
OSMessage field_0028[10 ];
WMPortRecvCallback field_0050;
unsigned char padding_0094[12];
__attribute__ ((aligned(32))) u32 field_00a0[10 ][256 / sizeof(u32)];
} NativeStorage_020e5d80;
extern NativeStorage_020e5d80 native_data_main_020e5d80;
void native_fn_02011e74 (void);
static inline void MI_CpuFill16 (void * dest, u16 data, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	native_fn_02008be0(data, dest, size);
}
static inline void MI_CpuCopy16 (const void * src, void * dest, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	native_fn_02008bf8(src, dest, size);
}
static inline void MI_CpuClear16 (void * dest, u32 size)
{
	MI_CpuFill16(dest, 0, size);
}
static inline void MI_CpuClear8 (void * dest, u32 size)
{
	native_fn_02008d78(dest, 0, size);
}
