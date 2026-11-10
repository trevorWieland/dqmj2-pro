#include "context.h"

extern u32 native_fn_02007ff4(void);
extern void native_fn_02008008(u32 state);
extern u32 native_fn_0200e3bc(void);
extern void native_fn_0200eb54(u32 word);

/* Queue one command: publish the completion callback and payload, then push the
   two command words.  Returns 0 after the queue is armed, 1 when another
   transfer already owns the block. */
u32 native_main_0200e77c(u32 command, u32 arg1, u32 arg2, u32 callback, u32 arg3)
{
    u32 irq = native_fn_02007ff4();

    if (native_fn_0200e3bc() == 0) {
        native_fn_02008008(irq);
        return 1;
    }
    native_data_020e540c.callback = (void (*)(u32, u32))callback;
    native_data_020e540c.callback_arg = arg3;
    native_data_020e540c.halfword_out = (u16 *)arg2;
    native_fn_0200eb54((command & 0xff) | 0x6100 | 0x02000000);
    native_fn_0200eb54(0x01010000 | (arg1 & 0xffff));
    native_fn_02008008(irq);
    return 0;
}
