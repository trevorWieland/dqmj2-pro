typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_0200a638(void);
extern u32 native_utility_child_arm9_arm_0200a87c(void);
void native_utility_child_arm9_main_020094a0(void) {
    native_utility_child_arm9_arm_0200a638();
loop_1:
    native_utility_child_arm9_arm_0200a87c();
    goto loop_1;
}
