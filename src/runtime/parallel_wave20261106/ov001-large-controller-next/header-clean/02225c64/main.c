#include "context.h"
s32 native_ov001_02225c64(s32 *available, Object440 *object, u32 mask) {
    s32 values[3];
    s32 i, j, childIndex, result;
    native_fn_02008e0c(available, values, sizeof(values));
    i = 0;
    do {
        if (values[i]) {
            if (object->field322 != 1) {
                j = 0;
                if (j < object->field323) do {
                    if (native_fn_0207b004(object->values35e[j], mask)) break;
                    if (j == object->field323 - 1) values[i] = 0;
                    j++;
                } while (j < object->field323);
            } else {
                childIndex = 0;
                do {
                    if (native_fn_0207b004(object->child1e8->values8[childIndex], mask)) break;
                    if (childIndex == 5) values[i] = 0;
                    childIndex++;
                } while (childIndex < 6);
            }
        }
        i++;
        object++;
    } while (i < 3);
    result = native_fn_ov001_02223f20(values);
    if (result > 0) native_fn_02008e0c(values, available, sizeof(values));
    return result;
}
