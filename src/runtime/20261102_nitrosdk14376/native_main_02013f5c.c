typedef unsigned short int u16;
typedef unsigned long u32;
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
u16 * native_main_02013f5c(WMDataSharingInfo * dsInfo, WMDataSet * receiveData, u16 aid);
extern const u16 (*ctrdgi_fl_maxtime);
extern u16 * native_fn_02013fb0(WMDataSharingInfo * dsInfo, u32 aidBitmap, u16 * receiveBuf, u32 aid);
u16 * native_main_02013f5c (WMDataSharingInfo * dsInfo, WMDataSet * receiveData, u16 aid)
{
    u32 aidBitmap = receiveData->aidBitmap;
    u32 receivedBitmap = receiveData->receivedBitmap;
    u32 aidBit = (1U << aid);
    if (dsInfo == ((void *)0) ) {
        ((void) 0) ;
        return ((void *)0) ;
    }
    if (receiveData == ((void *)0) ) {
        ((void) 0) ;
        return ((void *)0) ;
    }
    if (!(aidBitmap & aidBit)) {
        return ((void *)0) ;
    }
    if (!(receivedBitmap & aidBit)) {
        return ((void *)0) ;
    }
    return native_fn_02013fb0(dsInfo, aidBitmap, receiveData->data, aid);
}
u16 * native_fn_02013fb0 (WMDataSharingInfo * dsInfo, u32 aidBitmap, u16 * receiveBuf, u32 aid);
