typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_020038f8(u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_020017a0(u32);
extern u32 native_utility_child_arm9_data_02027c98[];
u32 native_utility_child_arm9_main_0200176c(u32 arg0) {
    u32 temp_r0;
    void *temp_r0_2;
    u32 temp_r4;

    temp_r4 = native_utility_child_arm9_arm_020038f8(*native_utility_child_arm9_data_02027c98, 0xCU, 0x20U);
    temp_r0 = native_utility_child_arm9_thumb_020017a0(arg0);
    M2C_FIELD(temp_r4, u32 *, 8) = temp_r0;
    temp_r0_2 = temp_r0 + 0x20;
    M2C_FIELD(temp_r4, s32 *, 0) = (s32) (temp_r0_2 + 0x10);
    M2C_FIELD(temp_r4, void **, 4) = (void *) (temp_r0_2 + M2C_FIELD(temp_r0_2, s32 *, 4) + 8);
    return temp_r4;
}
