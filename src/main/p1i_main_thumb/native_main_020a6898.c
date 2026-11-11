#include "context.h"

extern void native_fn_020a67e4(u32 arg1, u32 arg2, u32 arg3, u32 arg4, u32 arg5, u32 arg6,
                               u32 arg7, u32 arg8);

/* Forward seven arguments with the fixed 0x80 marker in the seventh slot. */
void native_main_020a6898(u32 arg1, u32 arg2, u32 arg3, u32 arg4, u32 arg5, u32 arg6, u32 arg7)
{
    native_fn_020a67e4(arg1, arg2, arg3, arg4, arg5, arg6, 0x80, arg7);
}
