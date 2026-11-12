#include "context.h"

/* native_ov001_022281e8.c: 120 bytes at 0x022281e8 in ov001.
 * void func(Record *record): seed the 12-byte 0x0222e740 template, submit
 * command 0x31, then apply 0x0222463c/0x0224570 and flush through
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

void native_ov001_022281e8(Record *record)
{
    Block local = *(Block *)native_data_ov001_0222e740;
    u8 *entry = record->entry;

    native_fn_ov001_02223fe8((u32 *)&local, entry);
    native_fn_ov001_02226bdc(&local, record, 0x31);
    native_fn_ov001_0222463c(&local, entry, 7);
    native_fn_ov001_0224570(&local, entry, 1);
    native_fn_ov001_02224050(&local);
    native_fn_ov001_02226cb0(&local);
}
