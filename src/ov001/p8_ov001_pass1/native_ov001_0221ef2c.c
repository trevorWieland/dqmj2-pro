#include "context.h"
s32 native_ov001_0221ef2c(u8 *record)
{
    u32 value = *(u32 *)(record + 8);
    u32 command = *(u32 *)(record + 0xC);
    s32 result = 0;
    if (command == 0x72 && native_fn_ov001_02218b54(value, command, 8) != 0)
        result = 1;
    return result;
}
