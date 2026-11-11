#include "context.h"

/* Walk a byte backwards adding one, at most eight digits, stopping when the
   byte does not wrap to zero. */
void native_main_02091c30(u8 *digit)
{
    s32 remaining = 8;

    do {
        u8 value;

        digit--;
        value = (u8)(*digit + 1);
        *digit = value;
        if (value != 0)
            return;
    } while (--remaining != 0);
}
