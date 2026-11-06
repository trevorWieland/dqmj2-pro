typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200b0c8(void);
extern u32 native_utility_child_arm9_thumb_0200b104(void);
extern u32 native_utility_child_arm9_thumb_0200b1c0(void);
extern u32 native_utility_child_arm9_thumb_0200b4bc(u32);
extern u32 native_utility_child_arm9_thumb_0200b2ec(u32);
extern u32 native_utility_child_arm9_thumb_0200b140(void);
u32 native_utility_child_arm9_main_0200b44c(s32 arg0) {
    u32 temp_r0;
    u32 var_r0;

    if (native_utility_child_arm9_thumb_0200b0c8() == 0) {
        return 0U;
    }
    var_r0 = native_utility_child_arm9_thumb_0200b104();
    if (var_r0 == 0) {
        if (!(arg0 & 1)) {
            return 0U;
        }
        if ((s32) native_utility_child_arm9_thumb_0200b1c0() > 0) {
            do {

            } while (native_utility_child_arm9_thumb_0200b4bc(0U) != 0);
            temp_r0 = native_utility_child_arm9_thumb_0200b104();
            if (temp_r0 != 0) {
                return temp_r0;
            }
            goto block_11;
        }
        native_utility_child_arm9_thumb_0200b2ec(1U);
block_11:
        native_utility_child_arm9_thumb_0200b140();
        do {
            native_utility_child_arm9_thumb_0200b4bc(1U);
            var_r0 = native_utility_child_arm9_thumb_0200b104();
        } while (var_r0 == 0);
        
        return var_r0;
    }
    return var_r0;
}
