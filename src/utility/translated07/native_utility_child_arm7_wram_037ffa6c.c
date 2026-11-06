typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037ff6e4(u32, u32, u32, u32);
void native_utility_child_arm7_wram_037ffa6c(void *arg0, u32 arg1, u32 arg2, u32 arg3) {
    M2C_FIELD(arg0, s16 *, 0x20) = (s16) native_utility_child_arm7_thumb_037ff6e4(arg1, arg1, arg2, arg3);
}
