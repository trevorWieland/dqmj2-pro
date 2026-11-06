#include "context.h"
u32 native_ov000_021e8c18(u32 index, u32 value)
{
    u8 *position;
    u8 previous;
    position = data_ov000_0223544e + index * 0x2CCU;
    previous = *position;
    *position = value;
    return previous;
   
}
