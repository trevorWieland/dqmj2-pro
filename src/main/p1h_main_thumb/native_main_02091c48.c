#include "context.h"

extern void native_fn_02093824(u32 base, u32 arg1, u32 arg2);

/* Prepare one indexed record and hand back the caller's context value. */
u32 native_main_02091c48(u32 base, u32 arg1, u32 arg2)
{
    native_fn_02093824(base + 0x1e0, arg1, arg2);
    return arg2;
}
