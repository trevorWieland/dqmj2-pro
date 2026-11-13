#include "context.h"

/* native_ov001_02226d70.c: 68 bytes at 0x02226d70 in ov001.
 * void func(Record *record): same 0x0222e908 template publish. */
typedef struct {
    s32 a;
    s32 b;
    s32 c;
} Block;

typedef struct {
    u8 unknown0[4];
    u8 *entry;
} Record;

void native_ov001_02226d70(Record *record)
{
    Block local = *(Block *)native_data_ov001_0222e908;

    ov001_clear_free_candidate_slots_02223fe8((u32 *)&local, record->entry);
    ov001_pick_random_candidate_02224050(&local);
    ov001_first_candidate_02226cb0(&local);
}
