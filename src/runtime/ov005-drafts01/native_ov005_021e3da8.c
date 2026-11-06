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
extern u32 native_fn_020bef68();
extern u32 native_fn_020bf224();
extern u32 native_fn_ov005_021dd6c0();
extern u32 native_fn_ov005_021e155c();
extern u32 native_fn_ov005_021e5b60();
extern u8 native_data_ov005_021ed438[];
extern u8 native_data_ov005_021edaf4[];
u32 native_ov005_021e3da8(void) {
    u8 temp_r0;

    native_fn_020bf224(native_data_ov005_021edaf4, M2C_FIELD(((M2C_FIELD(native_data_ov005_021ed438, u8 *, 4) * 0x268) + M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x40)), u8 *, 0xFF));
    native_fn_020bef68(3);
    native_fn_ov005_021e5b60();
    temp_r0 = M2C_FIELD(((M2C_FIELD(native_data_ov005_021ed438, u8 *, 4) * 0x268) + M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x40)), u8 *, 0xFF);
    switch (temp_r0) {
    case 3:
        native_fn_ov005_021dd6c0(6);
        break;
    case 1:
        native_fn_ov005_021dd6c0(4);
        break;
    case 2:
        native_fn_ov005_021dd6c0(5);
        break;
    }
    M2C_FIELD(native_data_ov005_021ed438, s16 *, 0xA) = 0x25;
    native_fn_ov005_021e155c(0x13);
    M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x64) = 0x14;
    return (u32) native_data_ov005_021ed438;
}
