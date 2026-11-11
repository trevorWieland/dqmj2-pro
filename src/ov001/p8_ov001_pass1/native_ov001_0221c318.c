#include "context.h"

/* Submit the object's three word fields to the battle command helper together
 * with two literal argument words, and report whether the answer reached 5. */
s32 native_ov001_0221c318(u32 *object)
{
    return native_fn_ov001_02218a54(object[0], object[2], object[3], 1, 1) >= 5;
}
