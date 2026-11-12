#include "context.h"
s32 native_ov001_02226190(s32 *available, Object440 *object) {
    s32 values[3];
    s32 i, j, result;
    native_fn_02008e0c(available, values, sizeof(values));
    i = 0;
    do {
        if (values[i]) {
            if (object->field322 != 1) {
                j = 0;
                if (j < object->field323) do {
                    if (native_fn_0207afec(object->values35e[j])->field24 > 0) break;
                    if (j == object->field323 - 1) values[i] = 0;
                    j++;
                } while (j < object->field323);
            } else {
                j = 0;
                do {
                    if (native_fn_0207afec(object->child1e8->values8[j])->field24 > 0) break;
                    if (j == 5) values[i] = 0;
                    j++;
                } while (j < 6);
            }
        }
        i++;
        object++;
    } while (i < 3);
    result = ov001_count_candidates_02223f20(values);
    if (result > 0) native_fn_02008e0c(values, available, sizeof(values));
    return result;
}
