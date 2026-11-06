typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200db20(void);
extern u32 native_utility_child_arm9_thumb_0200db0c(void);
extern u32 native_utility_child_arm9_arm_02009e74(u32, u32);
u32 native_utility_child_arm9_main_0200de60(void) {
    u16 temp_r1;
    u32 temp_r0;
    u32 temp_r4;

    temp_r4 = native_utility_child_arm9_thumb_0200db20();
    if (native_utility_child_arm9_thumb_0200db0c() != 0) {
        return 0U;
    }
    native_utility_child_arm9_arm_02009e74(M2C_FIELD(temp_r4, u32 *, 4), 2U);
    temp_r0 = M2C_FIELD(temp_r4, u32 *, 4);
    temp_r1 = M2C_FIELD(temp_r0, u16 *, 0);
    switch (temp_r1) {
    case 9:
        native_utility_child_arm9_arm_02009e74(temp_r0 + 0x182, 2U);
        if (M2C_FIELD(M2C_FIELD(temp_r4, u32 *, 4), u16 *, 0x182) == 0) {
            return 0U;
        }
    case 10:
    case 11:
        native_utility_child_arm9_arm_02009e74(M2C_FIELD(temp_r4, u32 *, 4) + 0xBC, 2U);
        return (u32) M2C_FIELD(M2C_FIELD(temp_r4, u32 *, 4), u16 *, 0xBC);
    default:
        return 0U;
    }
}
