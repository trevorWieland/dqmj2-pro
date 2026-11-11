#include "context.h"

/* Bind the 20-byte mixer slot selected by the first argument and hand it, with
 * the caller's three payload words, to the platform mixer initialiser at
 * 0x0202871c.  The three forwarded words are why the image keeps lr and ip as
 * scratch registers. */
void native_ov001_021d92c0(s32 slot, s32 a, s32 b, s32 c)
{
    native_fn_0202871c(native_data_ov001_02235534 + slot * 0x14, a, b, c);
}
