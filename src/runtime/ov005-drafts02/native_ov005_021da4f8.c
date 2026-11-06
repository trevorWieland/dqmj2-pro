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
extern u32 native_fn_02008c14();
void native_ov005_021da4f8(void *arg0, s32 arg1, s32 arg2) {
    void *temp_r4;
    void *temp_r1;
    s32 var_ip;

    var_ip = 0;
    temp_r4 = M2C_FIELD(M2C_FIELD(M2C_FIELD(arg0, void **, 0x20), void **, 0xC), void **, 0x24);
    M2C_FIELD(arg0, s32 *, 0) = 0;
    M2C_FIELD(arg0, s32 *, 4) = 0;
    M2C_FIELD(arg0, s16 *, 0xC) = 0;
    M2C_FIELD(arg0, s32 *, 0x10) = 0;
    M2C_FIELD(arg0, s32 *, 0x14) = 0;
    M2C_FIELD(arg0, s32 *, 0x18) = 0;
    M2C_FIELD(temp_r4, s16 *, 0x168) = (s16) (arg1 - 8);
    M2C_FIELD(temp_r4, s16 *, 0x16A) = (s16) (arg2 - 8);
loop_1:
    temp_r1 = temp_r4 + (var_ip * 2) + 0x100;
    var_ip += 1;
    M2C_FIELD(temp_r1, s16 *, 0x6C) = 0;
    if (var_ip < 2) {
        goto loop_1;
    }
    M2C_FIELD(temp_r4, s8 *, 0) = 0;
    M2C_FIELD(temp_r4, s32 *, 8) = 0;
    M2C_FIELD(temp_r4, s8 *, 1) = 5;
    M2C_FIELD(temp_r4, s8 *, 4) = 0;
    M2C_FIELD(temp_r4, s8 *, 5) = 0;
    native_fn_02008c14(0, temp_r4 + 0x10, 0x158);
    M2C_FIELD(temp_r4, s32 *, 0x170) = 1;
    return;
}
