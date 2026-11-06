#include "compare_mutex.h"
extern u32 native_fn_0200708c(void *mutex);
extern u32 native_fn_02007110(void *mutex);
extern u8 *native_data_021d1914;

u32 native_main_02099138(void) {
    u32 value;
    native_fn_0200708c(native_data_021d1914+0x11DC);
    value=*(u32 *)(native_data_021d1914+0x1000);
    native_fn_02007110(native_data_021d1914+0x11DC);
    return value;
}
