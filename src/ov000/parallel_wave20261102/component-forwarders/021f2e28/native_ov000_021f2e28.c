#include "context.h"
void native_ov000_021f2e28(u32 selector, u32 a, u32 b, u32 c, s16 value)
{
    u32 *object;
    u8 *component;
    object = native_fn_main_02049ad0(selector);
    component = (u8 *) *(u32 *) (object[0] + 4);
    native_fn_main_02049f4c(object);
    native_fn_main_0204a04c(component, a, b, c);
    native_fn_main_02085270(component + 0x3C, value, 0);
}
