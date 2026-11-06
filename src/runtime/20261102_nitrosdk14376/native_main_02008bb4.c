typedef unsigned long u32;
        typedef int BOOL;
typedef void (*MIDmaCallback) (void *);
typedef enum {
	GX_FIFOINTR_COND_DISABLE      = 0,
	GX_FIFOINTR_COND_UNDERHALF    = 1,
	GX_FIFOINTR_COND_EMPTY        = 2
} GXFifoIntrCond;
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
void native_main_02008bb4(void *);
void native_main_02008bb4 (void *)
{
	native_data_main_020e3740.isBusy = 0 ;
	MIi_CallCallback(native_data_main_020e3740.callback, native_data_main_020e3740.arg);
}
