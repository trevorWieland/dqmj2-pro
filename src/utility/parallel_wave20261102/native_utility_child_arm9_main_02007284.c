typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_02007284(u32 arg0) {
    s32 *temp_r2;

    temp_r2 = CHILD_FIELD(arg0, s32 **, 0x14C);
    if (temp_r2 != 0) {
        *temp_r2 = 0;
        CHILD_FIELD(arg0, s32 **, 0x14C) = 0;
    }
    CHILD_FIELD(arg0, s32 *, 0x110) = (s32) (CHILD_FIELD(arg0, s32 *, 0x110) & ~1);
    CHILD_FIELD(arg0, s32 *, 0x110) = (s32) (CHILD_FIELD(arg0, s32 *, 0x110) & ~4);
    CHILD_FIELD(arg0, s32 *, 0x110) = (s32) (CHILD_FIELD(arg0, s32 *, 0x110) & ~2);
    return (u32) arg0;
}
