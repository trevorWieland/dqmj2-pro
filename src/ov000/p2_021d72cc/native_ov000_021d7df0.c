#include "context.h"

/* Feed every byte of the value list to the per-entry installer, then run the
   caller-side teardown. The list cursor is created after the count check so the
   list base is only loaded when there is at least one entry. */
void native_ov000_021d7df0(void)
{
    s8 index = 0;

    if (index < native_data_ov000_022300c0.entry_count) {
        u8 *cursor = native_data_ov000_02230150;

        do {
            native_fn_0204861c(0, *cursor++);
            index = index + 1;
        } while (index < native_data_ov000_022300c0.entry_count);
    }
    native_fn_ov000_021d7d90();
}
