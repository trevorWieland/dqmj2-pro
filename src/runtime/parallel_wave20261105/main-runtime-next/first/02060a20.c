#include "context.h"
u32 native_main_02060a20(u32 item, void *output)
{
    u8 command[2];
    command[1] = (u8)native_fn_02066a6c(native_fn_02065d88(item)->symbol24);
    command[0] = 0xe2;
    native_fn_02047ff0(command, 2, output);
    return 2;
}
