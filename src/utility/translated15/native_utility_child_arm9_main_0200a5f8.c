typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02009080(u32);
extern u16 native_utility_child_arm9_data_02029600[];
extern u8 native_utility_child_arm9_data_0202960c[];
extern u32 native_utility_child_arm9_data_02029608[];
extern u32 native_utility_child_arm9_data_02029604[];
void native_utility_child_arm9_main_0200a5f8(void) {
    if (*native_utility_child_arm9_data_02029600 == 0) {
        *native_utility_child_arm9_data_02029600 = 1;
        M2C_FIELD(native_utility_child_arm9_data_0202960c, s32 *, 0) = 0;
        M2C_FIELD(native_utility_child_arm9_data_0202960c, s32 *, 4) = 0;
        native_utility_child_arm9_thumb_02009080(4U);
        *native_utility_child_arm9_data_02029608 = 0;
        *native_utility_child_arm9_data_02029604 = 0;
    }
}
