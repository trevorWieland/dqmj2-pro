#include "context.h"

/* Read the sound-context ready byte at +0xF, clear the request byte at +2 when it
 * is set, and return the ready byte (the image keeps it in r0 across the store,
 * which is why the zeroed byte is materialised in a second register). */
s32 native_ov001_02203480(void)
{
    u8 ready = native_data_ov001_02239c10[0xF];

    if (ready != 0)
        native_data_ov001_02239c10[2] = 0;
    return ready;
}
