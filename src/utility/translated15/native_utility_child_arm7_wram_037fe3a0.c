typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fbc50(u32);
extern u16 native_utility_child_arm7_data_03805b74[];
extern u8 native_utility_child_arm7_data_03805b80[];
extern u32 native_utility_child_arm7_data_03805b7c[];
extern u32 native_utility_child_arm7_data_03805b78[];
void native_utility_child_arm7_wram_037fe3a0(void) {
    if (*native_utility_child_arm7_data_03805b74 == 0) {
        *native_utility_child_arm7_data_03805b74 = 1;
        M2C_FIELD(native_utility_child_arm7_data_03805b80, s32 *, 0) = 0;
        M2C_FIELD(native_utility_child_arm7_data_03805b80, s32 *, 4) = 0;
        native_utility_child_arm7_arm_037fbc50(4U);
        *native_utility_child_arm7_data_03805b7c = 0;
        *native_utility_child_arm7_data_03805b78 = 0;
    }
}
