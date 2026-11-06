#include "context.h"
u32 native_main_0206092c(u32 value, void *output)
{
    u8 command[2];
    command[1] = (u8)value;
    command[0] = 0xe2;
    native_fn_02047ff0(command, 2, output);
    return 2;
}
