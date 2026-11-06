typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_020099ac(void *arg0) {
    void *temp_r1;
    void *temp_r2;

    temp_r2 = CHILD_FIELD(arg0, void **, 0);
    if (temp_r2 != 0) {
        temp_r1 = CHILD_FIELD(temp_r2, void **, 0x10);
        CHILD_FIELD(arg0, void **, 0) = temp_r1;
        if (temp_r1 != 0) {
            CHILD_FIELD(temp_r1, s32 *, 0x14) = 0;
        } else {
            CHILD_FIELD(arg0, s32 *, 4) = 0;
        }
    }
    return (u32) temp_r2;
}
