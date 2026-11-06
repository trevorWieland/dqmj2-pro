typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed long s32;
        typedef int BOOL;
void native_fn_02008bf8(const void * srcp, void * destp, u32 size);
static inline void MI_CpuCopy16 (const void * src, void * dest, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	native_fn_02008bf8(src, dest, size);
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
WMErrCode native_fn_020130e8(WMCallbackFunc callback,
                               void * arg,
                               const u16 * sendData,
                               u16 sendDataSize, u16 destBitmap, u16 port, u16 prio);
WMErrCode native_main_020136fc(WMDataSharingInfo * dsInfo, const u16 * sendData, WMDataSet * receiveData);
u16 native_fn_02011eb4(void);
u16 native_fn_02011ee4(void);
extern const u16 (*ctrdgi_fl_maxtime);
WMErrCode native_fn_02011a34(s32 paramNum, ...);
extern void native_data_main_02013a44(void * callback);
extern void native_fn_02013d3c(WMDataSharingInfo * dsInfo, u16 aid, u16 * data);
extern void native_fn_02013e08(WMDataSharingInfo * dsInfo, BOOL delayed);
static inline u16 WmDataSharingGetNextIndex (u32 index)
{
    return (u16)((index + 1) % 4 );
}
static inline u16 WmDataSharingGetPrevIndex (u32 index)
{
    return (u16)((index + 4 - 1) % 4 );
}
WMErrCode native_main_020136fc (WMDataSharingInfo * dsInfo, const u16 * sendData, WMDataSet * receiveData)
{
    WMErrCode result;
    u16 aid;
    u16 connectedAIDs;
    u16 state;
    result = native_fn_02011a34(2, WM_STATE_MP_PARENT, WM_STATE_MP_CHILD);
    if((result) != WM_ERRCODE_SUCCESS ) { return (result); } ;
    if (dsInfo == ((void *)0) ) {
        ((void) 0) ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    if (sendData == ((void *)0) ) {
        ((void) 0) ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    if (receiveData == ((void *)0) ) {
        ((void) 0) ;
        return WM_ERRCODE_INVALID_PARAM;
    }
    aid = native_fn_02011eb4();
    if (aid == 0) {
        connectedAIDs = native_fn_02011ee4();
    }
    state = dsInfo->state;
    if (state == WM_DS_STATE_ERROR) {
        ((void) 0) ;
        return WM_ERRCODE_FAILED;
    }
    if (state != WM_DS_STATE_START && state != WM_DS_STATE_RETRY_SEND) {
        ((void) 0) ;
        return WM_ERRCODE_ILLEGAL_STATE;
    }
    result = WM_ERRCODE_NO_DATASET;
    if (aid == 0) {
        BOOL sendFlag = 0 ;
        BOOL delayed = 0 ;
        if (state == WM_DS_STATE_RETRY_SEND) {
            int res;
            int oldWI;
            dsInfo->state = WM_DS_STATE_START;
            ((void) 0) ;
            oldWI = WmDataSharingGetPrevIndex(dsInfo->writeIndex);
            res =
                native_fn_020130e8(native_data_main_02013a44, dsInfo,
                                     (u16 *)&dsInfo->ds[oldWI], dsInfo->dataSetLength,
                                     (u16)(dsInfo->aidBitmap & connectedAIDs), dsInfo->port,
                                     WM_PRIORITY_HIGH);
            if (res == WM_ERRCODE_NO_CHILD) {
                ((void) 0)
                                     ;
                dsInfo->seqNum[oldWI] = 0xffff;
                dsInfo->sendIndex = WmDataSharingGetNextIndex(dsInfo->sendIndex);
            } else {
                if (res != WM_ERRCODE_SUCCESS && res != WM_ERRCODE_OPERATING) {
                    ((void) 0) ;
                    dsInfo->state = WM_DS_STATE_ERROR;
                    return WM_ERRCODE_FAILED;
                }
            }
        }
        if (dsInfo->readIndex != dsInfo->sendIndex) {
            ((void) 0)
                                 ;
            dsInfo->ds[dsInfo->readIndex].aidBitmap |= 0x0001;
            MI_CpuCopy16(&dsInfo->ds[dsInfo->readIndex], receiveData, sizeof(WMDataSet));
            dsInfo->currentSeqNum = dsInfo->seqNum[dsInfo->readIndex];
            dsInfo->readIndex = WmDataSharingGetNextIndex(dsInfo->readIndex);
            sendFlag = 1 ;
            result = WM_ERRCODE_SUCCESS;
            if (dsInfo->doubleMode == 0 && connectedAIDs != 0
                && dsInfo->ds[dsInfo->writeIndex].aidBitmap == 0x0001) {
                delayed = 1 ;
            } else {
                delayed = 0 ;
            }
        }
        native_fn_02013e08(dsInfo, 0 );
        if (sendFlag) {
            ((void) 0)
                                 ;
            native_fn_02013d3c(dsInfo, 0, (u16 *)sendData);
            if (dsInfo->doubleMode == 0 ) {
                native_fn_02013e08(dsInfo, delayed);
            }
        }
    } else {
        BOOL sendFlag = 0 ;
        if (state == WM_DS_STATE_RETRY_SEND) {
            sendFlag = 1 ;
            dsInfo->state = WM_DS_STATE_START;
            ((void) 0) ;
        } else {
            if (dsInfo->readIndex != dsInfo->writeIndex) {
                if (!(dsInfo->ds[dsInfo->readIndex].aidBitmap & 0x0001)) {
                    dsInfo->ds[dsInfo->readIndex].aidBitmap |= 0x0001;
                } else {
                    ((void) 0)
                                         ;
                    MI_CpuCopy16(&dsInfo->ds[dsInfo->readIndex], receiveData, sizeof(WMDataSet));
                    dsInfo->currentSeqNum = dsInfo->seqNum[dsInfo->readIndex];
                    dsInfo->readIndex = WmDataSharingGetNextIndex(dsInfo->readIndex);
                    sendFlag = 1 ;
                    result = WM_ERRCODE_SUCCESS;
                }
            }
        }
        if (sendFlag) {
            int res;
            u16 * buf = (u16 *)(((u8 *)&dsInfo->ds[dsInfo->sendIndex]) + 32);
            ((void) 0)                                 ;
            MI_CpuCopy16(sendData, buf, dsInfo->dataLength);
            res =
                native_fn_020130e8(native_data_main_02013a44, dsInfo, buf, dsInfo->dataLength,
                                     dsInfo->aidBitmap, dsInfo->port, WM_PRIORITY_HIGH);
            dsInfo->sendIndex = WmDataSharingGetNextIndex(dsInfo->sendIndex);
            if (res != WM_ERRCODE_OPERATING && res != WM_ERRCODE_SUCCESS) {
                ((void) 0) ;
                dsInfo->state = WM_DS_STATE_ERROR;
                result = WM_ERRCODE_FAILED;
            }
        }
    }
    return result;
}
void native_data_main_02013a44 (void * callback);
void native_fn_02013d3c (WMDataSharingInfo * dsInfo, u16 aid, u16 * data);
void native_fn_02013e08 (WMDataSharingInfo * dsInfo, BOOL delayed);
