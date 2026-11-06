typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_0200a64c(void);
extern u32 native_utility_child_arm9_thumb_020096a4(u32, u32);
extern u8 native_utility_child_arm9_data_02029300[];
u32 native_utility_child_arm9_main_020096ec(void) {
    native_utility_child_arm9_arm_0200a64c();
    return native_utility_child_arm9_thumb_020096a4(M2C_FIELD(native_utility_child_arm9_data_02029300, u32 *, 4), 0U);
}
