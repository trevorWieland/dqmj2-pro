typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027f5a08(u32);
extern u32 native_utility_child_arm7_arm_027f5ad0(void);
extern u32 native_utility_child_arm7_arm_027f67bc(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_027f5a14(u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_main_027f5a20(u32 arg0, u32 arg1, u32 arg2) {
    native_utility_child_arm7_arm_027f5a08(M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u32 *, 0x314));
    native_utility_child_arm7_arm_027f5ad0();
    native_utility_child_arm7_arm_027f67bc(arg0, arg1, arg2);
    return native_utility_child_arm7_arm_027f5a14(M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u32 *, 0x314));
}
