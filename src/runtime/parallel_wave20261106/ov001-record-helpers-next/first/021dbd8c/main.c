#include "context.h"
s32 native_ov001_021dbd8c(Object440 *object) {
    s16 base = object->field222;
    s32 addition = native_fn_0207c52c(object->bytes1ec, object->child1e8 + 0x46);
    s32 value = native_fn_ov001_021dbc64(object, 2, base + addition);
    if (object->field238 != 0) value = 1;
    return MAXIMUM(1, MINIMUM(value, 9999));
}
