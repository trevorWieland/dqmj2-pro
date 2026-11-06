typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200a4b0(u32);
extern u32 native_utility_child_arm9_thumb_0200912c(u32, u32);
extern u32 native_utility_child_arm9_thumb_020090a8(u32);
extern u32 native_utility_child_arm9_thumb_0200a541(void);
extern u16 native_utility_child_arm9_data_020295f0[];
extern u8 native_utility_child_arm9_data_020295f8[];
extern u16 native_utility_child_arm9_data_04000102[];
extern u16 native_utility_child_arm9_data_04000100[];
extern u32 native_utility_child_arm9_data_020295f4[];
void native_utility_child_arm9_main_0200a59c(void) {
    if (*native_utility_child_arm9_data_020295f0 == 0) {
        *native_utility_child_arm9_data_020295f0 = 1;
        native_utility_child_arm9_thumb_0200a4b0(0U);
        M2C_FIELD(native_utility_child_arm9_data_020295f8, s32 *, 0) = 0;
        M2C_FIELD(native_utility_child_arm9_data_020295f8, s32 *, 4) = 0;
        *native_utility_child_arm9_data_04000102 = 0;
        *native_utility_child_arm9_data_04000100 = 0;
        *native_utility_child_arm9_data_04000102 = 0xC1;
        native_utility_child_arm9_thumb_0200912c(8U, (u32) native_utility_child_arm9_thumb_0200a541);
        native_utility_child_arm9_thumb_020090a8(8U);
        *native_utility_child_arm9_data_020295f4 = 0;
    }
}
