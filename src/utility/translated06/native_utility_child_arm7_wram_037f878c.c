typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fbc50(u32);
extern u32 native_utility_child_arm7_arm_037fbc8c(u32);
u32 native_utility_child_arm7_wram_037f878c(void *arg0, void *arg1) {
    u32 temp_r0;

    if (M2C_FIELD(arg1, u16 *, 0xA) != 0xBF1D) {
        return 1U;
    }
    if (M2C_FIELD(arg1, u16 *, 8) != M2C_FIELD(arg0, u16 *, 0xA)) {
        return 2U;
    }
    temp_r0 = native_utility_child_arm7_arm_037fbc50(0x01000000U);
    M2C_FIELD(arg0, u16 *, 8) = (u16) (M2C_FIELD(arg0, u16 *, 8) - 1);
    if (M2C_FIELD(arg0, u16 *, 8) == 0) {
        M2C_FIELD(arg0, void ***, 0) = (void **)-1;
        M2C_FIELD(arg0, void **, 4) = (void *)-1;
    } else if (arg1 == M2C_FIELD(arg0, void ***, 0)) {
        M2C_FIELD(arg0, void ***, 0) = (void **) M2C_FIELD(arg1, void ***, 4);
        *M2C_FIELD(arg0, void ***, 0) = (void *)-1;
    } else if (arg1 == M2C_FIELD(arg0, void **, 4)) {
        M2C_FIELD(arg0, void **, 4) = (void *) M2C_FIELD(arg1, void **, 0);
        M2C_FIELD(M2C_FIELD(arg0, void **, 4), s32 *, 4) = -1;
    } else {
        *M2C_FIELD(arg1, void ***, 4) = M2C_FIELD(arg1, void **, 0);
        M2C_FIELD(M2C_FIELD(arg1, void **, 0), void ***, 4) = (void **) M2C_FIELD(arg1, void ***, 4);
    }
    M2C_FIELD(arg1, u16 *, 8) = 0U;
    native_utility_child_arm7_arm_037fbc8c(temp_r0);
    return 0U;
}
