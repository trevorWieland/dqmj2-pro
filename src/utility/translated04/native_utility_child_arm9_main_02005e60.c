typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200afc4(u32, u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_02010334(u32);
extern u32 native_utility_child_arm9_thumb_02010324(u32);
u32 native_utility_child_arm9_main_02005e60(void *arg0) {
    s32 temp_r0_2;
    u32 temp_r0;

    native_utility_child_arm9_thumb_0200afc4(M2C_FIELD(arg0, u32 *, 0x44), 0U, 1 << M2C_FIELD(arg0, s32 *, 0x40), 0U);
    temp_r0_2 = (s32) (M2C_FIELD(arg0, u32 *, 0x24) << 0x1E) >> 0x1F;
    if (temp_r0_2 != 0) {
        return (u32) temp_r0_2;
    }
    native_utility_child_arm9_thumb_02010334((u32) (arg0 + 8));
    native_utility_child_arm9_thumb_02010324((u32) (arg0 + 0x14));
    temp_r0 = M2C_FIELD(arg0, u32 *, 0x24) | 2;
    M2C_FIELD(arg0, u32 *, 0x24) = temp_r0;
    return temp_r0;
}
