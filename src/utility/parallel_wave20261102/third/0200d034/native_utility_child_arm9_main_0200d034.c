typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
#define NULL ((void *)0)
extern u32 native_utility_child_arm9_thumb_02009708();
extern u32 native_utility_child_arm9_thumb_0200957c();
extern u32 native_utility_child_arm9_arm_0200a64c();
extern u32 native_utility_child_arm9_arm_0200a660();
extern u32 native_utility_child_arm9_thumb_0200d028();
extern u32 native_utility_child_arm9_thumb_0200cf8d();
extern u32 native_utility_child_arm9_data_0202b3e8[];
extern u8 native_utility_child_arm9_data_0202b3ec[];
extern u8 native_utility_child_arm9_data_0202b810[];
u32 native_utility_child_arm9_main_0200d034(u32 arg0) {
    u32 temp_r4;

    temp_r4 = native_utility_child_arm9_arm_0200a64c();
    if (*native_utility_child_arm9_data_0202b3e8 == 0) {
        *native_utility_child_arm9_data_0202b3e8 = arg0;
        native_utility_child_arm9_thumb_0200d028(arg0 + 0xC4);
        native_utility_child_arm9_thumb_0200d028((u32) native_utility_child_arm9_data_0202b3ec);
        CHILD_FIELD(arg0, s32 *, 0xC0) = 0;
        native_utility_child_arm9_thumb_02009708(arg0, native_utility_child_arm9_thumb_0200cf8d, arg0, native_utility_child_arm9_data_0202b810, 0x400, 0x14);
        native_utility_child_arm9_thumb_0200957c((void *) arg0);
    }
    return native_utility_child_arm9_arm_0200a660(temp_r4);
}
