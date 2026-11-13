#include "context.h"

/* native_ov001_0222a7cc.c: 132 bytes at 0x0222a7cc in ov001.
 * void func(Record *record): seed the 12-byte 0x0222e434 template,
 * submit command 0x72, then publish through 0x02224570
 * and flush through 0x0224050/0x02226cb0. */
typedef struct {
    s32 a;
    s32 b;
    s32 c;
} Block;

typedef struct {
    u8 unknown0[4];
    u8 *entry;
    u8 *other;
} Record;

void native_ov001_0222a7cc(Record *record)
{
    Block local = *(Block *)native_data_ov001_0222e434;
    u8 *entry = record->entry;
    u8 *other = record->other;

    ov001_clear_free_candidate_slots_02223fe8((u32 *)&local, entry);
    native_fn_ov001_02226bdc(&local, record, 0x72);
    native_fn_ov001_0225534(&local, entry,
                            M2C_FIELD(native_fn_0207afec((s32)other), u8 *, 0x1f));
    ov001_filter_highest_priority_candidates_02224570(&local, entry, 4);
    ov001_pick_random_candidate_02224050(&local);
    ov001_first_candidate_02226cb0(&local);
}
