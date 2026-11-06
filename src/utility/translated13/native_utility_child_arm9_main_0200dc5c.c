typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_data_0202b83c[];
void native_utility_child_arm9_main_0200dc5c(s32 arg0, s32 arg1) {
    M2C_FIELD((*native_utility_child_arm9_data_0202b83c + (arg0 * 4)), s32 *, 0x18) = arg1;
}
