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
extern u32 native_fn_02008c14();
extern u32 native_fn_0202b9cc();
u32 native_main_0202b6dc(void *arg0) {
    u32 temp_r0;
    void *var_r1;
    s32 temp_r5;
    u32 temp_r6;

    temp_r6 = M2C_FIELD(arg0, u32 *, 0x28);
    temp_r5 = M2C_FIELD(arg0, u32 *, 0x1C) - temp_r6;
    if ((u8) M2C_FIELD(arg0, s32 *, 0x20) & 2) {
        native_fn_02008c14(native_fn_0202b9cc(2), temp_r6, temp_r5);
    }
    var_r1 = M2C_FIELD(arg0, void **, 0x2C);
    if (var_r1 != NULL) {
        do {
            M2C_FIELD(var_r1, u32 *, 8) = (u32) M2C_FIELD(arg0, u32 *, 0x1C);
            var_r1 = M2C_FIELD(var_r1, void **, 0xC);
        } while (var_r1 != NULL);
    }
    temp_r0 = M2C_FIELD(arg0, u32 *, 0x1C);
    M2C_FIELD(arg0, u32 *, 0x28) = temp_r0;
    return temp_r0;
}
