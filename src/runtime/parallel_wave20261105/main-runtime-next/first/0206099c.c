#include "context.h"
u32 native_main_0206099c(s32 kind, void *output)
{
    u8 command[2];
    u32 length = 0;
    command[0] = 0xe2;
    if (kind >= 8) {
        command[1] = (u8)native_fn_02060510(kind);
        length = 2;
        native_fn_02047ff0(command, length, output);
    }
    return length;
}
