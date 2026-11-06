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
extern u32 native_utility_child_arm7_thumb_0380191c(u32, u32, u32);
extern u32 native_utility_child_arm7_thumb_037ff394(void);
extern u32 native_utility_child_arm7_thumb_037fe67c(u32);
extern u8 native_utility_child_arm7_data_02000000[];
extern u8 native_utility_child_arm7_data_03807324[];
u32 native_utility_child_arm7_wram_038018e0(u32 arg0, u32 arg1) {
    u32 temp_r4;

    temp_r4 = native_utility_child_arm7_thumb_037fe670();
    if (arg1 >= (u32) native_utility_child_arm7_data_02000000) {
        native_utility_child_arm7_thumb_0380191c((u32) native_utility_child_arm7_data_03807324, arg1, 0U);
    } else if (arg1 == 0) {
        native_utility_child_arm7_thumb_037ff394();
    }
    return native_utility_child_arm7_thumb_037fe67c(temp_r4);
}
