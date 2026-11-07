#include "context.h"
s32 native_ov001_021dbd3c(Object440 *object) {
    s32 value = object->field220;
    value += native_fn_0207c424(object->bytes1ec, object->child1e8 + 0x46);
    value = MAXIMUM(1, MINIMUM(value, 9999));
    return value;
}
