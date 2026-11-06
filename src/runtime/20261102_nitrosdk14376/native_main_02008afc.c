typedef unsigned long u32;
        typedef int BOOL;
void native_fn_02005c64(u32 dmaNo, void (*callback)(void *), void * arg);
typedef void (*MIDmaCallback) (void *);
void native_main_02008afc(u32 dmaNo, const void * src, u32 commandLength, MIDmaCallback callback, void * arg);
void native_fn_02008714(u32 dmaNo);
typedef enum {
	GX_FIFOINTR_COND_DISABLE      = 0,
	GX_FIFOINTR_COND_UNDERHALF    = 1,
	GX_FIFOINTR_COND_EMPTY        = 2
} GXFifoIntrCond;
    void native_fn_01ff8448(u32 dmaNo, u32 src, u32 dest, u32 ctrl);
extern void native_fn_02005c64(u32 dmaNo, MIDmaCallback callback, void * arg);
static inline void MIi_CallCallback (MIDmaCallback callback, void * arg)
{
    if (callback) {
        (callback) (arg);
    }
}
    void native_fn_02008820(u32 dmaNo, u32 dmaType);
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
extern MIiGXDmaParams native_data_main_020e3740;
extern void native_data_main_02008bb4(void *);
void native_main_02008afc (u32 dmaNo, const void * src, u32 commandLength, MIDmaCallback callback, void * arg)
{
	((void) 0) ;
	((void) 0) ;
	((void)0) ;
	if (commandLength == 0) {
		MIi_CallCallback(callback, arg);
		return;
	}
	while (native_data_main_020e3740.isBusy  ) {
	}
	native_data_main_020e3740.isBusy = 1 ;
	native_data_main_020e3740.dmaNo = dmaNo;
	native_data_main_020e3740.callback = callback;
	native_data_main_020e3740.arg = arg;
	native_fn_02008820(dmaNo, (7UL << 27) );
	native_fn_020088a4(dmaNo, (u32)src, commandLength, (0UL << 23) );
	native_fn_02008714(dmaNo);
	native_fn_02005c64(dmaNo, native_data_main_02008bb4, ((void *)0) );
	native_fn_01ff8448(dmaNo, (u32)src, (u32)(0x04000000 + 0x400) , (((1UL << 31) | (7UL << 27) | (0UL << 23) | (2UL << 21) | (1UL << 26) | ((commandLength) / 4)) | (1UL << 30)) );
}
void native_data_main_02008bb4 (void *);
