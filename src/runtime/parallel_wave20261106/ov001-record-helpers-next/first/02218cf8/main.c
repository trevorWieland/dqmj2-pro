#include "context.h"
s32 native_ov001_02218cf8(Object440 *first, Object440 *second, s32 value) {
    if (native_fn_0207afec(value)->low4 == 1) {
        if (first->field356 == 0) first->field356 = 1;
        s32 result = native_fn_ov001_021f07dc(first, second, value, 0, 0, 2, 0);
        return first->field356 * result;
    } else {
        return native_fn_ov001_021f0858(first, second,
            (s16)native_fn_0207b244(value, ov001_record_field_1f2_021dbd30(first),
                (u8 *)first->child1e8 + 0x46), value, 0, 0, 2);
    }
}
