#include "context.h"

extern void native_fn_0200f3e0(u8 *time);
extern void native_fn_0200f48c(u8 *time);
extern u32 native_fn_0200fc74(u8 *first, u8 *second);

/* Convert the two RTC snapshots and bias the difference. */
u32 native_main_02090b30(void)
{
    u8 first[0x10];
    u8 second[0x0c];

    native_fn_0200f3e0(first);
    native_fn_0200f48c(second);
    return native_fn_0200fc74(first, second) + 0x386d4380;
}
