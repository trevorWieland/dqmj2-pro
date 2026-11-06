typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200ba04(u32, u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_0200bb20(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200c548(u32);
extern u32 native_utility_child_arm9_thumb_0200c4d4(u32);
u32 native_utility_child_arm9_main_0200c49c(void *arg0, u32 arg1, u32 arg2, u32 arg3) {
    u32 temp_r0;

    native_utility_child_arm9_thumb_0200bb20((u32) arg0, native_utility_child_arm9_thumb_0200ba04((u32) arg0, M2C_FIELD(arg0, u32 *, 0x10), arg2, arg3));
    temp_r0 = native_utility_child_arm9_thumb_0200c548(M2C_FIELD(arg0, u32 *, 8));
    if (temp_r0 != 0) {
        native_utility_child_arm9_thumb_0200c4d4(temp_r0);
    }
    if (M2C_FIELD(arg0, s32 *, 0x14) == 0) {
        return 1U;
    }
    return 0U;
}
