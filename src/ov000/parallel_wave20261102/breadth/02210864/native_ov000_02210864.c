#include "context.h"
u32 native_ov000_02210864(u32 index, u32 value)
{
    u8 *position;
    u8 previous;
    position = data_ov000_02238816 + index * 708U;
    previous = *position;
    *position = value;
    return previous;
   
}
