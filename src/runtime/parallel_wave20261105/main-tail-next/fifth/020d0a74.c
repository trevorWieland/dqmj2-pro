#include "context.h"
void *native_main_020d0a74(void)
{
    s32 index = native_data_021d6b64.x0 + native_data_021d6b64.y1 * 4;
    s32 count = native_fn_020629e0();
    PageEntry *entries = native_data_021d6b5c.entries4;
    if (entries == 0) return 0;
    if (native_data_021d6b5c.page1 * 12 + index < count && native_data_021d6b64.side2 == 0) return entries[index].member0;
    return 0;
}
