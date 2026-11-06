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
extern u32 native_fn_020414b0();
extern u32 native_fn_020414c8();
extern u32 native_fn_02041510();
extern u32 native_fn_02041538();
extern u32 native_fn_0205e814();
u32 native_itcm_01ffb6e0(s32 arg0) {
    u32 temp_r0;

    native_fn_020414b0(0x3F);
    native_fn_02041510(1, 2, 0xF);
    native_fn_020414c8(0x3F);
    temp_r0 = native_fn_02041538(1, 2, 0xF);
    if (arg0 != 1) {
        return temp_r0;
    }
    return native_fn_0205e814(0, 0, 0xF);
}
