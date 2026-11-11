#include "context.h"

/* Scale a positive count by six fifths.  The magic constant 0x66666667 with the
 * `asr #1` on the high word is a signed division by five; the `mul` by six is the
 * numerator scaling, so the source expression is `value * 6 / 5` and not two
 * separate helpers. */
s32 native_ov001_0220ee84(s32 value)
{
    return value * 6 / 5;
}
