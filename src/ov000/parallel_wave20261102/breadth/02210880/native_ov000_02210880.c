#include "context.h"
u32 native_ov000_02210880(u32 index, u32 value)
{
    u8 *position;
    u8 previous;
    position = data_ov000_02238818 + index * 708U;
    previous = *position;
    *position = value;
    return previous;
   
}
