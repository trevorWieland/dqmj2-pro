#include "context.h"

/* Clear the four-slot window block and initialise each slot through the shared
   window helper and the per-slot reset. The walk locals are created after the
   clear so the block base is only loaded for the walk. */
void native_ov000_021dfe0c(void)
{
    native_fn_02008c58(0, native_data_ov000_02232264, 0x60);
    {
        s32 index = 0;
        u8 *cursor = native_data_ov000_02232264;

        do {
            native_fn_020286e8(cursor + 4, (u8)index);
            native_fn_ov000_021dfea4(index, 0);
            index++;
            cursor += 0x18;
        } while (index < 4);
    }
}
