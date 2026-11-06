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
u32 native_main_02029964(void *arg0, s32 arg1, s32 arg2) {
    s32 var_r1;
    u16 temp_r3;
    void *temp_ip;

    temp_ip = M2C_FIELD(arg0, void **, 0x6C);
    if (temp_ip != NULL) {
        temp_r3 = M2C_FIELD(M2C_FIELD(temp_ip, void **, 8), u16 *, 4);
        var_r1 = M2C_FIELD(temp_ip, s32 *, 0) + arg1;
        if (var_r1 >= (s32) (temp_r3 << 0xC)) {
            if (arg2 != 0) {
                var_r1 = 0;
            } else {
                var_r1 = (temp_r3 << 0xC) - 1;
            }
        }
        M2C_FIELD(temp_ip, s32 *, 0) = var_r1;
        return 1U;
    }
    return 0U;
}
