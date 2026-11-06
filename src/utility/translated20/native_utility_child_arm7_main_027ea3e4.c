typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define native_utility_child_arm7_data_0380fff4 ((volatile u32 *)0x380fff4)
#define native_utility_child_arm7_data_04808038 ((volatile u16 *)0x4808038)
void native_utility_child_arm7_main_027ea3e4(void) {
    M2C_FIELD(*native_utility_child_arm7_data_0380fff4, s16 *, 0x3EA) = 0;
    *native_utility_child_arm7_data_04808038 |= 2;
}
