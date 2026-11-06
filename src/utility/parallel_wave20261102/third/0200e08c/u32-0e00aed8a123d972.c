typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200db20(void);
extern u32 native_utility_child_arm9_thumb_0200da80();
extern u32 native_utility_child_arm9_arm_02009e74(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200dc5c(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200db84();
u32 native_utility_child_arm9_main_0200e08c(u32 arg0, u32 arg1) {
    u16 temp_r0;
    u32 var_r0;
    void *temp_r1;
    u32 temp_r4;

    temp_r4 = native_utility_child_arm9_thumb_0200db20();
    var_r0 = native_utility_child_arm9_thumb_0200da80(5, 7, 9, 8, 0xA, 0xB);
    if (var_r0 == 0) {
        temp_r1 = CHILD_FIELD(temp_r4, void **, 4);
        temp_r0 = CHILD_FIELD(temp_r1, u16 *, 0);
        if ((temp_r0 == 7) || (temp_r0 == 9)) {
            if ((arg1 < 1U) || (arg1 > 0xFU)) {
                return 6U;
            }
            native_utility_child_arm9_arm_02009e74((u32) (temp_r1 + 0x182), 2U);
            if (!(CHILD_FIELD(CHILD_FIELD(temp_r4, void **, 4), u16 *, 0x182) & (1 << arg1))) {
                return 7U;
            }
            goto block_10;
        }
        if (arg1 != 0) {
            return 6U;
        }
block_10:
        native_utility_child_arm9_thumb_0200dc5c(0xDU, arg0);
        var_r0 = native_utility_child_arm9_thumb_0200db84(0xD, 1, 1 << arg1);
        if (var_r0 == 0) {
            var_r0 = 2;
        }
        
        return var_r0;
    }
    return var_r0;
}
