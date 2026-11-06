typedef unsigned long u32;
        typedef u32 OSIrqMask;
void native_main_02005c64(u32 dmaNo, void (*callback)(void *), void * arg);
typedef struct {
	void (*func) (void *);
	u32 enable;
	void * arg;
} OSIrqCallbackInfo;
extern OSIrqCallbackInfo native_data_main_020e335c[(7 + 1) ];
OSIrqMask native_fn_02005d20(OSIrqMask intr);
void native_main_02005c64 (u32 dmaNo, void (*callback)(void *), void * arg)
{
    OSIrqMask imask = (1UL << (8 + dmaNo));
    native_data_main_020e335c[dmaNo].func = callback;
    native_data_main_020e335c[dmaNo].arg = arg;
    native_data_main_020e335c[dmaNo].enable = native_fn_02005d20(imask) & imask;
}
OSIrqMask native_fn_02005d20 (OSIrqMask intr);
