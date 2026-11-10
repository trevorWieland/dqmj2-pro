#include "context.h"

extern u32 native_fn_0200e8dc(u32 command, u32 arg1, u32 callback, u32 *out);
extern void native_fn_0200e4c8(void);

/* Two-argument command wrapper: submit, then run the installed wait routine. */
u32 native_main_0200e964(u32 command, u32 arg1)
{
    u32 result;
    u32 status = native_fn_0200e8dc(command, arg1, (u32)native_fn_0200e4c8, &result);

    if (status != 0)
        return status;
    native_data_020dce4c();
    return result;
}
