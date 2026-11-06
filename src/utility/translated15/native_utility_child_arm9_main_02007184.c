typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_02007148(u32);
extern u32 native_utility_child_arm9_arm_020070d8(u32, u32);
extern u32 native_utility_child_arm9_arm_02007284(u32);
extern u8 native_utility_child_arm9_data_02028c40[];
extern u32 native_utility_child_arm9_data_02028750[];
u32 native_utility_child_arm9_main_02007184(void *arg0) {
    if (((s32) (M2C_FIELD(arg0, s32 *, 0x110) << 0x1F) >> 0x1F) == 0) {
        return (u32) arg0;
    }
    native_utility_child_arm9_arm_02007148((u32) arg0);
    M2C_FIELD(arg0, s32 (**)(void *), 0x164)(arg0);
    native_utility_child_arm9_arm_020070d8((u32) native_utility_child_arm9_data_02028c40, (u32) arg0);
    if (*native_utility_child_arm9_data_02028750 != 0) {
        native_utility_child_arm9_arm_020070d8(*native_utility_child_arm9_data_02028750 + 0x4E0, (u32) arg0);
    }
    return native_utility_child_arm9_arm_02007284((u32) arg0);
}
