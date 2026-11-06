typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
extern u32 native_utility_child_arm9_arm_020035e8();
extern u32 native_utility_child_arm9_arm_0200542c();
extern u8 native_utility_child_arm9_data_0202860c[];
void native_utility_child_arm9_main_02005d20(void *arg0) {
    native_utility_child_arm9_arm_0200542c(M2C_FIELD(arg0, s32 *, 0x40));
    native_utility_child_arm9_arm_020035e8(native_utility_child_arm9_data_0202860c, arg0);
    M2C_FIELD(arg0, s32 *, 0x24) = (s32) (M2C_FIELD(arg0, s32 *, 0x24) & ~1);
}
