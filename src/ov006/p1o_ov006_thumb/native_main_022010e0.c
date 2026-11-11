#include "context.h"

extern u8 native_data_0221c160[];

/* Store the caller's halfword into the active flag record. */
void native_main_022010e0(u16 value)
{
    *(u16 *)(*(u32 **)native_data_0221c160) = value;
}
