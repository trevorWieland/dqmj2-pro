typedef unsigned short int u16;
typedef unsigned long u32;
    typedef u32 OSIntrMode;
    extern OSIntrMode native_fn_02007ff4(void);
    extern OSIntrMode native_fn_02008008(OSIntrMode state);
void native_fn_02008be0(u16 data, void * destp, u32 size);
void native_fn_02008bf8(const void * srcp, void * destp, u32 size);
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
extern const u16 (*ctrdgi_fl_maxtime);
void native_main_02013d3c(WMDataSharingInfo * dsInfo, u16 aid, u16 * data);
extern u16 * native_fn_02013fb0(WMDataSharingInfo * dsInfo, u32 aidBitmap, u16 * receiveBuf, u32 aid);
static inline u16 WmDataSharingGetNextIndex (u32 index)
{
    return (u16)((index + 1) % 4 );
}
void native_main_02013d3c (WMDataSharingInfo * dsInfo, u16 aid, u16 * data)
{
    u16 aidBit = (u16)(1 << aid);
    ((void) 0)                         ;
    if (dsInfo->aidBitmap & aidBit) {
        u16 * buf;
        u16 writeIndex;
        OSIntrMode enabled;
        if (!(dsInfo->ds[dsInfo->writeIndex].aidBitmap & aidBit)) {
            if (dsInfo->doubleMode == 1 ) {
                ((void) 0) ;
                writeIndex = WmDataSharingGetNextIndex(dsInfo->writeIndex);
                if (!(dsInfo->ds[writeIndex].aidBitmap & aidBit)) {
                    ((void)0)                               ;
                    return;
                }
            } else {
                ((void)0) ;
                return;
            }
        } else {
            writeIndex = dsInfo->writeIndex;
        }
        buf = native_fn_02013fb0(dsInfo, dsInfo->aidBitmap, dsInfo->ds[writeIndex].data, aid);
        if (data != ((void *)0) ) {
            MI_CpuCopy16(data, buf, dsInfo->dataLength);
        } else {
            MI_CpuClear16(buf, dsInfo->dataLength);
        }
        enabled = native_fn_02007ff4();
        dsInfo->ds[writeIndex].aidBitmap &= ~aidBit;
        dsInfo->ds[writeIndex].receivedBitmap |= aidBit;
        (void)native_fn_02008008(enabled);
    }
}
u16 * native_fn_02013fb0 (WMDataSharingInfo * dsInfo, u32 aidBitmap, u16 * receiveBuf, u32 aid);
