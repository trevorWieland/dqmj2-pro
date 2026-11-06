typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_02005468(u32);
u32 native_utility_child_arm9_main_02005eb4(void *arg0) {
    u32 temp_r0;

    temp_r0 = M2C_FIELD(arg0, u32 *, 0x44);
    if (temp_r0 == 0) {
        return temp_r0;
    }
    native_utility_child_arm9_arm_02005468(temp_r0);
    M2C_FIELD(arg0, u32 *, 0x44) = 0U;
    M2C_FIELD(arg0, s32 *, 0x48) = 0;
    return 0U;
}
