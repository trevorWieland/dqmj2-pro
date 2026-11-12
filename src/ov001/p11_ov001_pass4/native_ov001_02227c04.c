#include "context.h"

/* native_ov001_02227c04.c: 104 bytes at 0x02227c04 in ov001.
 * void func(Record *record): seed the 12-byte 0x0222e7d0 template, submit
 * command 0x25 and publish through 0x0222463c/ plus
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

void native_ov001_02227c04(Record *record)
{
    Block local = *(Block *)native_data_ov001_0222e7d0;
    u8 *entry = record->entry;

    native_fn_ov001_02223fe8((u32 *)&local, entry);
    native_fn_ov001_02226bdc(&local, record, 0x25);
    native_fn_ov001_0222463c(&local, entry, 5);
    native_fn_ov001_02224050(&local);
    native_fn_ov001_02226cb0(&local);
}
