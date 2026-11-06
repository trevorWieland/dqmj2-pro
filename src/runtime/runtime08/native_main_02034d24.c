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
u32 native_main_02034d24(void *arg0, u32 arg1) {
    void *temp_r2;
    void *temp_r3;

    temp_r3 = M2C_FIELD(arg0, void **, 0x1C);
    if (arg1 < (u32) M2C_FIELD(temp_r3, u16 *, 0)) {
        temp_r2 = M2C_FIELD(temp_r3, s32 *, 0xC) + (arg1 * 8);
        M2C_FIELD(arg0, void **, 0) = temp_r2;
        if (M2C_FIELD(temp_r2, u16 *, 4) != 0) {
            M2C_FIELD(arg0, void **, 4) = temp_r2;
        }
        return 1U;
    }
    return 0U;
}
