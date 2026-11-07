#include "context.h"
u32 native_ov001_021e2b1c(s32 a, s32 b) {
    s8 first, second;
    s32 i = 0;
    if (i < native_data_022388ec.count12) do {
        native_fn_ov001_021e8178(i, &first, &second);
        if (first == a && second == b) return 1;
        i++;
    } while (i < native_data_022388ec.count12);
    return 0;
}
