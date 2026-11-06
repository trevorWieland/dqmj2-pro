#include "context.h"
u32 native_ov000_021e8c34(u32 index, u32 value)
{
    u8 *position;
    u8 previous;
    position = data_ov000_02235450 + index * 0x2CCU;
    previous = *position;
    *position = value;
    return previous;
   
}
