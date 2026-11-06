typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_0207cd98();
extern u32 native_fn_020bf61c();
extern u8 native_data_021d4bec[];
u32 native_main_020bf76c(s32 arg0) {
    s32 var_r6;
    s32 var_r7;
    u32 temp_r8;

    var_r7 = 0;
    if (arg0 == 0) {
        return 0U;
    }
    var_r6 = 0;
loop_3:
    temp_r8 = native_fn_0207cd98(var_r6);
    if ((native_fn_020bf61c() != 0) || ((temp_r8 != 0) && (temp_r8 == M2C_FIELD(native_data_021d4bec, s32 *, 0x10)))) {
        if (var_r7 == (arg0 - 1)) {
            return temp_r8;
        }
        var_r7 += 1;
        goto block_9;
    }
block_9:
    var_r6 += 1;
    if (var_r6 >= 0x64) {
        return 0U;
    }
    goto loop_3;
}
