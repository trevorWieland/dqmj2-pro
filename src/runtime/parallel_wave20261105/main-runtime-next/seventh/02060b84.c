#include "context.h"
s8 native_main_02060b84(u32 kind, u32 alternate, u32 selected)
{
    if (kind == 0) return alternate == 0 ? 4 : 7;
    if (kind <= 2) {
        if (kind == 1) return alternate == 0 ? 0 : 2;
        return alternate == 0 ? 1 : 3;
    }
    if (kind == selected) return alternate == 0 ? 6 : 9;
    return alternate == 0 ? 5 : 8;
}
