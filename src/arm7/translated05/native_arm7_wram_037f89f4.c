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
extern u32 native_arm7_fn_037fb928(u32);
extern u32 native_arm7_fn_037fb8f0(u32);
u32 native_arm7_wram_037f89f4(void *arg0, void *arg1) {
    u32 temp_r0;
    void *temp_r1;

    if (M2C_FIELD(arg1, u16 *, 0xA) != 0xBF1D) {
        return 1U;
    }
    if (M2C_FIELD(arg1, u16 *, 8) != 0) {
        return 2U;
    }
    temp_r0 = native_arm7_fn_037fb928(0x01000000U);
    if (M2C_FIELD(arg0, u16 *, 8) == 0) {
        M2C_FIELD(arg1, void **, 0) = (void *)-1;
        M2C_FIELD(arg0, void **, 0) = arg1;
    } else {
        temp_r1 = M2C_FIELD(arg0, void **, 4);
        M2C_FIELD(arg1, void **, 0) = temp_r1;
        M2C_FIELD(temp_r1, void **, 4) = arg1;
    }
    M2C_FIELD(arg1, s32 *, 4) = -1;
    M2C_FIELD(arg1, u16 *, 8) = (u16) M2C_FIELD(arg0, u16 *, 0xA);
    M2C_FIELD(arg0, void **, 4) = arg1;
    M2C_FIELD(arg0, u16 *, 8) = (u16) (M2C_FIELD(arg0, u16 *, 8) + 1);
    native_arm7_fn_037fb8f0(temp_r0);
    return 0U;
}
