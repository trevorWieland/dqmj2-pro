#include "context.h"

extern void native_fn_02204974(u32 mode, u32 owner);

/* Advance the record's 16-bit counter and release its owner when the limit is
   reached. */
void native_main_02203314(u32 owner, u8 *record)
{
    *(s16 *)(record + 4) = (s16)(*(s16 *)(record + 4) + 1);
    if (*(s16 *)(record + 4) >= *(u16 *)(record + 6)) {
        record[9] = 0;
        native_fn_02204974(1, owner);
    }
}
