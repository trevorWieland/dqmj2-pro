typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_0200a64c(void);
extern u32 native_utility_child_arm9_thumb_02009a08(u32);
extern u32 native_utility_child_arm9_thumb_020098c4(void);
extern u32 native_utility_child_arm9_arm_0200a660(u32);
u32 native_utility_child_arm9_main_020095a0(void *arg0) {
    s32 temp_r0;
    u32 temp_r7;
    void *temp_r0_2;

    temp_r7 = native_utility_child_arm9_arm_0200a64c();
    temp_r0 = M2C_FIELD(arg0, s32 *, 0);
    if (temp_r0 != 0) {
        if (temp_r0 != 0) {
            do {
                temp_r0_2 = (void *) native_utility_child_arm9_thumb_02009a08((u32) arg0);
                M2C_FIELD(temp_r0_2, s32 *, 0x64) = 1;
                M2C_FIELD(temp_r0_2, s32 *, 0x78) = 0;
                M2C_FIELD(temp_r0_2, s32 *, 0x80) = 0;
                M2C_FIELD(temp_r0_2, s32 *, 0x7C) = (s32) M2C_FIELD(temp_r0_2, s32 *, 0x80);
            } while (M2C_FIELD(arg0, s32 *, 0) != 0);
        }
        M2C_FIELD(arg0, s32 *, 4) = 0;
        M2C_FIELD(arg0, s32 *, 0) = (s32) M2C_FIELD(arg0, s32 *, 4);
        native_utility_child_arm9_thumb_020098c4();
    }
    return native_utility_child_arm9_arm_0200a660(temp_r7);
}
