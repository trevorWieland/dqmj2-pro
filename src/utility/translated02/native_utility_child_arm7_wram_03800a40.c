typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_03800b08(u32, u32, u32);
extern u32 native_utility_child_arm7_thumb_03800ae4(u32);
u32 native_utility_child_arm7_wram_03800a40(u32 arg0, u32 arg1) {
    native_utility_child_arm7_thumb_03800b08(arg0, arg1, -1U);
    return native_utility_child_arm7_thumb_03800ae4(arg0);
}
