typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_020035e8(u32, u32);
extern u32 native_utility_child_arm9_arm_02003720(u32, u32);
#define native_utility_child_arm9_data_02027d40 ((volatile u8 *)0x2027d40)
#define native_utility_child_arm9_data_02027d34 ((volatile u8 *)0x2027d34)
void native_utility_child_arm9_main_02005548(u32 arg0) {
    s32 *temp_r1;
    u32 temp_r1_2;
    u32 temp_r5;

    temp_r1 = CHILD_FIELD(arg0, s32 **, 0);
    if (temp_r1 != 0) {
        *temp_r1 = 0;
        CHILD_FIELD(arg0, s32 **, 0) = 0;
    }
    temp_r5 = CHILD_FIELD(arg0, u32 *, 4);
    native_utility_child_arm9_arm_020035e8(temp_r5, (u32) arg0);
    CHILD_FIELD(arg0, u32 *, 4) = 0U;
    temp_r1_2 = CHILD_FIELD(arg0, u32 *, 8);
    if (temp_r1_2 != 0) {
        native_utility_child_arm9_arm_02003720(temp_r5 + 0xC, temp_r1_2);
        CHILD_FIELD(CHILD_FIELD(arg0, u32 *, 8), s32 *, 0xC) = 0;
        CHILD_FIELD(arg0, u32 *, 8) = 0U;
    }
    native_utility_child_arm9_arm_020035e8((u32) native_utility_child_arm9_data_02027d40, (u32) arg0);
    native_utility_child_arm9_arm_02003720((u32) native_utility_child_arm9_data_02027d34, (u32) arg0);
    CHILD_FIELD(arg0, s8 *, 0x2C) = 0;
}
