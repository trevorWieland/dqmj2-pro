typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_02010df4(u32, u32, u32, u32);
u32 native_utility_child_arm9_main_02007444(void *arg0, u32 arg1, u32 arg2, u32 arg3) {
    s32 temp_r1;
    s32 temp_r2;
    s32 temp_r4;

    temp_r1 = M2C_FIELD(arg0, s32 *, 0xC);
    temp_r2 = M2C_FIELD(arg0, s32 *, 8);
    if (temp_r2 >= temp_r1) {
        return M2C_FIELD(arg0, u32 *, 4);
    }
    temp_r4 = M2C_FIELD(arg0, s32 *, 0);
    return temp_r4 + native_utility_child_arm9_arm_02010df4(temp_r2 * (M2C_FIELD(arg0, u32 *, 4) - temp_r4), (u32) temp_r1, (u32) temp_r2, arg3);
}
