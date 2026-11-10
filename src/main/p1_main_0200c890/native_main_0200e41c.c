#include "context.h"

extern u32 native_fn_0200804c(void);
extern void native_fn_0200a4c8(void);

/* Wait for the queued transfer to finish.  Completes a pending step every time
   the driver reports the idle pattern or when interrupts are masked. */
void native_main_0200e41c(void)
{
    PendingWord *pending = &native_data_020e5428;

    if (native_data_020e540c.pending == 0)
        return;
    do {
        if (native_fn_0200804c() == 0x80 || *(volatile u16 *)0x04000208 == 0)
            native_fn_0200a4c8();
    } while (pending->pending != 0);
}
