#include "context.h"

extern u32 native_fn_02008058(void);
extern void native_fn_0200a4c8(void);

/* Drain completed transfers until the outstanding count clears. */
void native_main_0200e3dc(void)
{
    PendingWord *pending = &native_data_020e5428;

    if (native_data_020e540c.pending != 0) {
        do {
            if (native_fn_02008058() == 0x12)
                native_fn_0200a4c8();
        } while (pending->pending != 0);
    }
}
