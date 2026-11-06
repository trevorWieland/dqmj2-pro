#include "context.h"
void *native_main_02048dd4(u32 key, void *value)
{
    if (value) {
        if (native_fn_020346c0(value, key)) return value;
        native_fn_0204532c(native_data_02102970, value);
    }
    return 0;
}
