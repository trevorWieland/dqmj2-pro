typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed long s32;
        typedef int BOOL;
void native_fn_02008c58(u32 data, void * destp, u32 size);
static inline void MI_CpuFillFast (void * dest, u32 data, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	native_fn_02008c58(data, dest, size);
}
static inline void MI_CpuClearFast (void * dest, u32 size)
{
	MI_CpuFillFast(dest, 0, size);
}
typedef enum WMPriorityLevel {
	WM_PRIORITY_URGENT = 0,
	WM_PRIORITY_HIGH,
	WM_PRIORITY_NORMAL,
	WM_PRIORITY_LOW
} WMPriorityLevel;
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
typedef enum WMState {
	WM_STATE_READY = 0,
	WM_STATE_STOP,
	WM_STATE_IDLE,
	WM_STATE_CLASS1,
	WM_STATE_TESTMODE,
	WM_STATE_SCAN,
	WM_STATE_CONNECT,
	WM_STATE_PARENT,
	WM_STATE_CHILD,
	WM_STATE_MP_PARENT,
	WM_STATE_MP_CHILD,
	WM_STATE_DCF_CHILD,
	WM_STATE_TESTMODE_RX,
	WM_STATE_MAX
} WMState;
typedef enum WMDataSharingState {
	WM_DS_STATE_READY = 0,
	WM_DS_STATE_START,
	WM_DS_STATE_PAUSING,
	WM_DS_STATE_PAUSED,
	WM_DS_STATE_RETRY_SEND,
	WM_DS_STATE_ERROR
} WMDataSharingState;
typedef void (*WMCallbackFunc) (void * arg);
typedef struct WMDataSet {
	u16 aidBitmap;
	u16 receivedBitmap;
	u16 data[508 / sizeof(u16)];
} WMDataSet;
typedef struct WMDataSharingInfo {
	WMDataSet ds[4 ];
	u16 seqNum[4 ];
	u16 writeIndex;
	u16 sendIndex;
	u16 readIndex;
	u16 aidBitmap;
	u16 dataLength;
	u16 stationNumber;
	u16 dataSetLength;
	u16 port;
	u16 doubleMode;
	u16 currentSeqNum;
	u16 state;
	u16 reserved[1];
} WMDataSharingInfo;
WMErrCode native_fn_02011f58(u16 port, WMCallbackFunc callback, void * arg);
WMErrCode native_fn_020130e8(WMCallbackFunc callback,
                               void * arg,
                               const u16 * sendData,
                               u16 sendDataSize, u16 destBitmap, u16 port, u16 prio);
WMErrCode native_main_02013460(WMDataSharingInfo * dsInfo, u16 port, u16 aidBitmap, u16 dataLength, BOOL doubleMode);
u16 native_fn_02011eb4(void);
u16 native_fn_02011ee4(void);
extern const u16 (*ctrdgi_fl_maxtime);
u8 native_fn_0201999c(u32 x);
WMErrCode native_fn_02011a34(s32 paramNum, ...);
extern void native_data_main_02013a44(void * callback);
extern void native_data_main_02013b1c(void * callback);
extern void native_data_main_02013c48(void * callback);
static inline u16 WmDataSharingGetNextIndex (u32 index)
{
    return (u16)((index + 1) % 4 );
}
WMErrCode native_main_02013460 (WMDataSharingInfo * dsInfo, u16 port, u16 aidBitmap, u16 dataLength, BOOL doubleMode)
{
    WMErrCode result;
    int aid;
    u16 connectedAIDs = 0x0001;
    result = native_fn_02011a34(2, WM_STATE_MP_PARENT, WM_STATE_MP_CHILD);
    if((result) != WM_ERRCODE_SUCCESS ) { return (result); } ;
    if (dsInfo == ((void *)0) ) {
        ((void) 0) ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    if (port >= 16 ) {
        ((void) 0) ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    if ((u32)dsInfo & 0x01f) {
        ((void) 0) ;
    }
    if (aidBitmap == 0) {
        ((void) 0) ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    aid = native_fn_02011eb4();
    if (aid == 0) {
        connectedAIDs = native_fn_02011ee4();
    }
    MI_CpuClearFast(dsInfo, sizeof(WMDataSharingInfo));
    dsInfo->writeIndex = 0;
    dsInfo->sendIndex = 0;
    dsInfo->readIndex = 0;
    dsInfo->dataLength = dataLength;
    dsInfo->port = port;
    dsInfo->aidBitmap = 0;
    dsInfo->doubleMode = (u16)((doubleMode) ? 1 : 0 );
    aidBitmap |= (1 << aid);
    dsInfo->aidBitmap = aidBitmap;
    {
        u16 count = native_fn_0201999c(aidBitmap);
        dsInfo->stationNumber = count;
        dsInfo->dataSetLength = (u16)(dataLength * count);
        if (dsInfo->dataSetLength > 508 ) {
            dsInfo->aidBitmap = 0;
            ((void) 0)
                       ;
            return WM_ERRCODE_INVALID_PARAM;
        }
        dsInfo->dataSetLength += 4;
    }
    dsInfo->state = WM_DS_STATE_START;
    if (aid == 0) {
        int i;
        for (i = 0; i < 4 ; i++) {
            dsInfo->ds[i].aidBitmap = (u16)(dsInfo->aidBitmap & (connectedAIDs | 0x0001));
        }
        (void)native_fn_02011f58(port, native_data_main_02013b1c, (void *)dsInfo);
        for (i = 0; i < ((dsInfo->doubleMode == 1 ) ? 2 : 1); i++) {
            int res;
            dsInfo->writeIndex = WmDataSharingGetNextIndex(dsInfo->writeIndex);
            res =
                native_fn_020130e8(native_data_main_02013a44, dsInfo, (u16 *)&dsInfo->ds[i],
                                     dsInfo->dataSetLength,
                                     (u16)(dsInfo->aidBitmap & connectedAIDs), dsInfo->port,
                                     WM_PRIORITY_HIGH);
            if (res == WM_ERRCODE_NO_CHILD) {
                dsInfo->seqNum[i] = 0xffff;
                dsInfo->sendIndex = WmDataSharingGetNextIndex(dsInfo->sendIndex);
            } else {
                if (res != WM_ERRCODE_SUCCESS && res != WM_ERRCODE_OPERATING) {
                    ((void) 0) ;
                    dsInfo->state = WM_DS_STATE_ERROR;
                    return WM_ERRCODE_FAILED;
                }
            }
        }
    } else {
        dsInfo->sendIndex = (u16)(4 - 1);
        (void)native_fn_02011f58(port, native_data_main_02013c48, (void *)dsInfo);
    }
    return WM_ERRCODE_SUCCESS;
}
void native_data_main_02013a44 (void * callback);
void native_data_main_02013b1c (void * callback);
void native_data_main_02013c48 (void * callback);
