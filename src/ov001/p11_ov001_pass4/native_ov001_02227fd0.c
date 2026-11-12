#include "context.h"

/* native_ov001_02227fd0.c: 120 bytes at 0x02227fd0 in ov001.
 * void func(Record *record): seed the 12-byte 0x0222e770 template, submit
 * command 0x2d, then apply 0x0222463c/0x0224570 and flush through
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

void native_ov001_02227fd0(Record *record)
{
    Block local = *(Block *)native_data_ov001_0222e770;
    u8 *entry = record->entry;

    native_fn_ov001_02223fe8((u32 *)&local, entry);
    native_fn_ov001_02226bdc(&local, record, 0x2d);
    native_fn_ov001_0222463c(&local, entry, 6);
    native_fn_ov001_0224570(&local, entry, 4);
    native_fn_ov001_02224050(&local);
    native_fn_ov001_02226cb0(&local);
}
