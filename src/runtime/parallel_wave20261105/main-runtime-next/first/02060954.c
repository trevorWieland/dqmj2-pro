#include "context.h"
u32 native_main_02060954(u32 item, void *output)
{
    u8 command[2];
    ItemMetadata *metadata = native_fn_020449d4(item);
    command[0] = 0xe2;
    command[1] = (u8)(metadata->flags4.nibble4 + 13);
    native_fn_02047ff0(command, 2, output);
    return 2;
}
