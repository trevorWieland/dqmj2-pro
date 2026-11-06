typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_020035e8(u32, u32);
extern u32 native_utility_child_arm9_arm_020056dc(u32, u32);
extern u32 native_utility_child_arm9_arm_02005680(u32);
extern u8 native_utility_child_arm9_data_02027d40[];
u32 native_utility_child_arm9_main_02005498(void *arg0, s8 arg1) {
    u32 temp_r4;

    temp_r4 = M2C_FIELD(arg0, u32 *, 4);
    if (temp_r4 != 0) {
        native_utility_child_arm9_arm_020035e8(temp_r4, (u32) arg0);
        M2C_FIELD(arg0, u32 *, 4) = 0U;
    }
    native_utility_child_arm9_arm_020035e8((u32) native_utility_child_arm9_data_02027d40, (u32) arg0);
    M2C_FIELD(arg0, s8 *, 0x3D) = arg1;
    if (temp_r4 != 0) {
        native_utility_child_arm9_arm_020056dc(temp_r4, (u32) arg0);
    }
    return native_utility_child_arm9_arm_02005680((u32) arg0);
}
