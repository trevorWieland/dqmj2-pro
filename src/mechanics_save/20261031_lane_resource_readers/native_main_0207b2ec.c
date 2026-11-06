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
#define NULL ((void *)0)
extern u32 native_fn_0203cc2c(u32, u32);
extern u8 native_data_020de4dc[];
extern u8 native_data_021c674c[];

u32 native_main_0207b2ec(s32 arg0) {
    u32 temp_r0;

    temp_r0 = native_fn_0203cc2c((u32)native_data_020de4dc, (u32)arg0);
    M2C_FIELD(native_data_021c674c, u32 *, 4) = temp_r0;
    if (temp_r0 != 0) {
        M2C_FIELD(native_data_021c674c, s8 *, 0) = arg0;
        M2C_FIELD(native_data_021c674c, s32 *, 8) = (s32) (temp_r0 + 8);
        return 1U;
    }
    M2C_FIELD(native_data_021c674c, s8 *, 0) = -1;
    M2C_FIELD(native_data_021c674c, s32 *, 8) = 0;
    return 0U;
}
