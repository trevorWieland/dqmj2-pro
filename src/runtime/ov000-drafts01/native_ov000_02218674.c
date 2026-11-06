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
extern u32 native_fn_0205f998();
extern u32 native_fn_ov000_0221863c();
extern u32 native_fn_ov000_02219d70();
extern u8 native_data_ov000_02245ee4[];
u32 native_ov000_02218674(void) {
    u32 temp_r0;

    native_fn_0205f998(native_data_ov000_02245ee4);
    M2C_FIELD(native_data_ov000_02245ee4, s32 *, 0) = 0;
    M2C_FIELD(native_data_ov000_02245ee4, s16 *, 0x14) = 0x7C;
    M2C_FIELD(native_data_ov000_02245ee4, s16 *, 0x16) = 0x60;
    M2C_FIELD(native_data_ov000_02245ee4, u8 *, 0x20) = 7U;
    M2C_FIELD(native_data_ov000_02245ee4, u8 *, 0x21) = 1U;
    native_fn_ov000_0221863c();
    temp_r0 = native_fn_0205f98c(M2C_FIELD(native_data_ov000_02245ee4, s32 *, 0x1C), 0);
    native_fn_ov000_02219d70(temp_r0, 0);
    native_fn_02048a60(temp_r0, M2C_FIELD(native_data_ov000_02245ee4, s16 *, 0x14), M2C_FIELD(native_data_ov000_02245ee4, s16 *, 0x16));
    M2C_FIELD(temp_r0, s32 *, 0x7C) = (s32) (M2C_FIELD(temp_r0, s32 *, 0x7C) | 2);
    native_fn_02048a94(temp_r0, M2C_FIELD(native_data_ov000_02245ee4, u8 *, 0x20));
    return native_fn_02048a9c(temp_r0, M2C_FIELD(native_data_ov000_02245ee4, u8 *, 0x21));
}
