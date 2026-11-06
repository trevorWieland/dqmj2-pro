typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037ff7a8(u32);
u32 native_utility_child_arm7_wram_037ff640(void *arg0, s32 arg1) {
    M2C_FIELD(arg0, s32 *, 0x10) = 0xFFFE9680;
    M2C_FIELD(arg0, s8 *, 2) = 0;
    M2C_FIELD(arg0, s32 *, 0x34) = arg1;
    native_utility_child_arm7_thumb_037ff7a8((u32) (arg0 + 0x28));
    M2C_FIELD(arg0, u8 *, 3) = (u8) (M2C_FIELD(arg0, u8 *, 3) | 2);
    M2C_FIELD(arg0, u8 *, 3) = (u8) ((M2C_FIELD(arg0, u8 *, 3) & ~1) | 1);
    return 1U;
}
