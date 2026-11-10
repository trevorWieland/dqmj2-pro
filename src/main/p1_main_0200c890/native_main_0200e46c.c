#include "context.h"

extern u32 native_fn_0200804c(void);
extern u32 native_fn_02008058(void);
extern void native_fn_0200a4c8(void);

/* Same wait as 0200e41c, but an idle driver report is also completed when the
   queued command tag is the "finished" tag 0x12. */
void native_main_0200e46c(void)
{
    PendingWord *pending = &native_data_020e5428;

    if (native_data_020e540c.pending == 0)
        return;
    do {
        if (native_fn_0200804c() == 0x80 || *(volatile u16 *)0x04000208 == 0 ||
            native_fn_02008058() == 0x12)
            native_fn_0200a4c8();
    } while (pending->pending != 0);
}
