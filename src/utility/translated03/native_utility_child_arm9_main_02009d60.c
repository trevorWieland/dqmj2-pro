typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_020099ac(u32);
extern u32 native_utility_child_arm9_thumb_020095a0(u32);
u32 native_utility_child_arm9_main_02009d60(void *arg0) {
    u32 var_r0;
    void *temp_r0;

    var_r0 = M2C_FIELD(arg0, u32 *, 0x88);
    if (var_r0 != 0) {
        do {
            temp_r0 = (void *) native_utility_child_arm9_thumb_020099ac((u32) (arg0 + 0x88));
            M2C_FIELD(temp_r0, s32 *, 0xC) = 0;
            M2C_FIELD(temp_r0, s32 *, 8) = 0;
            native_utility_child_arm9_thumb_020095a0((u32) temp_r0);
            var_r0 = M2C_FIELD(arg0, u32 *, 0x88);
        } while (var_r0 != 0);
    }
    return var_r0;
}
