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
extern u32 native_fn_0200c4dc();
extern u32 native_fn_0202a428();
extern u8 native_data_020f6028[];
u32 native_main_0203d068(void) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 var_r5;

    var_r5 = 0;
    temp_r0 = native_fn_0200c4dc(0U, 0U);
    temp_r0_2 = native_fn_0202a428(temp_r0, 4);
    M2C_FIELD(native_data_020f6028, u32 *, 0x10) = temp_r0_2;
    if ((temp_r0_2 != 0) && (native_fn_0200c4dc(temp_r0_2, temp_r0) <= temp_r0)) {
        var_r5 = 1;
    }
    return var_r5;
}
