typedef unsigned short int u16;
typedef unsigned long u32;
typedef int BOOL;
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
WMErrCode native_main_02012774(void * wmSysBuf, WMCallbackFunc callback, u16 dmaNo, BOOL blink);
WMErrCode native_fn_0201278c(void * wmSysBuf, WMCallbackFunc callback, u16 dmaNo, u32 miscFlags);
extern const u16 (*ctrdgi_fl_maxtime);
WMErrCode native_fn_0201278c (void * wmSysBuf, WMCallbackFunc callback, u16 dmaNo, u32 miscFlags);
