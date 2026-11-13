#include "context.h"

/* native_ov001_0222afc8.c: 84 bytes at 0x0222afc8 in ov001.
 * void func(Record *record): seed the 12-byte 0x0222e344 template from the
 * record's +4 entry, submit command 0x86 and publish the result. */
typedef struct {
    s32 a;
    s32 b;
    s32 c;
} Block;

typedef struct {
    u8 unknown0[4];
    u8 *entry;
} Record;

void native_ov001_0222afc8(Record *record)
{
    Block local = *(Block *)native_data_ov001_0222e344;

    ov001_clear_free_candidate_slots_02223fe8((u32 *)&local, record->entry);
    native_fn_ov001_02226bdc(&local, record, 0x86);
    ov001_pick_random_candidate_02224050(&local);
    ov001_first_candidate_02226cb0(&local);
}
