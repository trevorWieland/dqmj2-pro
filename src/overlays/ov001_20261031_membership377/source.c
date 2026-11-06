#include "context.h"
u32 native_ov001_02209ac0(void *actor) {
    void *record;
    s32 index;
    s32 reserve_index;
    u32 found;
    found = 0;
    index = 0;
    do {
        record = native_fn_02062a50(index);
        if (record && FIELD(record, u32 *, 0x14) == FIELD(FIELD(actor, void **, 0x1E8), u32 *, 0)) found = 1;
        index++;
    } while (index < 3);
    reserve_index = 0;
    do {
        record = native_fn_02062a88(reserve_index);
        if (record && FIELD(record, u32 *, 0x14) == FIELD(FIELD(actor, void **, 0x1E8), u32 *, 0)) found = 1;
        reserve_index++;
    } while (reserve_index < 3);
    return found == 0;
}
