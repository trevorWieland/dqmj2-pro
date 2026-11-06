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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_ov005_021e0730();
extern u32 native_fn_ov005_021e1048();
extern u32 native_fn_ov005_021e155c();
extern u8 native_data_ov005_021ed438[];
u32 native_ov005_021e2e64(void) {
    s32 temp_r0;
    u8 temp_r2;

    ++M2C_FIELD(native_data_ov005_021ed438, u8 *, 2);
    if ((u32) M2C_FIELD(native_data_ov005_021ed438, u8 *, 2) <= 0x28U) {
        return (u32) native_data_ov005_021ed438;
    }
    native_fn_ov005_021e155c(M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x64));
    native_fn_ov005_021e0730(0x13, 2, M2C_FIELD(native_data_ov005_021ed438, u16 *, 0xA));
    temp_r0 = (s32) (*(u16 *)0x027FFFA8 & 0x8000) >> 0xF;
    if (temp_r0 == 1) {
        return (u32) temp_r0;
    }
    return native_fn_ov005_021e1048(0x57);
}
