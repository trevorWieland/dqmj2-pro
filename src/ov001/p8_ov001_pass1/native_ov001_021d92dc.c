#include "context.h"

/* Release the 20-byte mixer slot selected by the first argument, forwarding the
 * caller's three payload words to the platform mixer release at 0x020287ac. */
void native_ov001_021d92dc(s32 slot, s32 a, s32 b, s32 c)
{
    native_fn_020287ac(native_data_ov001_02235534 + slot * 0x14, a, b, c);
}
