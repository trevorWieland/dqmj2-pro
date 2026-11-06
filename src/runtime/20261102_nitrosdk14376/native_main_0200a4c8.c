typedef unsigned short int u16;
typedef unsigned long u32;
typedef volatile u16 vu16;
typedef volatile u32 vu32;
typedef vu16 REGType16v;
typedef vu32 REGType32v;
        typedef int BOOL;
    typedef u32 OSIntrMode;
    extern OSIntrMode native_fn_02007ff4(void);
    extern OSIntrMode native_fn_02008008(OSIntrMode state);
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
typedef enum {
	PXI_FIFO_SUCCESS              = 0,
	PXI_FIFO_FAIL_SEND_ERR        = -1,
	PXI_FIFO_FAIL_SEND_FULL       = -2,
	PXI_FIFO_FAIL_RECV_ERR        = -3,
	PXI_FIFO_FAIL_RECV_EMPTY      = -4,
	PXI_FIFO_NO_CALLBACK_ENTRY    = -5
} PXIFifoStatus;
typedef union {
	struct {
		u32 tag : 5 ;
		u32 err : 1 ;
		u32 data : 26 ;
	} e;
	u32 raw;
} PXIFifoMessage;
typedef void (*PXIFifoCallback) (PXIFifoTag tag, u32 data, BOOL err);
void native_main_0200a4c8(void);
extern const u16 (*ctrdgi_fl_maxtime);
extern PXIFifoCallback native_data_main_020e52c8[PXI_MAX_FIFO_TAG];
static inline PXIFifoStatus PXIi_GetFromFifo(u32 * data_buf);
static inline PXIFifoStatus PXIi_SetToFifo(u32 data);
static inline PXIFifoStatus PXIi_SetToFifo (u32 data)
{
    OSIntrMode enabled;
    if ((*( REGType16v *) (0x04000000 + 0x184)) & 0x4000 ) {
        (*( REGType16v *) (0x04000000 + 0x184)) |= (0x8000 | 0x4000 );
        return PXI_FIFO_FAIL_SEND_ERR;
    }
    enabled = native_fn_02007ff4();
    if ((*( REGType16v *) (0x04000000 + 0x184)) & 0x0002 ) {
        (void)native_fn_02008008(enabled);
        return PXI_FIFO_FAIL_SEND_FULL;
    }
    (*( REGType32v *) (0x04000000 + 0x188)) = data;
    (void)native_fn_02008008(enabled);
    return PXI_FIFO_SUCCESS;
}
static inline PXIFifoStatus PXIi_GetFromFifo (u32 * data_buf)
{
    OSIntrMode enabled;
    if ((*( REGType16v *) (0x04000000 + 0x184)) & 0x4000 ) {
        (*( REGType16v *) (0x04000000 + 0x184)) |= (0x8000 | 0x4000 );
        return PXI_FIFO_FAIL_RECV_ERR;
    }
    enabled = native_fn_02007ff4();
    if ((*( REGType16v *) (0x04000000 + 0x184)) & 0x0100 ) {
        (void)native_fn_02008008(enabled);
        return PXI_FIFO_FAIL_RECV_EMPTY;
    }
    *data_buf = (*( REGType32v *) (0x04000000 + 0x100000)) ;
    (void)native_fn_02008008(enabled);
    return PXI_FIFO_SUCCESS;
}
void native_main_0200a4c8 (void)
{
    PXIFifoMessage fifomsg;
    PXIFifoStatus ret_code;
    PXIFifoTag tag;
    while (1) {
        ret_code = PXIi_GetFromFifo(&fifomsg.raw);
        if (ret_code == PXI_FIFO_FAIL_RECV_EMPTY)
            break;
        if (ret_code == PXI_FIFO_FAIL_RECV_ERR)
            continue;
        tag = (PXIFifoTag)fifomsg.e.tag;
        if (tag) {
            if (native_data_main_020e52c8[tag]) {
                (native_data_main_020e52c8[tag])(tag, fifomsg.e.data, (BOOL)fifomsg.e.err);
            } else {
                if (fifomsg.e.err) {
                } else {
                    fifomsg.e.err = 1 ;
                    (void)PXIi_SetToFifo(fifomsg.raw);
                }
            }
        } else {
        }
    }
}
