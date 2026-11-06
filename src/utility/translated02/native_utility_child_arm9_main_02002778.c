typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02007618(u32, u32);
extern u8 native_utility_child_arm9_data_02027cd8[];
u32 native_utility_child_arm9_main_02002778(void) {
    if (native_utility_child_arm9_thumb_02007618((u32) (M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4) + 0xC0), M2C_FIELD(M2C_FIELD(native_utility_child_arm9_data_02027cd8, void **, 4), u32 *, 0x7E0)) == 1) {
        return 1U;
    }
    return 0U;
}
