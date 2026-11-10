#include "context.h"

/* Accept a character code only outside the two reserved slots: the +0x61 bias
   maps the code into the 0x73 / 0x75 pair the layout helper distinguishes.
   Returns 1 for an accepted code and 0 for a reserved one. */
s32 native_ov000_021d9128(u8 code)
{
    s32 accepted = 1;
    u8 biased = code + 0x61;

    if (native_fn_0205bfd4() == 1) {
        if (biased == 0x73)
            accepted = 0;
    } else {
        if (biased == 0x75)
            accepted = 0;
    }
    return accepted;
}
