typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200a888(void);
#define native_utility_child_arm9_data_04000000 ((volatile u8 *)0x4000000)
u32 native_utility_child_arm9_main_0200a8a4(u32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    s32 var_r1;
    u32 temp_r1;
    u32 temp_r0;
    u32 var_r0;

    var_r0 = arg0;
    var_r1 = arg1;
    if (var_r0 == 0) {
        temp_r0 = var_r1 & 0xFF000000;
        switch (arg3) {
        case 0x0:
            var_r1 += arg2;
            break;
        case 0x800000:
            var_r1 -= arg2;
            break;
        }
        if ((temp_r0 == (u32)native_utility_child_arm9_data_04000000) || (temp_r0 >= 0x08000000U) || (var_r0 = 0xFF000000, temp_r1 = var_r1 & 0xFF000000, (temp_r1 == (u32)native_utility_child_arm9_data_04000000)) || (temp_r1 >= 0x08000000U)) {
            var_r0 = native_utility_child_arm9_thumb_0200a888();
        }
    }
    return var_r0;
}
