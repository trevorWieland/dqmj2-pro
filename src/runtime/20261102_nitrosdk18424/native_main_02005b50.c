typedef unsigned long u32;
        typedef u32 OSIrqMask;
typedef void (*OSIrqFunction) (void);
typedef struct {
	void (*func) (void *);
	u32 enable;
	void * arg;
} OSIrqCallbackInfo;
extern OSIrqFunction native_data_main_027e0000[];
extern OSIrqCallbackInfo native_data_main_020e335c[(7 + 1) ];
void native_main_02005b50(OSIrqMask intrBit, OSIrqFunction function);
void native_main_02005b50 (OSIrqMask intrBit, OSIrqFunction function)
{
    int i;
    OSIrqCallbackInfo * info;
    for (i = 0; i < 22 ; i++) {
        if (intrBit & 1) {
            info = ((void *)0) ;
            if (8 <= i && i <= 11 ) {
                info = &native_data_main_020e335c[i - 8 ];
            } else if (3 <= i && i <= 6 )   {
                info = &native_data_main_020e335c[i - 3 + 4 ];
            }
            else {
                native_data_main_027e0000[i] = function;
            }
            if (info) {
                info->func = (void (*)(void *)) function;
                info->arg = 0;
                info->enable = 1 ;
            }
        }
        intrBit >>= 1;
    }
}
