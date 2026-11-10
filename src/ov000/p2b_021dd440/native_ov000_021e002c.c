#include "context.h"

/* Release the two byte-controlled sub-objects of the actor. The returned mask
   reports which releases ran: bit 1 for the 0x100 sub-object, bit 0 for the
   actor itself. */
s32 native_ov000_021e002c(u8 *actor)
{
    s32 flags = 0;

    if (actor[0x1e3] != 0) {
        native_fn_0203cac8(actor + 0x100, 0x41);
        flags |= 2;
    }
    if (actor[0x1e2] != 0) {
        native_fn_0203caa4(actor, 0x41);
        flags |= 1;
    }
    return flags;
}
