typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_0200742c(void *arg0) {
    s32 temp_r2;

    temp_r2 = M2C_FIELD(arg0, s32 *, 8);
    if (temp_r2 < (s32) M2C_FIELD(arg0, s32 *, 0xC)) {
        M2C_FIELD(arg0, s32 *, 8) = (s32) (temp_r2 + 1);
    }
    return (u32) arg0;
}
