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
extern u32 native_fn_0204540c();
extern u32 native_fn_02045770();
extern u32 native_fn_02048f6c();
extern u32 native_fn_ov006_021d7e90();
extern u8 native_data_ov006_0220e9a0[];
extern u8 native_data_ov006_0220e9f0[];
extern u8 native_data_ov006_0220e9f4[];
u32 native_ov006_021d7ebc(u32 arg0, s32 arg1, s32 arg2) {
    u32 temp_r4;

    temp_r4 = native_fn_02048f6c(0);
    native_fn_ov006_021d7e90(native_data_ov006_0220e9f0, arg0);
    native_fn_0204540c(temp_r4, native_data_ov006_0220e9f4, M2C_FIELD(native_data_ov006_0220e9a0, s32 *, 0x20) << 5, 0x80);
    native_fn_02045770(0, temp_r4, 2, 2, arg1, arg2, 0x20, M2C_FIELD(native_data_ov006_0220e9a0, s32 *, 0x20), *(u32 *)native_data_ov006_0220e9f0 + 5);
    M2C_FIELD(native_data_ov006_0220e9a0, s32 *, 0x20) = (s32) (M2C_FIELD(native_data_ov006_0220e9a0, s32 *, 0x20) - 4);
    return (u32) native_data_ov006_0220e9a0;
}
