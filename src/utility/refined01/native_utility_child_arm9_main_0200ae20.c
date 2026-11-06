typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200a8f4(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200a8a4(u32, u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_01ff8238(u32, u32, u32, u32);
#define native_utility_child_arm9_data_040000b0 ((volatile u8 *)0x40000b0)
u32 native_utility_child_arm9_main_0200ae20(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    u32 var_r0;

    native_utility_child_arm9_thumb_0200a8f4(arg0, -1U);
    var_r0 = native_utility_child_arm9_thumb_0200a8a4(arg0, arg1, arg3, 0x01000000U);
    if (arg3 != 0) {
        do {

        } while (*(volatile u32 *)((((3 * arg0) + 2) * 4) + native_utility_child_arm9_data_040000b0) & 0x80000000);
        var_r0 = native_utility_child_arm9_thumb_01ff8238(arg0, arg1, arg2, 0xAF000001U);
    }
    return var_r0;
}
