typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037fe94c(void);
extern u32 native_utility_child_arm7_thumb_037feab4(u32, u32);
extern u32 native_utility_child_arm7_thumb_037feae0(u32, u32);
extern u32 native_utility_child_arm7_thumb_03802835(u32, u32);
extern u32 native_utility_child_arm7_data_03807be4[];
u32 native_utility_child_arm7_wram_03802850(void) {
    u32 *var_r0;

    var_r0 = native_utility_child_arm7_data_03807be4;
    if (*native_utility_child_arm7_data_03807be4 == 0) {
        *native_utility_child_arm7_data_03807be4 = 1;
        native_utility_child_arm7_thumb_037fe94c();
        do {

        } while (native_utility_child_arm7_thumb_037feab4(0xEU, 0U) == 0);
        var_r0 = (u32 *) native_utility_child_arm7_thumb_037feae0(0xEU, (u32) native_utility_child_arm7_thumb_03802835);
    }
    return (u32) var_r0;
}
