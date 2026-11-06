#include "context.h"
u32 native_main_02039fc4(PlayerHandle *handle, u32 a, u32 b, u32 c, u32 d)
{
    if (!native_fn_02039f2c(handle, a, b, c, d)) return 0;
    native_fn_02039fa4(handle);
    return 1;
}
