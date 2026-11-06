#include "context.h"
u32 native_main_02049af0(u32 first, u32 second, u32 third, ArgumentBlock arguments)
{
    u32 previous = native_fn_02048f7c(1);
    native_fn_02049c90(native_fn_02048f7c(1), &arguments, arguments.input);
    native_fn_02049e28(first, second, third);
    if (arguments.enabled) {
        u32 mask = ~(1u << previous) & 0x3f;
        if (!arguments.include4) mask &= ~0x10u;
        native_fn_020414c8(mask);
        native_fn_02041538(1, 2, 4);
        native_fn_0204157c(10);
    }
    return arguments.output;
}
