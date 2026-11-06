#include "context.h"
int native_main_02048188(u32 offset, u32 value)
{
    u8 bytes[3];
    bytes[0] = 0xe3;
    bytes[1] = 0x1c;
    bytes[2] = (u8)value;
    native_fn_02047ff0(bytes, 3, offset);
    return 3;
}
