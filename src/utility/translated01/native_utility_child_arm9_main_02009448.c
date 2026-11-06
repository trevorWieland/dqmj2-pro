typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

void native_utility_child_arm9_main_02009448(void *arg0, s32 arg1) {
    M2C_FIELD(arg0, s32 *, 0xB4) = arg1;
}
