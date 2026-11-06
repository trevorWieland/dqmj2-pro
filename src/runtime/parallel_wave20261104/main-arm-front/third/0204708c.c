#include "context.h"
u32 native_main_0204708c(u32 value) {
    s32 index;
    if (value >= 0x61 && value <= 0x7a) return (u16)(value - 0x20);
    index = 0;
    do {
        if (value == native_data_main_020d932c[index * 2]) return native_data_main_020d932e[index * 2];
        index++;
    } while (index < 23);
    return value;
}
