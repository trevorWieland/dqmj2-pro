#include "context.h"
void native_main_020421b4(Record *object, s32 x, s32 y, s32 z, s32 update) {
    Matrix33 d, c, b, a;
    object->angles_0088.x = (s32)((u32)object->angles_0088.x + (u32)x);
    object->angles_0088.y = (s32)((u32)object->angles_0088.y + (u32)y);
    object->angles_0088.z = (s32)((u32)object->angles_0088.z + (u32)z);
    object->angles_0088.x = native_fn_02028158(object->angles_0088.x);
    object->angles_0088.y = native_fn_02028158(object->angles_0088.y);
    object->angles_0088.z = native_fn_02028158(object->angles_0088.z);
    object->flags_0009 |= 1;
    if (!update || !object->flags_0009) return;
    native_fn_02000ce8(&a);
    native_fn_020280a0(&b, object->angles_0088.z);
    native_fn_02028044(&c, object->angles_0088.y);
    native_fn_02027fe8(&d, object->angles_0088.x);
    native_fn_02000e1c(&c, &b, &a);
    native_fn_02000e1c(&d, &a, &object->matrix_0094);
    object->flags_0009 = 0;
}
