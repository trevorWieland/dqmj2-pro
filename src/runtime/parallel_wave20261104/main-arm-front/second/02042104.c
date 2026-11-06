#include "context.h"
s32 native_main_02042104(Record *object, s32 delta, s32 update) {
    Matrix33 d, c, b, a;
    s32 previous = object->angles_0088.y;
    object->angles_0088.y = (s32)((u32)previous + (u32)delta);
    object->angles_0088.y = native_fn_02028158(object->angles_0088.y);
    object->flags_0009 |= previous != delta;
    if (update && object->flags_0009) {
        native_fn_02000ce8(&a);
        native_fn_020280a0(&b, object->angles_0088.z);
        native_fn_02028044(&c, object->angles_0088.y);
        native_fn_02027fe8(&d, object->angles_0088.x);
        native_fn_02000e1c(&c, &b, &a);
        native_fn_02000e1c(&d, &a, &object->matrix_0094);
        object->flags_0009 = 0;
    }
    return previous;
}
