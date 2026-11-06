typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_020685c8(s32 index);
extern u32 native_fn_02096d04(u32 record);
extern u32 native_fn_02096d4c(u32 record);
extern u32 native_fn_02096d9c(u32 record);
u32 native_main_020bb144(s32 index) {
    u32 temp_r0;
    u32 var_r0;
    u32 temp_r4;

    temp_r4 = native_fn_020685c8(index);
    temp_r0 = native_fn_02096d9c(temp_r4);
    switch (temp_r0) {
    case 1:
        return 1U;
    case 2:
        return 2U;
    case 3:
        if (native_fn_02096d4c(temp_r4) != 0) {
            return 5U;
        }
        if (native_fn_02096d04(temp_r4) != 0) {
            var_r0 = 4;
        } else {
            var_r0 = 3;
        }
        return var_r0;
    default:
        return 0U;
    }
}
