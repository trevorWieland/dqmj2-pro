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
u32 native_main_0202b834(void *arg0, s32 arg1) {
    void *var_r3;

    var_r3 = M2C_FIELD(arg0, void **, 0x2C);
    if ((arg1 != 0) && (var_r3 != NULL)) {
loop_4:
        if (M2C_FIELD(var_r3, s32 *, 0) != arg1) {
            var_r3 = M2C_FIELD(var_r3, void **, 0xC);
            if (var_r3 != NULL) {
                goto loop_4;
            }
        }
    }
    if (var_r3 == NULL) {
        return 0U;
    }
    M2C_FIELD(arg0, s32 *, 0x24) = (s32) M2C_FIELD(var_r3, s32 *, 4);
    M2C_FIELD(arg0, s32 *, 0x28) = (s32) M2C_FIELD(var_r3, s32 *, 8);
    M2C_FIELD(arg0, void **, 0x2C) = (void *) M2C_FIELD(var_r3, void **, 0xC);
    return 1U;
}
