typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define native_utility_child_arm7_data_04000134 ((volatile u16 *)0x4000134)
void native_utility_child_arm7_wram_037febfc(s32 arg0, s32 arg1) {
    *native_utility_child_arm7_data_04000134 = arg1 | (~arg0 & *native_utility_child_arm7_data_04000134);
}
