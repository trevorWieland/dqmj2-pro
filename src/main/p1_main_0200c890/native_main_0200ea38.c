#include "context.h"

extern u32 native_fn_0200e9ec(void);
extern void native_fn_02007ff4(void);
extern void native_fn_02008064(u32 delay);
extern void native_fn_020087f8(void);
extern void native_fn_02008440(void);

/* Flush the queued command engine, then park forever in the idle loop. */
void native_main_0200ea38(void)
{
    if (native_fn_0200e9ec() != 0) {
        do {
            native_fn_02008064(0x000a3a47);
        } while (native_fn_0200e9ec() != 0);
    }
    native_fn_02007ff4();
    native_fn_020087f8();
    for (;;)
        native_fn_02008440();
}
