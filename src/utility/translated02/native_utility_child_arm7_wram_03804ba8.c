typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_038048d4(void);
extern u32 native_utility_child_arm7_thumb_037f837c(void);
u32 native_utility_child_arm7_wram_03804ba8(u32 arg0, s32 arg1) {
    if ((arg1 & 0x3F) == 2) {
        return native_utility_child_arm7_thumb_038048d4();
    }
    return native_utility_child_arm7_thumb_037f837c();
}
