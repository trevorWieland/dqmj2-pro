typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200d478(u32, u32, u32);
extern u32 native_utility_child_arm9_arm_0200d09c(void);
extern u8 native_utility_child_arm9_data_0200d0b5[];
extern u8 native_utility_child_arm9_data_0202b814[];
u32 native_utility_child_arm9_main_0200d44c(u32 arg0) {
    u32 temp_r0;

    temp_r0 = native_utility_child_arm9_thumb_0200d478(arg0, (u32) native_utility_child_arm9_data_0200d0b5, 0U);
    M2C_FIELD(native_utility_child_arm9_data_0202b814, u32 *, 0x20) = temp_r0;
    if (temp_r0 == 0) {
        native_utility_child_arm9_arm_0200d09c();
    }
    return M2C_FIELD(native_utility_child_arm9_data_0202b814, u32 *, 0x20);
}
