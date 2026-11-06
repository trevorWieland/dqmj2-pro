typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_0200a6a4(void);
extern u32 native_utility_child_arm9_thumb_0200f8dc(void);
extern u32 native_utility_child_arm9_data_0202cca0[];
void native_utility_child_arm9_main_02010a70(void) {
    if (*native_utility_child_arm9_data_0202cca0 != 0) {
        do {
            if (native_utility_child_arm9_arm_0200a6a4() == 0x80) {
                native_utility_child_arm9_thumb_0200f8dc();
            }
        } while (*native_utility_child_arm9_data_0202cca0 != 0);
    }
}
