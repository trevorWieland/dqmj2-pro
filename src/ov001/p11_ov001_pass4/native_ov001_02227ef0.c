#include "context.h"

/* native_ov001_02227ef0.c: 104 bytes at 0x02227ef0 in ov001.
 * void func(Record *record): seed the 12-byte 0x0222e788 template, submit
 * command 0x2b and publish through 0x0222463c/ plus
 * 0x0224050/0x02226cb0. */
typedef struct {
    s32 a;
    s32 b;
    s32 c;
} Block;

typedef struct {
    u8 unknown0[4];
    u8 *entry;
} Record;

void native_ov001_02227ef0(Record *record)
{
    Block local = *(Block *)native_data_ov001_0222e788;
    u8 *entry = record->entry;

    ov001_clear_free_candidate_slots_02223fe8((u32 *)&local, entry);
    native_fn_ov001_02226bdc(&local, record, 0x2b);
    native_fn_ov001_0222463c(&local, entry, 6);
    ov001_pick_random_candidate_02224050(&local);
    ov001_first_candidate_02226cb0(&local);
}
