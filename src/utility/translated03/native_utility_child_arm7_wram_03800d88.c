typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_03800db8(u32);
extern u8 native_utility_child_arm7_data_03806188[];
extern u8 native_utility_child_arm7_data_03806190[];
u32 native_utility_child_arm7_wram_03800d88(u32 arg0) {
    if ((arg0 < (u32) M2C_FIELD(native_utility_child_arm7_data_03806188, u32 *, 0)) || (arg0 >= (u32) M2C_FIELD(native_utility_child_arm7_data_03806188, u32 *, 4))) {
        native_utility_child_arm7_thumb_03800db8(arg0);
    }
    return (u32) native_utility_child_arm7_data_03806190[arg0 - M2C_FIELD(native_utility_child_arm7_data_03806188, u32 *, 0)];
}
