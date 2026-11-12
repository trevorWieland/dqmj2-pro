#include "context.h"

/* native_ov001_0220b2fc.c: 72 bytes at 0x0220b2fc in ov001.
 * void func(void): drain the signed count in the 0x0223df3c block, then clear
 * its +4 word.  The pre-test plus do/while is what keeps the table load inside
 * the taken branch. */
void native_ov001_0220b2fc(void)
{
    s8 count = *(s8 *)native_data_ov001_0223df3c;

    if (count > 0) {
        do {
            native_fn_ov001_0220b344(
                ((s8 *)(native_data_ov001_0223df44 + count))[-1]);
            count = *(s8 *)native_data_ov001_0223df3c;
        } while (count > 0);
    }
    *(s32 *)(native_data_ov001_0223df3c + 4) = 0;
}
