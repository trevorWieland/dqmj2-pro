typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_03800a58(u32, u32);
extern u32 native_utility_child_arm7_thumb_03800080(u32, u32, u32, u32);
extern u32 native_utility_child_arm7_thumb_03800a08(u32, u32);
u32 native_utility_child_arm7_wram_03800030(u32 arg0, u32 arg1) {
    s32 var_r6;
    u32 temp_r0;
    u32 var_r4;

    var_r6 = 0;
    var_r4 = 0;
    do {
        temp_r0 = native_utility_child_arm7_thumb_03800a58(arg0, var_r4);
        if ((temp_r0 != 0) && (M2C_FIELD(temp_r0, s32 *, 0x28) != 0)) {
            if (native_utility_child_arm7_thumb_03800080(temp_r0, arg0, var_r4, arg1) == 0) {
                var_r6 = 1;
            } else {
                native_utility_child_arm7_thumb_03800a08(arg0, var_r4);
            }
        }
        var_r4 += 1;
    } while ((s32) var_r4 < 0x10);
    if (var_r6 == 0) {
        return 1U;
    }
    return 0U;
}
