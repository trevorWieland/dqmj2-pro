#include "context.h"

extern u32 native_fn_0200e844(s32 operation, u32 callback, u32 *out);
extern void native_fn_0200e4c8(void);

/* Command wrapper whose operation index never selects the queued form. */
u32 native_main_0200e8a8(u32 command)
{
    u32 result;
    u32 status = native_fn_0200e844((s32)command, (u32)native_fn_0200e4c8, &result);

    if (status != 0)
        return status;
    native_data_020dce4c();
    return result;
}
