#include "context.h"

/* native_ov001_021fe54c.c: 92 bytes at 0x021fe54c in ov001.
 * void func(s8 a, s8 b): flush every one of 0x24 records whose live pair of
 * pointers and +4/+5 bytes match the arguments. */
typedef struct {
    u32 *first;
    s8 a;
    s8 b;
} Record;

void native_ov001_021fe54c(s8 a, s8 b)
{
    s8 i = 0;

    do {
        Record *record = (Record *)native_fn_02049ad0(i);

        if (record->first != 0 && *(u32 *)((u8 *)record->first + 4) != 0
            && record->a == a && record->b == b)
            native_fn_ov001_021fe6cc(record);
        i++;
    } while (i < 0x24);
}
