#include "context.h"

/* native_ov001_02226d2c.c: 68 bytes at 0x02226d2c in ov001.
 * void func(Record *record): copy the 12-byte 0x0222e914 template to the stack,
 * fill it from the record's +4 entry, then publish and query it. */
typedef struct {
    s32 a;
    s32 b;
    s32 c;
} Block;

typedef struct {
    u8 unknown0[4];
    u8 *entry;
} Record;

void native_ov001_02226d2c(Record *record)
{
    Block local = *(Block *)native_data_ov001_0222e914;

    native_ov001_02223fe8((u32 *)&local, record->entry);
    native_fn_ov001_02224050(&local);
    native_fn_ov001_02226cb0(&local);
}
