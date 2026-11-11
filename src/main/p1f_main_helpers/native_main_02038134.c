#include "context.h"

/* Store the byte at record offset 0x40 when the slot is live. */
void native_main_02038134(u8 *volatile *slot, u8 value)
{
    if (*slot != 0)
        (*slot)[0x40] = value;
}

