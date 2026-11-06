#include "context.h"
u32 native_ov006_021edc50(u32 value)
{
    return (u8) (value >> 24) | ((value >> 8) & 0xFF00U) | ((value << 8) & 0xFF0000U) | ((value << 24) & 0xFF000000U);
}
