typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027e0134(void);
extern u32 native_utility_child_arm7_arm_037fcccc(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_0380576c(void);
extern u32 native_utility_child_arm7_arm_038057c8(u32);
extern u32 native_utility_child_arm7_arm_037fe6ec(u32, u32, u32);
extern u8 native_utility_child_arm7_data_027f94f0[];
#define utility_shared_halfword_027fff98 ((volatile u16 *)0x027fff98)
extern u8 native_utility_child_arm7_data_027f8578[];
void native_utility_child_arm7_main_027e1c78(void *arg0) {
    u16 temp_r0_2;
    u32 temp_r0;
    u32 temp_r0_3;
    u32 var_r0;
    void *temp_r0_4;
    void *temp_r6;
    u8 temp_r1;
    u16 temp_r2;
    u8 var_r2;
    void *temp_r0_5;
    u16 *temp_r4;

    temp_r4 = M2C_FIELD(native_utility_child_arm7_data_027f94f0, u16 **, 0x550);
    temp_r6 = arg0 + 0x3C;
    temp_r1 = M2C_FIELD(arg0, u8 *, 0x1F);
    if (temp_r1 & 2) {
        var_r2 = (u8) ((s32) temp_r1 >> 2);
    } else {
        var_r2 = ((s32) temp_r1 >> 2) + 0x19;
    }
    temp_r0 = var_r2 ^ (*utility_shared_halfword_027fff98 * 2);
    *utility_shared_halfword_027fff98 = temp_r0 ^ (temp_r0 >> 0x10);
    temp_r0_2 = M2C_FIELD(temp_r4, u16 *, 0);
    if ((temp_r0_2 == 8) || (temp_r0_2 == 0xA)) {
        if (M2C_FIELD(temp_r4, u16 *, 0xBA) != M2C_FIELD(temp_r6, u16 *, 8)) {
            temp_r0_3 = native_utility_child_arm7_arm_027e0134();
            if (temp_r0_3 == 0) {
                var_r0 = 0;
            } else {
                M2C_FIELD(temp_r0_3, s32 *, 0) = 0x25;
                M2C_FIELD(temp_r0_3, s32 *, 4) = 1;
                M2C_FIELD(temp_r0_3, s32 *, 8) = 0x8002;
                var_r0 = native_utility_child_arm7_arm_037fcccc((u32) native_utility_child_arm7_data_027f8578, temp_r0_3, 0U);
            }
            if (var_r0 == 0) {
                temp_r0_4 = (void *) native_utility_child_arm7_arm_0380576c();
                M2C_FIELD(temp_r0_4, s16 *, 0) = 0x80;
                M2C_FIELD(temp_r0_4, s16 *, 2) = 8;
                M2C_FIELD(temp_r0_4, s16 *, 4) = 0x16;
                M2C_FIELD(temp_r0_4, s16 *, 6) = 0x25;
                native_utility_child_arm7_arm_038057c8((u32) temp_r0_4);
            }
        } else if (M2C_FIELD(M2C_FIELD(native_utility_child_arm7_data_027f94f0, u16 **, 0x550), u16 *, 0xC2) != 0) {
            temp_r0_5 = (void *) native_utility_child_arm7_arm_0380576c();
            M2C_FIELD(temp_r0_5, s16 *, 0) = 0x80;
            M2C_FIELD(temp_r0_5, s16 *, 2) = 0;
            M2C_FIELD(temp_r0_5, s16 *, 4) = 0x10;
            M2C_FIELD(temp_r0_5, u16 *, 6) = (u16) M2C_FIELD(temp_r6, u16 *, 8);
            M2C_FIELD(temp_r0_5, u16 *, 8) = (u16) M2C_FIELD(temp_r4, u16 *, 0);
            M2C_FIELD(temp_r0_5, u16 *, 0xA) = (u16) M2C_FIELD(arg0, u16 *, 0x16);
            temp_r2 = M2C_FIELD(temp_r0_5, u16 *, 0xA);
            if ((u32) temp_r2 <= 0x80U) {
                native_utility_child_arm7_arm_037fe6ec((u32) temp_r6, (u32) (temp_r0_5 + 0xC), (temp_r2 + 1) & ~1);
            }
            native_utility_child_arm7_arm_038057c8((u32) temp_r0_5);
        }
    }
}
