#include "context.h"
s8 native_main_02060cb4(u32 kind, u32 alternate, u32 selected)
{
    s8 result = 0;
    if (alternate) result += 3;
    if (kind != 0) {
        if (kind == selected) result += 2;
        else result++;
    }
    return result;
}
