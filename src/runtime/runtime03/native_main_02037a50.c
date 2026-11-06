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
extern u32 native_fn_0202b740();
extern u32 native_fn_0202b778();
extern u32 native_fn_02037d38();
u32 native_main_02037a50(s32 arg0, s32 arg1) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r1;
    u32 temp_r5;

    temp_r0 = arg0 + arg1;
    temp_r5 = (arg0 + 3) & ~3;
    if (temp_r5 > temp_r0) {
        return 0U;
    }
    temp_r1 = temp_r0 - temp_r5;
    if (temp_r1 < 0x10U) {
        return 0U;
    }
    temp_r0_2 = native_fn_0202b740(temp_r5 + 0x10, temp_r1 - 0x10, 0);
    if (temp_r0_2 == 0) {
        return 0U;
    }
    if (native_fn_02037d38(temp_r5, temp_r0_2) != 0) {
        return temp_r5;
    }
    native_fn_0202b778(temp_r0_2);
    return 0U;
}
