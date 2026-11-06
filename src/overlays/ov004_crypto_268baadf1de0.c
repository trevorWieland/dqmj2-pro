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

u32 native_ov004_021d8a70(u8 *arg0) {
    u8 temp_r1;
    u8 temp_r1_2;
    s32 temp_r2_2;
    u8 temp_r2;
    u8 temp_ip;
    u8 *temp_lr;

    temp_r2_2 = M2C_FIELD(arg0, s32 *, 0);
    temp_r1 = M2C_FIELD(arg0, s32 *, 4) + 1 + temp_r2_2;
    temp_lr = arg0 + 0xC;
    temp_ip = *(temp_lr + temp_r1);
    temp_r1_2 = temp_r2_2 + (temp_ip + M2C_FIELD(arg0, s32 *, 8));
    temp_r2 = *(temp_lr + temp_r1_2);
    M2C_FIELD(arg0, s32 *, 4) = (s32) temp_r1;
    M2C_FIELD(arg0, s32 *, 8) = (s32) temp_r1_2;
    *(temp_lr + temp_r1_2) = temp_ip;
    *(temp_lr + temp_r1) = temp_r2;
    return (u32) M2C_FIELD((arg0 + (u8) (temp_ip + temp_r2)), u8 *, 0xC);
}

u32 native_ov004_021d8ac8(u8 *arg0) {
    u8 *var_r0;
    s32 var_ip;
    u32 temp_lr;

    var_r0 = arg0;
    var_ip = 0x03020100;
    temp_lr = var_r0 + 0x100;
    do {
        *(u32 *)var_r0 = var_ip ^ -1;
        var_r0 += 4;
        var_ip += 0x04040404;
    } while ((u32) var_r0 < temp_lr);
    return 0U;
}

u32 native_ov004_021d8da0(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    s32 var_r0;
    u8 sp0[268];

    func_ov004_021d89e4(&sp0, arg0, 0x10);
    if (func_ov004_021d8b00(&sp0, arg1, arg2, arg3) == -1U) {
        var_r0 = 1;
    } else {
        var_r0 = 0;
    }
    return 0 - var_r0;
}

u32 native_ov004_021d8df8(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    s32 var_r0;
    u8 sp0[268];

    func_ov004_021d89e4(&sp0, arg0, 0x10);
    if (func_ov004_021d8c18(&sp0, arg1, arg2, arg3) == -1U) {
        var_r0 = 1;
    } else {
        var_r0 = 0;
    }
    return 0 - var_r0;
}
