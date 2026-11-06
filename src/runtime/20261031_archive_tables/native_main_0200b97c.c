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
extern u32 native_fn_02008d78();
extern u32 native_fn_0200b200();
extern u32 native_fn_0200bd04();
extern u32 native_fn_0200bf2c();
extern u32 native_fn_0200c02c();
extern u32 native_fn_0200c180();
u32 native_main_0200b97c(u32 arg0, u32 arg1, u32 arg2) {
    s32 temp_r2;
    s32 temp_r2_2;
    u32 temp_r4;
    u32 temp_r5;
    u32 temp_r5_2;
    u32 sp4[18];

    temp_r4 = (M2C_FIELD(arg0, u32 *, 0x30) + M2C_FIELD(arg0, u32 *, 0x38) + 0x3F) & ~0x1F;
    if (temp_r4 <= arg2) {
        temp_r5 = (arg1 + 0x1F) & ~0x1F;
        native_fn_0200bd04(&sp4);
        temp_r2 = M2C_FIELD(arg0, s32 *, 0x2C);
        if (native_fn_0200bf2c(&sp4, (s32) arg0, temp_r2, temp_r2 + M2C_FIELD(arg0, u32 *, 0x30), -1) != 0) {
            if ((s32) native_fn_0200c180((u32) &sp4, temp_r5, M2C_FIELD(arg0, u32 *, 0x30)) < 0) {
                native_fn_02008d78(temp_r5, 0U, M2C_FIELD(arg0, u32 *, 0x30));
            }
            native_fn_0200c02c(&sp4);
        }
        M2C_FIELD(arg0, s32 *, 0x2C) = (s32) temp_r5;
        temp_r2_2 = M2C_FIELD(arg0, s32 *, 0x34);
        temp_r5_2 = temp_r5 + M2C_FIELD(arg0, u32 *, 0x30);
        if (native_fn_0200bf2c(&sp4, (s32) arg0, temp_r2_2, temp_r2_2 + M2C_FIELD(arg0, u32 *, 0x38), -1) != 0) {
            if ((s32) native_fn_0200c180((u32) &sp4, temp_r5_2, M2C_FIELD(arg0, u32 *, 0x38)) < 0) {
                native_fn_02008d78(temp_r5_2, 0U, M2C_FIELD(arg0, u32 *, 0x38));
            }
            native_fn_0200c02c(&sp4);
        }
        M2C_FIELD(arg0, s32 *, 0x34) = (s32) temp_r5_2;
        M2C_FIELD(arg0, u32 *, 0x44) = arg1;
        M2C_FIELD(arg0, u32 (**)(u32, u32, u32, u32), 0x50) = native_fn_0200b200;
        M2C_FIELD(arg0, s32 *, 0x1C) = (s32) (M2C_FIELD(arg0, s32 *, 0x1C) | 4);
    }
    return temp_r4;
}
