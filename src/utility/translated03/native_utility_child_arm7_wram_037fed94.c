typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037fedc8(void);
extern u32 native_utility_child_arm7_thumb_037fefa8(u32, u32);
extern u8 native_utility_child_arm7_data_04000508[];
extern u8 native_utility_child_arm7_data_04000509[];
u32 native_utility_child_arm7_wram_037fed94(void) {
    u32 var_r5;

    native_utility_child_arm7_thumb_037fedc8();
    var_r5 = 0;
    do {
        native_utility_child_arm7_thumb_037fefa8(var_r5, 1U);
        var_r5 += 1;
    } while ((s32) var_r5 < 0x10);
    *native_utility_child_arm7_data_04000508 = 0;
    *native_utility_child_arm7_data_04000509 = 0;
    return (u32) native_utility_child_arm7_data_04000509;
}
