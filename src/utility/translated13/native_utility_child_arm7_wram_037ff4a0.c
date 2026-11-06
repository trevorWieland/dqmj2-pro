typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_03801bf8(void);
extern u32 native_utility_child_arm7_thumb_037ff454(u32);
extern u32 native_utility_child_arm7_data_03805c68[];
u32 native_utility_child_arm7_wram_037ff4a0(u32 arg0) {
    u32 *var_r0;

    var_r0 = native_utility_child_arm7_data_03805c68;
    if (*native_utility_child_arm7_data_03805c68 == 0) {
        *native_utility_child_arm7_data_03805c68 = 1;
        native_utility_child_arm7_thumb_03801bf8();
        var_r0 = (u32 *) native_utility_child_arm7_thumb_037ff454(arg0);
    }
    return (u32) var_r0;
}
