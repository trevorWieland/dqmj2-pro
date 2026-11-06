#include "context.h"
s8 native_main_02060c1c(u32 kind, u32 alternate, u32 selected)
{
    s8 result = alternate == 0 ? 0 : 3;
    if (kind != 0) {
        if (kind == selected) result += 2;
        else result++;
    }
    return result;
}
