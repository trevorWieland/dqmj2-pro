typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037ff390(void);
extern u32 native_utility_child_arm7_thumb_037ff38c(void);
extern u8 native_utility_child_arm7_data_02000000[];
u32 native_utility_child_arm7_wram_0380136c(s32 arg0, s32 arg1) {
    u32 var_r4;

    native_utility_child_arm7_thumb_037ff390();
    var_r4 = M2C_FIELD((arg0 + (arg1 * 4)), u32 *, 0x3C);
    if (var_r4 != 0) {
        if (var_r4 < (u32) native_utility_child_arm7_data_02000000) {
            var_r4 = (u32)((u8 *)arg0 + var_r4);
        }
    } else {
        var_r4 = 0;
    }
    native_utility_child_arm7_thumb_037ff38c();
    return var_r4;
}
