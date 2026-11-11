#include "context.h"

extern u8 native_data_0221c140[];

/* Store the mode byte and the derived pair value into the slot record. */
void native_main_021fe8d0(u32 mode)
{
    u8 pair;

    (*(u8 **)native_data_0221c140)[0x1c] = (u8)mode;
    if (mode == 2)
        pair = 4;
    else
        pair = 6;
    (*(u8 **)native_data_0221c140)[0x1d] = pair;
}
