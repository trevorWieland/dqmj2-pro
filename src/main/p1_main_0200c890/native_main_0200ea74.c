#include "context.h"

extern u32 native_fn_0200f0c4(void);
extern u32 native_fn_0200e800(u32 command, u32 arg1, u32 arg2);

/* Send a 16-bit value as command 0x10 when the channel lock is available. */
u32 native_main_0200ea74(u32 value)
{
    if (native_fn_0200f0c4() == 0)
        return 0;
    return native_fn_0200e800(0x10, (u16)value, 0);
}
