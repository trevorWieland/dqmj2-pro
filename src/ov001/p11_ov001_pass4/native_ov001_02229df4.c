#include "context.h"

/* native_ov001_02229df4.c: 132 bytes at 0x02229df4 in ov001.
 * void func(Record *record): seed the 12-byte 0x0222e50c template,
 * submit command 0x60, then publish through 0x02224570
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

void native_ov001_02229df4(Record *record)
{
    Block local = *(Block *)native_data_ov001_0222e50c;
    u8 *entry = record->entry;
    u8 *other = record->other;

    native_fn_ov001_02223fe8((u32 *)&local, entry);
    native_fn_ov001_02226bdc(&local, record, 0x60);
    native_fn_ov001_0225534(&local, entry,
                            M2C_FIELD(native_fn_0207afec((s32)other), u8 *, 0x1f));
    native_fn_ov001_02224570(&local, entry, 4);
    native_fn_ov001_02224050(&local);
    native_fn_ov001_02226cb0(&local);
}
