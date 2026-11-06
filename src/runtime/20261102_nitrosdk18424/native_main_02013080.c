typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
void native_fn_02008c14(u32 data, void * destp, u32 size);
static inline void MI_CpuFill32 (void * dest, u32 data, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	native_fn_02008c14(data, dest, size);
}
static inline void MI_CpuClear32 (void * dest, u32 size)
{
	MI_CpuFill32(dest, 0, size);
}
typedef enum WMErrCode {
	WM_ERRCODE_SUCCESS               = 0,
	WM_ERRCODE_FAILED                = 1,
	WM_ERRCODE_OPERATING             = 2,
	WM_ERRCODE_ILLEGAL_STATE         = 3,
	WM_ERRCODE_WM_DISABLE            = 4,
	WM_ERRCODE_NO_KEYSET             = 5,
	WM_ERRCODE_NO_DATASET            = 5,
	WM_ERRCODE_INVALID_PARAM         = 6,
	WM_ERRCODE_NO_CHILD              = 7,
	WM_ERRCODE_FIFO_ERROR            = 8,
	WM_ERRCODE_TIMEOUT               = 9,
	WM_ERRCODE_SEND_QUEUE_FULL       = 10,
	WM_ERRCODE_NO_ENTRY              = 11,
	WM_ERRCODE_OVER_MAX_ENTRY        = 12,
	WM_ERRCODE_INVALID_POLLBITMAP    = 13,
	WM_ERRCODE_NO_DATA               = 14,
	WM_ERRCODE_SEND_FAILED           = 15,
	WM_ERRCODE_DCF_TEST,
	WM_ERRCODE_WL_INVALID_PARAM,
	WM_ERRCODE_WL_LENGTH_ERR,
	WM_ERRCODE_FLASH_ERROR,
	WM_ERRCODE_MAX
} WMErrCode;
typedef void (*WMCallbackFunc) (void * arg);
typedef struct WMMPTmpParam {
	u32 mask;
	u16 minFrequency;
	u16 frequency;
	u16 maxFrequency;
	u16 defaultRetryCount;
	u8 minPollBmpMode;
	u8 singlePacketMode;
	u8 ignoreFatalErrorMode;
	u8 reserved[1];
} WMMPTmpParam;
WMErrCode native_main_02013080(WMCallbackFunc callback, u16 * recvBuf, u16 recvBufSize, u16 * sendBuf, u16 sendBufSize, u16 mpFreq);
extern const u16 (*ctrdgi_fl_maxtime);
WMErrCode native_fn_02012e6c(WMCallbackFunc callback, u16 * recvBuf, u16 recvBufSize, u16 * sendBuf, u16 sendBufSize, WMMPTmpParam * tmpParam);
WMErrCode native_fn_02012e6c (WMCallbackFunc callback, u16 * recvBuf, u16 recvBufSize, u16 * sendBuf, u16 sendBufSize, WMMPTmpParam * tmpParam);
WMErrCode native_main_02013080 (WMCallbackFunc callback, u16 * recvBuf, u16 recvBufSize, u16 * sendBuf, u16 sendBufSize, u16 mpFreq)
{
    WMMPTmpParam tmpParam;
    MI_CpuClear32(&tmpParam, sizeof(tmpParam));
    tmpParam.mask = 0x0002 | 0x0001 ;
    tmpParam.minFrequency = mpFreq;
    tmpParam.frequency = mpFreq;
    return native_fn_02012e6c(callback, recvBuf, recvBufSize, sendBuf, sendBufSize, &tmpParam);
}
