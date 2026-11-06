#include "record_lookup_abi.h"
extern u32 native_fn_0206be2c(void);
extern u32 native_fn_0206bf34(void);
extern u32 native_fn_0206dcd0(void *record);
u32 native_main_02078a1c(void) {
    u32 id = native_fn_0206be2c();
    if (id != 0) return native_fn_0206dcd0(native_fn_02062a10(id));
    return native_fn_0206dcd0(native_fn_02062a10(native_fn_0206bf34()));
}
