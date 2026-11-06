#include "context.h"
void native_ov006_021eddf4(u32 *input, u8 *output)
{
    native_fn_main_02008be0(0, output + 12, 32);
    *(u16 *) (output + 10) = (u16) *input;
    native_fn_main_02008e0c(input + 1, output + 12, *(u16 *) (output + 10));
}
