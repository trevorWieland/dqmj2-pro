typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_020037ac(u32, u32);
extern u32 native_utility_child_arm9_arm_02003868(u32);
extern u32 native_utility_child_arm9_arm_02003720(u32, u32);
#define native_utility_child_arm9_data_02027cf4 ((volatile u32 *)0x2027cf4)
#define native_utility_child_arm9_data_02027cf8 ((volatile u8 *)0x2027cf8)
u32 native_utility_child_arm9_main_020037dc(u32 arg0, s32 arg1, s32 arg2, s32 arg3, u16 arg4) {
    CHILD_FIELD(arg0, s32 *, 0) = arg1;
    CHILD_FIELD(arg0, s32 *, 0x18) = arg2;
    CHILD_FIELD(arg0, s32 *, 0x1C) = arg3;
    CHILD_FIELD(arg0, s32 *, 0x20) = 0;
    CHILD_FIELD(arg0, s32 *, 0x20) = (s32) (CHILD_FIELD(arg0, s32 *, 0x20) & ~0xFF);
    CHILD_FIELD(arg0, s32 *, 0x20) = (s32) (CHILD_FIELD(arg0, s32 *, 0x20) | (u8) arg4);
    native_utility_child_arm9_arm_020037ac((u32) (arg0 + 0xC), 4U);
    if (*native_utility_child_arm9_data_02027cf4 == 0) {
        native_utility_child_arm9_arm_020037ac((u32) native_utility_child_arm9_data_02027cf8, 4U);
        *native_utility_child_arm9_data_02027cf4 = 1;
    }
    return native_utility_child_arm9_arm_02003720(native_utility_child_arm9_arm_02003868((u32) arg0), (u32) arg0);
}
