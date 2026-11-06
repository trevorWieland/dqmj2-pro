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
extern u32 native_fn_02092ffc(void *);
extern u32 native_fn_0209302c(void *, const void *, u32);
extern u32 native_fn_020930ac(void *, void *);
extern u32 native_fn_020936bc(void *);
extern u32 native_fn_020936f4(void *, const void *, u32);
extern u32 native_fn_02093774(void *, void *);
extern u32 native_fn_020937dc(void *, const void *, u32);
u32 native_main_020918a4(s8 *arg0, u32 arg1, s32 arg2) {
    s32 temp_r0_2;
    s8 *temp_r0_3;
    s8 *temp_r0_4;
    u16 temp_r0;
    s32 var_r2;
    s32 var_r4;
    s32 temp_r6;
    s8 sp20[21];
    s8 *sp1C;
    s8 *sp18;
    s8 *sp14;
    s32 sp10;
    s32 spC;
    s32 sp8;
    s32 sp4;
    s32 sp0;

    var_r2 = arg2;
    temp_r0 = M2C_FIELD(arg0, u16 *, 0x32);
    switch (temp_r0) {
    case 4:
        spC = 0x10;
        sp8 = 0x10;
        var_r2 = 0;
        break;
    case 5:
        spC = 0x14;
        sp8 = 0x10;
        var_r2 = 0;
        break;
    }
    temp_r0_2 = (var_r2 + (spC + sp8)) * 2;
    sp4 = temp_r0_2;
    sp10 = 0;
    if (temp_r0_2 > 0) {
        sp0 = sp10;
        sp14 = arg0;
        sp14 = arg0 + 0x54;
        sp18 = arg0;
        sp18 = arg0 + 0x34;
        sp1C = arg0;
        sp1C = arg0 + 0x74;
        do {
            native_fn_020936bc(arg0 + 0x348);
            sp20[0] = sp10 + 0x41;
            var_r4 = 0;
            temp_r6 = sp10 + 1;
            if (temp_r6 > 0) {
                do {
                    native_fn_020936f4(arg0 + 0x348, sp20, 1);
                    var_r4 += 1;
                } while (var_r4 < temp_r6);
            }
            native_fn_020936f4(arg0 + 0x348, arg0, 0x30);
            native_fn_020936f4(arg0 + 0x348, sp14, 0x20);
            native_fn_020936f4(arg0 + 0x348, sp18, 0x20);
            native_fn_02093774(arg0 + 0x348, sp20 + 1);
            native_fn_02092ffc(arg0 + 0x3FC);
            native_fn_0209302c(arg0 + 0x3FC, arg0, 0x30);
            native_fn_0209302c(arg0 + 0x3FC, sp20 + 1, 0x14);
            native_fn_020930ac(arg0 + 0x3FC, &sp1C[sp0]);
            sp0 += 0x10;
            sp10 += 1;
        } while (sp0 < sp4);
    }
    if (M2C_FIELD(arg0, u8 *, 0x454) != 0) {
        temp_r0_3 = arg0 + 0x74;
        M2C_FIELD(arg0, s8 **, 0x1D4) = temp_r0_3;
        M2C_FIELD(arg0, s8 **, 0x1D8) = (s8 *) (M2C_FIELD(arg0, s8 **, 0x1D4) + (spC * 2));
        M2C_FIELD(arg0, s8 **, 0xBC) = &temp_r0_3[spC];
        M2C_FIELD(arg0, s8 **, 0xC0) = &(&M2C_FIELD(arg0, s8 **, 0xBC)[spC])[sp8];
    } else {
        temp_r0_4 = arg0 + 0x74;
        M2C_FIELD(arg0, s8 **, 0xBC) = temp_r0_4;
        M2C_FIELD(arg0, s8 **, 0xC0) = (s8 *) (M2C_FIELD(arg0, s8 **, 0xBC) + (spC * 2));
        M2C_FIELD(arg0, s8 **, 0x1D4) = &temp_r0_4[spC];
        M2C_FIELD(arg0, s8 **, 0x1D8) = &(&M2C_FIELD(arg0, s8 **, 0x1D4)[spC])[sp8];
    }
    native_fn_020937dc(arg0 + 0x1E0, M2C_FIELD(arg0, s8 **, 0x1D8), 0x10);
    return native_fn_020937dc(arg0 + 0xC8, M2C_FIELD(arg0, s8 **, 0xC0), 0x10);
}
