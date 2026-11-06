typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200b018(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200b064(u32);
extern u32 native_utility_child_arm9_arm_02005548(u32);
u32 native_utility_child_arm9_main_02005648(void *arg0) {
    if (M2C_FIELD(arg0, u8 *, 0x2C) == 2) {
        native_utility_child_arm9_thumb_0200b018((u32) M2C_FIELD(arg0, u8 *, 0x3C), 0xFFFFFD2DU);
    }
    native_utility_child_arm9_thumb_0200b064((u32) M2C_FIELD(arg0, u8 *, 0x3C));
    return native_utility_child_arm9_arm_02005548((u32) arg0);
}
