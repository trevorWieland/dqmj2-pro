typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037fe670(void);
extern u32 native_utility_child_arm7_thumb_037fe67c(u32);
extern u32 native_utility_child_arm7_thumb_038023ac(u32);
extern u32 native_utility_child_arm7_thumb_03802ae8(u32);
extern u8 native_utility_child_arm7_data_03808080[];
extern u32 native_utility_child_arm7_data_03807bf0[];
extern u8 native_utility_child_arm7_data_03808070[];
u32 native_utility_child_arm7_wram_03802bd0(s32 arg0) {
    u32 temp_r0;

loop_1:
    temp_r0 = native_utility_child_arm7_thumb_037fe670();
    if (*native_utility_child_arm7_data_03807bf0 != 0) {
        native_utility_child_arm7_thumb_037fe67c(temp_r0);
        native_utility_child_arm7_thumb_038023ac((u32) native_utility_child_arm7_data_03808080);
        goto loop_1;
    }
    native_utility_child_arm7_thumb_03802ae8(4U);
    M2C_FIELD(native_utility_child_arm7_data_03808070, s32 *, 0x18) = arg0;
    return native_utility_child_arm7_thumb_037fe67c(temp_r0);
}
