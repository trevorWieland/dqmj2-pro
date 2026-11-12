#include "context.h"

/* native_ov001_0222b198.c: 84 bytes at 0x0222b198 in ov001.
 * void func(Record *record): same publish with the 0x0222e2fc template and
 * command 0x90. */
typedef struct {
    s32 a;
    s32 b;
    s32 c;
} Block;

typedef struct {
    u8 unknown0[4];
    u8 *entry;
} Record;

void native_ov001_0222b198(Record *record)
{
    Block local = *(Block *)native_data_ov001_0222e2fc;

    native_fn_ov001_02223fe8((u32 *)&local, record->entry);
    native_fn_ov001_02226bdc(&local, record, 0x90);
    native_fn_ov001_02224050(&local);
    native_fn_ov001_02226cb0(&local);
}
