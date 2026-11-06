#include "packed_pointer_abi.h"

u32 native_main_02096d4c(u32 *record) {
    u32 value;
    value=native_fn_02096ce8(record);
    if (((value&0x10)==0x10)&&((value&8)!=8)) return 1;
    return 0;
}
