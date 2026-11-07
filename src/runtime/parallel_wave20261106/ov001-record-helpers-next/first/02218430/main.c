#include "context.h"
s32 native_ov001_02218430(Object440 *object, s32 *values, u32 capacity) {
    s32 i = 0;
    if (object->field322 != 1) {
        while (i < object->field323 && capacity > (u32)i * sizeof(values[0])) {
            values[i] = object->values35e[i];
            i++;
        }
    } else {
        while (i < 6 && capacity > (u32)i * sizeof(values[0])) {
            values[i] = object->child1e8->values8[i];
            i++;
        }
    }
    return i;
}
