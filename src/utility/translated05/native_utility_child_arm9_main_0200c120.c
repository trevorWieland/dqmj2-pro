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
extern u32 native_utility_child_arm9_thumb_020095f4(u32);
extern u32 native_utility_child_arm9_arm_0200a660(u32);
u32 native_utility_child_arm9_main_0200c120(void *arg0, s32 arg1, s32 arg2) {
    u32 sp4;
    s32 sp0;
    u32 var_r0;
    void *temp_r5;

    sp0 = arg2;
    temp_r5 = M2C_FIELD(arg0, void **, 0);
    M2C_FIELD(temp_r5, s32 *, 0x1C) = (s32) (M2C_FIELD(temp_r5, s32 *, 0x1C) | 0x200);
    var_r0 = M2C_FIELD(temp_r5, u32 (**)(void *, s32, s32, s32), 0x50)(temp_r5, arg1, M2C_FIELD(arg0, s32 *, 4), sp0);
    switch (var_r0) {
    case 0:
    case 1:
        M2C_FIELD(temp_r5, s32 *, 0x1C) = (s32) (M2C_FIELD(temp_r5, s32 *, 0x1C) & 0xFFFFFDFF);
        break;
    case 6:
        sp4 = native_utility_child_arm9_arm_0200a64c();
        if (M2C_FIELD(temp_r5, s32 *, 0x1C) & 0x200) {
            do {
                native_utility_child_arm9_thumb_020095f4((u32) (temp_r5 + 0xC));
            } while (M2C_FIELD(temp_r5, s32 *, 0x1C) & 0x200);
        }
        native_utility_child_arm9_arm_0200a660(sp4);
        var_r0 = M2C_FIELD(M2C_FIELD(temp_r5, void **, 0x24), u32 *, 0x14);
        break;
    }
    M2C_FIELD(arg0, s32 *, 4) = (s32) (M2C_FIELD(arg0, s32 *, 4) + sp0);
    return var_r0;
}
