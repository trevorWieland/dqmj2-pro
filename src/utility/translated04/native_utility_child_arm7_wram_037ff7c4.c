typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037fefa8(u32, u32);
extern u8 native_utility_child_arm7_data_038061a4[];
void native_utility_child_arm7_wram_037ff7c4(u32 arg0, u32 arg1) {
    u32 temp_r2;
    u32 var_r4;
    u8 *temp_r1;
    u8 temp_r0;

    var_r4 = 0;
    do {
        temp_r1 = &native_utility_child_arm7_data_038061a4[0x54 * var_r4];
        temp_r0 = M2C_FIELD(temp_r1, u8 *, 3);
        if ((((u32) (temp_r0 << 0x1F) >> 0x1F) != 0) && (M2C_FIELD(temp_r1, u8 *, 1) == 0)) {
            temp_r2 = M2C_FIELD(temp_r1, u32 *, 0x44);
            if ((arg0 <= temp_r2) && (temp_r2 <= arg1)) {
                M2C_FIELD(temp_r1, u8 *, 3) = (u8) (temp_r0 & ~2);
                native_utility_child_arm7_thumb_037fefa8(var_r4, 0U);
            }
        }
        var_r4 = (u32) (u8) (var_r4 + 1);
    } while (var_r4 < 0x10U);
}
