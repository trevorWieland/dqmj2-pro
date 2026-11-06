typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fe5fc(u32);
extern u32 native_utility_child_arm7_arm_037fe41c(void);
extern u32 native_utility_child_arm7_arm_037fe608(void);
void native_utility_child_arm7_wram_037fe5e0(void) {
    native_utility_child_arm7_arm_037fe5fc(0U);
loop_1:
    native_utility_child_arm7_arm_037fe41c();
    native_utility_child_arm7_arm_037fe608();
    goto loop_1;
}
