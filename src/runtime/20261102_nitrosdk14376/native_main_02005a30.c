typedef unsigned short int u16;
typedef unsigned long u32;
typedef volatile u32 vu32;
        typedef u32 OSIrqMask;
extern u32 native_data_main_027e0000[];
typedef struct {
	void (*func) (void *);
	u32 enable;
	void * arg;
} OSIrqCallbackInfo;
extern OSIrqCallbackInfo native_data_main_020e335c[(7 + 1) ];
OSIrqMask native_fn_02005d50(OSIrqMask intr);
static inline void OS_SetIrqCheckFlag (OSIrqMask intr)
{
	*(vu32 *)((((u32)native_data_main_027e0000) + 0x00003fc0) + 0x38) |= (u32)intr;
}
void native_main_02005a30(int dmaNo);
OSIrqCallbackInfo native_data_main_020e335c[(7 + 1) ] = {
    {((void *)0) , 0, 0, },
    {((void *)0) , 0, 0, },
    {((void *)0) , 0, 0, },
    {((void *)0) , 0, 0, },
    {((void *)0) , 0, 0, },
    {((void *)0) , 0, 0, },
    {((void *)0) , 0, 0, },
    {((void *)0) , 0, 0, },
};
extern u16 native_data_main_020dcb48[(7 + 1) ];
void native_main_02005a30 (int index)
{
    OSIrqMask imask = (1UL << native_data_main_020dcb48[index]);
    void (*callback) (void *) = native_data_main_020e335c[index].func;
    native_data_main_020e335c[index].func = ((void *)0) ;
    if (callback) {
        (callback) (native_data_main_020e335c[index].arg);
    }
    OS_SetIrqCheckFlag(imask);
    if (!native_data_main_020e335c[index].enable) {
        (void)native_fn_02005d50(imask);
    }
}
