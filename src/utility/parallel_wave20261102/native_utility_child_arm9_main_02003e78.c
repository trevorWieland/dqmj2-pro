typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_02003e78(u32 arg0) {
    u32 var_r3;
    u32 temp_r2;
    u32 temp_r0;

    temp_r2 = arg0 + 0x24;
    var_r3 = CHILD_FIELD(temp_r2, u32 *, 8);
    if (var_r3 != 0) {
        do {
            CHILD_FIELD(var_r3, u32 *, 8) = (u32) CHILD_FIELD(arg0, u32 *, 0x1C);
            var_r3 = CHILD_FIELD(var_r3, u32 *, 0xC);
        } while (var_r3 != 0);
    }
    temp_r0 = CHILD_FIELD(arg0, u32 *, 0x1C);
    CHILD_FIELD(temp_r2, u32 *, 4) = temp_r0;
    return temp_r0;
}
