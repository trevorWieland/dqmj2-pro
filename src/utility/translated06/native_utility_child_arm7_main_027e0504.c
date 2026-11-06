typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fe814(u32, u32, u32, u32);
void native_utility_child_arm7_main_027e0504(void *arg0, void *arg1) {
    s32 var_ip;
    s32 var_lr;
    s32 var_r3;
    u8 temp_r3;

    M2C_FIELD(arg0, s32 *, 4) = (s32) M2C_FIELD(arg1, s32 *, 8);
    M2C_FIELD(arg0, u16 *, 8) = (u16) M2C_FIELD(arg1, u16 *, 0xC);
    if (M2C_FIELD(arg1, u16 *, 0x12) != 0) {
        var_r3 = 2;
    } else {
        var_r3 = 0;
    }
    if (M2C_FIELD(arg1, u16 *, 0xE) != 0) {
        var_ip = 1;
    } else {
        var_ip = 0;
    }
    if (M2C_FIELD(arg1, u16 *, 0x14) != 0) {
        var_lr = 4;
    } else {
        var_lr = 0;
    }
    M2C_FIELD(arg0, s8 *, 0xB) = (s8) (var_lr | (var_ip | var_r3));
    M2C_FIELD(arg0, u8 *, 0xA) = (u8) M2C_FIELD(arg1, u16 *, 4);
    M2C_FIELD(arg0, s16 *, 0) = 1;
    M2C_FIELD(arg0, s8 *, 2) = 1;
    M2C_FIELD(arg0, s8 *, 3) = 0;
    M2C_FIELD(arg0, u16 *, 0xC) = (u16) M2C_FIELD(arg1, u16 *, 0x34);
    M2C_FIELD(arg0, u16 *, 0xE) = (u16) M2C_FIELD(arg1, u16 *, 0x36);
    temp_r3 = M2C_FIELD(arg0, u8 *, 0xA);
    if (temp_r3 != 0) {
        native_utility_child_arm7_arm_037fe814(M2C_FIELD(arg1, u32 *, 0), (u32) (arg0 + 0x10), (temp_r3 + 1) & ~1, (u32) temp_r3);
    }
}
