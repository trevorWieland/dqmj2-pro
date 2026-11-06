#include "context.h"
void *native_main_02048d14(u32 key, void *value)
{
    if (value) {
        if (native_fn_020349b8(value, key)) return value;
        native_fn_0204532c(native_data_02102970, value);
    }
    return 0;
}
