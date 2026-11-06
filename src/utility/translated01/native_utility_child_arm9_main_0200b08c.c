typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02009dd5(u32);
extern u8 native_utility_child_arm9_data_02029638[];
u32 native_utility_child_arm9_main_0200b08c(void) {
    return native_utility_child_arm9_thumb_02009dd5((u32) native_utility_child_arm9_data_02029638);
}
