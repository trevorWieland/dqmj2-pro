#include "context.h"

extern void native_fn_0200e46c(void);
extern u32 native_fn_0200e77c(u32 command, u32 arg1, u32 arg2, u32 callback, u32 *out);
extern void native_fn_0200f278(void);

/* Issue command 0x0e with the queued form pinned to the tag-check wait
   routine, then restore the previously installed wait routine. */
void native_main_0200e998(u32 arg3, u32 out)
{
    void (*saved)(void) = native_data_020dce4c;

    native_data_020dce4c = native_fn_0200e46c;
    native_fn_0200f278();
    native_data_020dce4c = saved;
    native_fn_0200e77c(0x0e, 0, 0, arg3, (u32 *)out);
}
