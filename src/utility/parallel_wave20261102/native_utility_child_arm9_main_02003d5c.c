typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_02003d5c(u32 arg0, u32 arg1) {
    u32 temp_r1;
    u32 temp_r2;

    temp_r2 = CHILD_FIELD(arg1, u32 *, 8);
    temp_r1 = CHILD_FIELD(arg1, u32 *, 0xC);
    if (temp_r2 != 0) {
        CHILD_FIELD(temp_r2, u32 *, 0xC) = temp_r1;
    } else {
        CHILD_FIELD(arg0, u32 *, 0) = temp_r1;
    }
    if (temp_r1 != 0) {
        CHILD_FIELD(temp_r1, u32 *, 8) = temp_r2;
    } else {
        CHILD_FIELD(arg0, u32 *, 4) = temp_r2;
    }
    return (u32) temp_r2;
}
