typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define native_utility_child_arm7_data_04000204 ((volatile u16 *)0x4000204)
void native_utility_child_arm7_wram_03804724(void *arg0) {
    M2C_FIELD(arg0, s32 *, 0) = (s32) ((s32) (*native_utility_child_arm7_data_04000204 & 0xC) >> 2);
    M2C_FIELD(arg0, s32 *, 4) = (s32) ((s32) (*native_utility_child_arm7_data_04000204 & 0x10) >> 4);
    *native_utility_child_arm7_data_04000204 = (*native_utility_child_arm7_data_04000204 & ~0xC) | 0xC;
    *native_utility_child_arm7_data_04000204 &= ~0x10;
}
