typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_038009e0(u32);
extern u8 native_utility_child_arm7_data_038066e4[];
u32 native_utility_child_arm7_wram_03800e74(u32 arg0, u32 arg1) {
    s32 temp_r1;
    s32 var_r4;
    u32 temp_r1_2;
    u8 *var_r0;

    var_r4 = 0;
    do {
        temp_r1 = 0x24 * var_r4;
        var_r0 = &native_utility_child_arm7_data_038066e4[temp_r1];
        if (((u32) (M2C_FIELD(&native_utility_child_arm7_data_038066e4[temp_r1], u8 *, 0) << 0x1F) >> 0x1F) != 0) {
            temp_r1_2 = M2C_FIELD(var_r0, u32 *, 0x20);
            if ((arg0 <= temp_r1_2) && (temp_r1_2 <= arg1)) {
                var_r0 = (u8 *) native_utility_child_arm7_thumb_038009e0((u32) var_r0);
            }
        }
        var_r4 += 1;
    } while (var_r4 < 0x10);
    return (u32) var_r0;
}
