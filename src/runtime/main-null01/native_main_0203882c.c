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
extern u32 native_fn_0202bb28();
extern u32 native_fn_02037ac0();
extern u8 native_data_020f47b8[];
u32 native_main_0203882c(void *arg0) {
    u32 temp_r0;
    void *temp_r1;

    temp_r0 = M2C_FIELD(arg0, u32 *, 8);
    if (temp_r0 == 0) {
        return temp_r0;
    }
    native_fn_02037ac0();
    temp_r1 = M2C_FIELD(arg0, void **, 0xC);
    if (temp_r1 != NULL) {
        M2C_FIELD(temp_r1, s32 *, 8) = 0;
        return 0U;
    }
    return native_fn_0202bb28((M2C_FIELD(arg0, s32 *, 0x10) * 0x24) + (s32) native_data_020f47b8 + 0xC, arg0);
}
