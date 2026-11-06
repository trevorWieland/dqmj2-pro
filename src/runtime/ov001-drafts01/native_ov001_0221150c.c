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
extern u32 native_fn_ov001_021f1a38();
extern u32 native_fn_ov001_021f1a44();
extern u32 native_fn_ov001_021f1a58();
extern u32 native_fn_ov001_021f1a90();
u32 native_ov001_0221150c(s16 arg0, s16 arg1, s32 arg2) {
    u32 temp_r0;
    u32 temp_r4;

    temp_r0 = native_fn_ov001_021f1a58();
    if (temp_r0 != 0x7F) {
        temp_r4 = native_fn_ov001_021f1a44();
        native_fn_ov001_021f1a38();
        M2C_FIELD(temp_r4, s8 *, 0x22) = 0x1E;
        native_fn_ov001_021f1a90(temp_r0);
        M2C_FIELD(temp_r4, s32 *, 0) = 9;
        M2C_FIELD(temp_r4, s16 *, 0x14) = arg0;
        M2C_FIELD(temp_r4, s16 *, 0x16) = arg1;
        M2C_FIELD(temp_r4, s8 *, 0x20) = 8;
        M2C_FIELD(temp_r4, s8 *, 0x21) = 3;
        M2C_FIELD(temp_r4, s32 *, 0x30) = arg2;
        M2C_FIELD(temp_r4, s32 *, 0x38) = 0;
    }
    return temp_r0;
}
