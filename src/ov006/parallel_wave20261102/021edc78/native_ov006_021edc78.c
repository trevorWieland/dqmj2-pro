#include "context.h"
u16 native_ov006_021edc78(s32 value)
{
    return (u16) ((u8) (value >> 8) | ((u32) value << 8 & 0xFF00U));
}
