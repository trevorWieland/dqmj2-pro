typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_0200d6b0(void *arg0) {
    return M2C_FIELD(arg0, s32 *, 8) + (0x3C * (M2C_FIELD(arg0, s32 *, 4) + (0x3C * M2C_FIELD(arg0, s32 *, 0))));
}
