#define NULL ((void *)0)
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
extern u8 native_data_020edd0c[];
u32 native_main_020283b4(void *arg0, u32 arg1) {
    void *var_r0;
    u32 temp_r3;

    var_r0 = arg0;
    if (var_r0 == NULL) {
        var_r0 = M2C_FIELD(native_data_020edd0c, void **, 8);
    }
    temp_r3 = M2C_FIELD(var_r0, u32 *, 0x14);
    M2C_FIELD(var_r0, u32 *, 0x14) = arg1;
    M2C_FIELD(var_r0, s8 *, 0x48) = 0;
    return temp_r3;
}
