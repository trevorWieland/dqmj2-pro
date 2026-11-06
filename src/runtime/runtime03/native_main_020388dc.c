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
extern u32 native_fn_020092a4();
extern u8 native_data_020f4c38[];
u32 native_main_020388dc(s32 arg0) {
    if (arg0 == 0) {
        return 1U;
    }
    if (arg0 & M2C_FIELD(native_data_020f4c38, s32 *, 8)) {
        return 0U;
    }
    native_fn_020092a4(arg0, 0);
    M2C_FIELD(native_data_020f4c38, s32 *, 8) = (s32) (M2C_FIELD(native_data_020f4c38, s32 *, 8) | arg0);
    return 1U;
}
