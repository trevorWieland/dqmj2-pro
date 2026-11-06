#include "allocation_resource_setup_20261030.h"
u32 native_main_020787a0(void) {
    u32 temp_r4;
    s16 coordinates[2];

    temp_r4 = native_fn_ov000_02215698();
    native_fn_ov000_022159b8(native_data_020de414, 4);
    coordinates[0] = 0;
    coordinates[1] = 0;
    native_fn_0204b4f4(temp_r4 + 0x10, coordinates, 0xC8, 3, 2, 0x24);
    return native_fn_0204b61c(temp_r4 + 0x10, 0);
}
