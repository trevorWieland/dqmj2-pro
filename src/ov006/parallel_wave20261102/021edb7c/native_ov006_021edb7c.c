#include "context.h"
s32 native_ov006_021edb7c(u8 *left, u8 *right, s32 count)
{
    s32 difference = 0;
    while (count-- > 0 && (difference = *left - *right) == 0) { left++;
    right++;
    } return difference;
}
