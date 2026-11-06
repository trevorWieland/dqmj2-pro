typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_02005b64(u32 *arg0, s16 arg1, s16 arg2) {
    u32 temp_r0;
    u32 temp_ip;

    temp_ip = *arg0;
    if (temp_ip == 0) {
        return (u32) arg0;
    }
    CHILD_FIELD(temp_ip, s16 *, 0x34) = 2;
    CHILD_FIELD(*arg0, s16 *, 0x38) = arg1;
    temp_r0 = *arg0;
    CHILD_FIELD(temp_r0, s16 *, 0x3A) = arg2;
    return (u32) temp_r0;
}
