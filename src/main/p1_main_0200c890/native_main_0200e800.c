#include "context.h"

extern u32 native_fn_0200e77c(u32 command, u32 arg1, u32 arg2, u32 callback, u32 *out);
extern void native_fn_0200e4c8(void);

/* Submit a transfer command and park until it completes.  On a successful
   submit the installed wait routine runs and the completion value is
   returned. */
u32 native_main_0200e800(u32 command, u32 arg1, u32 arg2)
{
    u32 result;
    u32 status = native_fn_0200e77c(command, arg1, arg2, (u32)native_fn_0200e4c8, &result);

    if (status != 0)
        return status;
    native_data_020dce4c();
    return result;
}
