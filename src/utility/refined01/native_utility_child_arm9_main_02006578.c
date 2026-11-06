typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_02003de8(u32, u32, u32);
extern u32 native_utility_child_arm9_arm_020035bc(u32, u32);
extern u32 native_utility_child_arm9_arm_02003720(u32, u32);
u32 native_utility_child_arm9_main_02006578(u32 *arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4) {
    u32 temp_r0;
    u32 temp_r0_2;

    temp_r0 = native_utility_child_arm9_arm_02003de8(*arg0, ((arg1 + 0x1F) & ~0x1F) + 0x20, 0x20U);
    if (temp_r0 == 0) {
        return 0U;
    }
    temp_r0_2 = native_utility_child_arm9_arm_020035bc((u32) ((u8 *)arg0 + 4), 0U);
    M2C_FIELD(temp_r0, s32 *, 8) = arg1;
    M2C_FIELD(temp_r0, s32 *, 0xC) = arg2;
    M2C_FIELD(temp_r0, s32 *, 0x10) = arg3;
    M2C_FIELD(temp_r0, s32 *, 0x14) = arg4;
    native_utility_child_arm9_arm_02003720(temp_r0_2, temp_r0);
    return temp_r0 + 0x20;
}
