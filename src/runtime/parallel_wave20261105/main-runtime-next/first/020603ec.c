#include "context.h"
u32 native_main_020603ec(u16 *output, s16 item, u32 kind, u32 style, s16 modifier)
{
    u8 parameters[32];
    native_fn_02044ff4(parameters, item, kind);
    native_fn_02046af4(native_data_021c9698, parameters, style, modifier, output, 255);
    return 1;
}
