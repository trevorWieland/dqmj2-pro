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
extern u32 native_fn_02048a60();
extern u32 native_fn_02048a94();
extern u32 native_fn_02048a9c();
extern u32 native_fn_0205f98c();
extern u32 native_fn_ov001_022023a8();
u32 native_ov001_022059f0(void *arg0) {
    u32 temp_r0;
    u32 temp_r0_2;

    temp_r0_2 = native_fn_0205f98c(M2C_FIELD(arg0, s32 *, 0x1C), 0);
    native_fn_ov001_022023a8(temp_r0_2, 0x62);
    native_fn_02048a60(temp_r0_2, M2C_FIELD(arg0, s16 *, 0x14), M2C_FIELD(arg0, s16 *, 0x16));
    native_fn_02048a94(temp_r0_2, M2C_FIELD(arg0, u8 *, 0x20));
    native_fn_02048a9c(temp_r0_2, M2C_FIELD(arg0, u8 *, 0x21));
    temp_r0 = M2C_FIELD(temp_r0_2, u32 *, 0x7C) | 2;
    M2C_FIELD(temp_r0_2, u32 *, 0x7C) = temp_r0;
    return temp_r0;
}
