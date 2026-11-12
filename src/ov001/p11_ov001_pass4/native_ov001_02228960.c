#include "context.h"

/* native_ov001_02228960.c: 152 bytes at 0x02228960 in ov001.
 * void func(Record *record): seed the 12-byte 0x0222e698 template,
 * submit command 0x3f, then apply 0x022470c/0x0224570
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

void native_ov001_02228960(Record *record)
{
    Block local = *(Block *)native_data_ov001_0222e698;
    u8 *entry = record->entry;
    u8 *other = record->other;

    ov001_clear_free_candidate_slots_02223fe8((u32 *)&local, entry);
    native_fn_ov001_02226bdc(&local, record, 0x3f);
    native_fn_ov001_0225534(&local, entry,
                            M2C_FIELD(native_fn_0207afec((s32)other), u8 *, 0x1f));
    native_fn_ov001_022470c(&local, entry, 1, 7);
    native_fn_ov001_0224570(&local, entry, 7);
    ov001_pick_random_candidate_02224050(&local);
    ov001_first_candidate_02226cb0(&local);
}
