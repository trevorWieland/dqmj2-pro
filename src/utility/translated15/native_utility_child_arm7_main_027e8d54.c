typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027e9640(void);
extern u32 native_utility_child_arm7_arm_027ea564(void);
extern u32 native_utility_child_arm7_arm_027e9b34(void);
extern u32 native_utility_child_arm7_arm_027e8e88(void);
extern u32 native_utility_child_arm7_arm_027e8da8(void);
extern u32 native_utility_child_arm7_arm_027eb530(u32, u32);
extern u32 native_utility_child_arm7_arm_027eca88(void);
extern u32 native_utility_child_arm7_arm_027ecb14(void);
extern u32 native_utility_child_arm7_arm_027ebe74(void);
extern u32 native_utility_child_arm7_arm_027eaa04(void);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_main_027e8d54(void) {
    native_utility_child_arm7_arm_027e9640();
    native_utility_child_arm7_arm_027ea564();
    native_utility_child_arm7_arm_027e9b34();
    native_utility_child_arm7_arm_027e8e88();
    native_utility_child_arm7_arm_027e8da8();
    native_utility_child_arm7_arm_027eb530(M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u32 *, 0x31C), (u32) M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u16 *, 0x320));
    native_utility_child_arm7_arm_027eca88();
    native_utility_child_arm7_arm_027ecb14();
    native_utility_child_arm7_arm_027ebe74();
    return native_utility_child_arm7_arm_027eaa04();
}
