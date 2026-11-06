typedef unsigned long u32;
        typedef u32 OSIrqMask;
void native_main_02005cac(u32 timerNo, void (*callback)(void *), void * arg);
typedef struct {
	void (*func) (void *);
	u32 enable;
	void * arg;
} OSIrqCallbackInfo;
extern OSIrqCallbackInfo native_data_main_020e335c[(7 + 1) ];
OSIrqMask native_fn_02005d20(OSIrqMask intr);
void native_main_02005cac (u32 timerNo, void (*callback)(void *), void * arg)
{
    OSIrqMask imask = (1UL << (3 + timerNo));
    native_data_main_020e335c[timerNo + 4].func = callback;
    native_data_main_020e335c[timerNo + 4].arg = arg;
    (void)native_fn_02005d20(imask);
    native_data_main_020e335c[timerNo + 4].enable = 1 ;
}
OSIrqMask native_fn_02005d20 (OSIrqMask intr);
