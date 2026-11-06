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
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
extern u32 native_fn_02043418();
extern u32 native_fn_02043570();
extern u32 native_fn_020435e8();
extern u32 native_fn_0204363c();
extern u32 native_fn_0204458c();
extern u8 native_data_020f69c4[];
u32 native_main_02043678(void) {
    u32 var_r0;
    u8 temp_r4;

    temp_r4 = M2C_FIELD(native_data_020f69c4, u8 *, 0x24);
    if (native_fn_0204458c() != 0) {
        goto block_2;
    }
    var_r0 = 1;
    goto block_3;
block_2:
    var_r0 = 0;
block_3:
    if (temp_r4 != 0) {
        goto block_5;
    }
    return native_fn_02043418();
block_5:
    if (temp_r4 != 8) {
        goto block_7;
    }
    return native_fn_02043418();
block_7:
    if (temp_r4 != 2) {
        goto block_10;
    }
    if (var_r0 == 0) {
        goto block_10;
    }
    return native_fn_02043418();
block_10:
    if (temp_r4 != 3) {
        goto block_12;
    }
    return native_fn_020435e8();
block_12:
    if (temp_r4 != 5) {
        goto block_14;
    }
    return var_r0;
block_14:
    if (temp_r4 != 7) {
        goto block_16;
    }
    return native_fn_020435e8();
block_16:
    if (temp_r4 != 6) {
        goto block_18;
    }
    return native_fn_0204363c();
block_18:
    if (temp_r4 == 1) {
        goto block_20;
    }
    return var_r0;
block_20:
    return native_fn_02043570();
}
