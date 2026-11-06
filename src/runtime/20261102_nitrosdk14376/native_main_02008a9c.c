typedef unsigned long u32;
typedef volatile u32 vu32;
typedef vu32 REGType32v;
        typedef int BOOL;
        typedef u32 OSIrqMask;
typedef void (*OSIrqFunction) (void);
OSIrqMask native_fn_02005d50(OSIrqMask intr);
void native_fn_02005b50(OSIrqMask intrBit, OSIrqFunction function);
typedef void (*MIDmaCallback) (void *);
typedef enum {
	GX_FIFOINTR_COND_DISABLE      = 0,
	GX_FIFOINTR_COND_UNDERHALF    = 1,
	GX_FIFOINTR_COND_EMPTY        = 2
} GXFifoIntrCond;
static void G3X_SetFifoIntrCond(GXFifoIntrCond cond);
static inline void G3X_SetFifoIntrCond (GXFifoIntrCond cond)
{
	((void) 0) ;
	(*( REGType32v *) (0x04000000 + 0x600)) = (((*( REGType32v *) (0x04000000 + 0x600)) & ~0xc0000000 ) |
	                  (cond << 30 ));
}
static inline void MIi_CallCallback (MIDmaCallback callback, void * arg)
{
    if (callback) {
        (callback) (arg);
    }
}
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
extern MIiGXDmaParams native_data_main_020e3740;
void native_main_02008a9c(void *);
void native_main_02008a9c (void *)
{
	(void)native_fn_02005d50((1UL << 21) );
	G3X_SetFifoIntrCond(native_data_main_020e3740.fifoCond);
	native_fn_02005b50((1UL << 21) , native_data_main_020e3740.fifoFunc);
	native_data_main_020e3740.isBusy = 0 ;
	MIi_CallCallback(native_data_main_020e3740.callback, native_data_main_020e3740.arg);
}
