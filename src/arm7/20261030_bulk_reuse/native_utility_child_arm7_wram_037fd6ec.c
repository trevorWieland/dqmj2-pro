#define NULL ((void *)0)
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm7_wram_037fd6ec(void **arg0, void *arg1) {
    M2C_FIELD(arg1, void ***, 4) = arg0;
    M2C_FIELD(arg1, s32 *, 0) = 0;
    if (arg0 != NULL) {
        *arg0 = arg1;
    }
    return (u32) arg1;
}
