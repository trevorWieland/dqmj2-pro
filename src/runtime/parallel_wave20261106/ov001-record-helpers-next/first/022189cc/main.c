#include "context.h"
s32 native_ov001_022189cc(Object440 *first, Object440 *second, s32 value, s32 mode) {
    s32 a = native_fn_0207afec(value)->field31;
    s32 b = native_fn_0207afec(value)->field32;
    s32 result = second->child1e8->values86[a];
    s32 other = 0;
    if (b != 0) other = second->child1e8->values86[b];
    if (mode != 0) result = native_fn_ov001_0220e3a8(first, a, b, result, other);
    else if (b != 0 && result >= other) result = other;
    return result;
}
