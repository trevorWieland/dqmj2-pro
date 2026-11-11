#include "context.h"

extern u32 native_fn_02029618(u8 *object, u32 *slot, u32 mask);

/* Release the 0x64 slot with the "visible" mask and clear the pending counter
   when the slot was actually freed. */
u32 native_main_02029688(u8 *object)
{
    if (native_fn_02029618(object, (u32 *)(object + 0x64), 4) != 0) {
        *(u32 *)(object + 0xf8) = 0;
        return 1;
    }
    return 0;
}
