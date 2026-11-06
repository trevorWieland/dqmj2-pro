typedef unsigned long u32;
typedef volatile u32 vu32;
typedef vu32 REGType32v;
typedef int BOOL;
typedef u32 OSIntrMode;
extern OSIntrMode native_fn_02007ff4(void);
extern OSIntrMode native_fn_02008008(OSIntrMode state);
typedef u32 OSIrqMask;
typedef void (*OSIrqFunction) (void);
OSIrqMask native_fn_02005d20(OSIrqMask intr);
void native_fn_02005b50(OSIrqMask intrBit, OSIrqFunction function);
OSIrqFunction native_fn_02005bd8(OSIrqMask intrBit);
typedef void (*MIDmaCallback) (void *);
void native_main_020088f8(u32 dmaNo, const void * src, u32 commandLength, MIDmaCallback callback, void * arg);
void native_fn_02008714(u32 dmaNo);
typedef enum {
	GX_FIFOINTR_COND_DISABLE      = 0,
	GX_FIFOINTR_COND_UNDERHALF    = 1,
	GX_FIFOINTR_COND_EMPTY        = 2
} GXFifoIntrCond;
typedef enum {
	GX_FIFOSTAT_EMPTY        = 6,
	GX_FIFOSTAT_UNDERHALF    = 2,
	GX_FIFOSTAT_OVERHALF     = 0,
	GX_FIFOSTAT_FULL         = 1
} GXFifoStat;
static void G3X_SetFifoIntrCond(GXFifoIntrCond cond);
static GXFifoStat G3X_GetCommandFifoStatus(void);
void native_fn_020088a4(u32 dmaNo, u32 src, u32 size, u32 dir);
typedef struct {
	volatile BOOL isBusy;
	u32 dmaNo;
	u32 src;
	u32 length;
	MIDmaCallback callback;
	void * arg;
	GXFifoIntrCond fifoCond;
	void (*fifoFunc)(void);
} MIiGXDmaParams;
typedef struct {
MIiGXDmaParams field_0000;
} NativeStorage_020e3740;
extern NativeStorage_020e3740 native_data_main_020e3740;
void native_fn_020089f0(void);
void native_fn_020089f0 (void);
static inline void G3X_SetFifoIntrCond (GXFifoIntrCond cond)
{
	((void) 0) ;
	(*( REGType32v *) (0x04000000 + 0x600)) = (((*( REGType32v *) (0x04000000 + 0x600)) & ~0xc0000000 ) |
	                  (cond << 30 ));
}
static inline GXFifoStat G3X_GetCommandFifoStatus (void)
{
	return (GXFifoStat)(((*( REGType32v *) (0x04000000 + 0x600)) & (0x01000000 |
	                                       0x02000000 |
	                                       0x04000000 )) >> 24 );
}
static inline void MIi_CallCallback (MIDmaCallback callback, void * arg)
{
    if (callback) {
        (callback) (arg);
    }
}
