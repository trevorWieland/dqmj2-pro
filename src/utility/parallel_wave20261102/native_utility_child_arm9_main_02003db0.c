typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_02003ea8(u32);
extern u32 native_utility_child_arm9_arm_02003e78(u32);
u32 native_utility_child_arm9_main_02003db0(u32 arg0, s32 arg1) {
    u32 temp_r0;

    if (arg1 & 1) {
        native_utility_child_arm9_arm_02003ea8(arg0);
    }
    temp_r0 = arg1 & 2;
    if (temp_r0 == 0) {
        return temp_r0;
    }
    return native_utility_child_arm9_arm_02003e78(arg0);
}
