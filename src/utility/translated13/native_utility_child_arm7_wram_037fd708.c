typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u16 native_utility_child_arm7_data_03805b54[];
void native_utility_child_arm7_wram_037fd708(s32 arg0) {
    *native_utility_child_arm7_data_03805b54 |= 1 << arg0;
}
