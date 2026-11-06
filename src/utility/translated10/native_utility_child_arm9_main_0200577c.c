typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_020035d0(u32, u32);
extern u32 native_utility_child_arm9_arm_020035e8(u32, u32);
extern u32 native_utility_child_arm9_arm_020065e0(u32);
extern u8 native_utility_child_arm9_data_0202818c[];
u32 native_utility_child_arm9_main_0200577c(s32 arg0, void *arg1) {
    u32 temp_r0;
    s32 temp_r5;

    temp_r5 = (arg0 * 0x24) + (s32) native_utility_child_arm9_data_0202818c;
    temp_r0 = native_utility_child_arm9_arm_020035d0(temp_r5 + 0xC, 0U);
    if (temp_r0 == 0) {
        return 0U;
    }
    native_utility_child_arm9_arm_020035e8(temp_r5 + 0xC, temp_r0);
    M2C_FIELD(temp_r0, void **, 0xC) = arg1;
    M2C_FIELD(arg1, u32 *, 8) = temp_r0;
    native_utility_child_arm9_arm_020065e0(M2C_FIELD(temp_r0, u32 *, 8));
    return M2C_FIELD(temp_r0, u32 *, 8);
}
