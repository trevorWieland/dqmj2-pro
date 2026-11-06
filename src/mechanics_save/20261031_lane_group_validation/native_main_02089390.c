typedef unsigned char u8;
typedef signed int s32;
typedef unsigned int u32;
extern u32 native_fn_02044cdc(u32 key);
extern u32 native_fn_020649c0(u32 index);
extern u32 native_fn_020649e8(u32 index);
extern u32 native_fn_02088f64(u8 *record);
u32 native_main_02089390(s32 arg0) {
    s32 var_r4;
    u8 var_r5;
    u8 var_r6;
    u8 *temp_r8;
    u8 *temp_r8_2;

    var_r5 = 0;
    var_r6 = 0;
    var_r4 = 0;
loop_1:
    if (var_r4 < 3) {
        temp_r8 = (u8 *)native_fn_020649c0(var_r4);
        if (native_fn_02088f64(temp_r8) == 1) {
            return 1U;
        }
        if ((s32) *(u32 *)temp_r8 > 0) {
            var_r5 += native_fn_02044cdc(*(u32 *)temp_r8) + 1;
            if ((u32) var_r5 > 3U) {
                return 1U;
            }
        }
        goto block_13;
    }
    if (arg0 != 0) {
        temp_r8_2 = (u8 *)native_fn_020649e8(var_r4 - 3);
        if (native_fn_02088f64(temp_r8_2) == 1) {
            return 1U;
        }
        if ((s32) *(u32 *)temp_r8_2 > 0) {
            var_r6 += native_fn_02044cdc(*(u32 *)temp_r8_2) + 1;
            if ((u32) var_r6 > 3U) {
                return 1U;
            }
        }
        goto block_13;
    }
block_13:
    var_r4 += 1;
    if (var_r4 >= 6) {
        return 0U;
    }
    goto loop_1;
}
