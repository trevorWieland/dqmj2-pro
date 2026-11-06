typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_0380384c(u32);
extern u32 native_utility_child_arm7_thumb_03803868(u32);
extern u32 native_utility_child_arm7_thumb_037f837c(void);
extern u32 native_utility_child_arm7_data_038058a8[];
u32 native_utility_child_arm7_wram_03803968(u32 arg0) {
    switch (arg0) {
    case 1:
        native_utility_child_arm7_thumb_0380384c(0x10U);
        break;
    case 3:
        native_utility_child_arm7_thumb_03803868(0x30U);
        break;
    case 2:
        native_utility_child_arm7_thumb_0380384c(0x20U);
        native_utility_child_arm7_thumb_03803868(0x10U);
        break;
    default:
        native_utility_child_arm7_thumb_037f837c();
        break;
    }
    *native_utility_child_arm7_data_038058a8 = arg0;
    return (u32) native_utility_child_arm7_data_038058a8;
}
