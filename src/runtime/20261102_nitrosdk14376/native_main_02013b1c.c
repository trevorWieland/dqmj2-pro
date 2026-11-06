typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
        typedef int BOOL;
    typedef u32 OSIntrMode;
    extern OSIntrMode native_fn_02007ff4(void);
    extern OSIntrMode native_fn_02008008(OSIntrMode state);
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
typedef enum WMStateCode {
	WM_STATECODE_PARENT_START                = 0,
	WM_STATECODE_BEACON_SENT                 = 2,
	WM_STATECODE_SCAN_START                  = 3,
	WM_STATECODE_PARENT_NOT_FOUND            = 4,
	WM_STATECODE_PARENT_FOUND                = 5,
	WM_STATECODE_CONNECT_START               = 6,
	WM_STATECODE_BEACON_LOST                 = 8,
	WM_STATECODE_CONNECTED                   = 7,
	WM_STATECODE_CHILD_CONNECTED             = 7,
	WM_STATECODE_DISCONNECTED                = 9,
	WM_STATECODE_DISCONNECTED_FROM_MYSELF    = 26,
	WM_STATECODE_MP_START                    = 10,
	WM_STATECODE_MPEND_IND                   = 11,
	WM_STATECODE_MP_IND                      = 12,
	WM_STATECODE_MPACK_IND                   = 13,
	WM_STATECODE_DCF_START                   = 14,
	WM_STATECODE_DCF_IND                     = 15,
	WM_STATECODE_BEACON_RECV                 = 16,
	WM_STATECODE_DISASSOCIATE                = 17,
	WM_STATECODE_REASSOCIATE                 = 18,
	WM_STATECODE_AUTHENTICATE                = 19,
	WM_STATECODE_PORT_INIT                   = 25,
	WM_STATECODE_PORT_SEND                   = 20,
	WM_STATECODE_PORT_RECV                   = 21,
	WM_STATECODE_FIFO_ERROR                  = 22,
	WM_STATECODE_INFORMATION                 = 23,
	WM_STATECODE_UNKNOWN                     = 24,
	WM_STATECODE_MAX                         = 27
} WMStateCode;
typedef enum WMDataSharingState {
	WM_DS_STATE_READY = 0,
	WM_DS_STATE_START,
	WM_DS_STATE_PAUSING,
	WM_DS_STATE_PAUSED,
	WM_DS_STATE_RETRY_SEND,
	WM_DS_STATE_ERROR
} WMDataSharingState;
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
typedef struct WMMpRecvBuf {
	u16 rsv1[3];
	u16 length;
	u16 rsv2[1];
	u16 ackTimeStamp;
	u16 timeStamp;
	u16 rate_rssi;
	u16 rsv3[2];
	u16 rsv4[2];
	u8 destAdrs[6];
	u8 srcAdrs[6];
	u16 rsv5[3];
	u16 seqCtrl;
	u16 txop;
	u16 bitmap;
	u16 wmHeader;
	u16 data[2];
} WMMpRecvBuf, WMmpRecvBuf;
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
extern const u16 (*ctrdgi_fl_maxtime);
void native_main_02013b1c(void * callback);
extern void native_fn_02013d3c(WMDataSharingInfo * dsInfo, u16 aid, u16 * data);
extern void native_fn_02013e08(WMDataSharingInfo * dsInfo, BOOL delayed);
static inline u16 WmDataSharingGetNextIndex (u32 index)
{
    return (u16)((index + 1) % 4 );
}
void native_main_02013b1c (void * callback)
{
    WMPortRecvCallback * cb_Port = (WMPortRecvCallback *)callback;
    WMDataSharingInfo * dsInfo = (WMDataSharingInfo *)cb_Port->arg;
    if (dsInfo == ((void *)0) ) {
        ((void) 0) ;
        return;
    }
    if (cb_Port->errcode == WM_ERRCODE_SUCCESS) {
        switch (cb_Port->state) {
        case WM_STATECODE_PORT_RECV:
            native_fn_02013d3c(dsInfo, cb_Port->aid, cb_Port->data);
            native_fn_02013e08(dsInfo, 0 );
            break;
        case WM_STATECODE_CONNECTED:
            native_fn_02013e08(dsInfo, 0 );
            break;
        case WM_STATECODE_DISCONNECTED:
        case WM_STATECODE_DISCONNECTED_FROM_MYSELF:
        {
            u32 aidBit;
            u32 writeIndex;
            OSIntrMode enabled;
            aidBit = 1U << cb_Port->aid;
            enabled = native_fn_02007ff4();
            writeIndex = dsInfo->writeIndex;
            dsInfo->ds[writeIndex].aidBitmap &= ~aidBit;
            if (dsInfo->doubleMode == 1 ) {
                dsInfo->ds[WmDataSharingGetNextIndex(writeIndex)].aidBitmap &= ~aidBit;
            }
            (void)native_fn_02008008(enabled);
            native_fn_02013e08(dsInfo, 0 );
            if (dsInfo->doubleMode == 1 ) {
                native_fn_02013e08(dsInfo, 0 );
            }
        }
        break;
        case WM_STATECODE_PORT_INIT:
            break;
        }
    } else {
        ((void) 0)
                   ;
        dsInfo->state = WM_DS_STATE_ERROR;
    }
}
void native_fn_02013d3c (WMDataSharingInfo * dsInfo, u16 aid, u16 * data);
void native_fn_02013e08 (WMDataSharingInfo * dsInfo, BOOL delayed);
