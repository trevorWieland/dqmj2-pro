typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_arm7_fn_037fe12c(u32, u32, u32);
void native_arm7_main_027e030c(void *arg0, void *arg1) {
    s32 var_ip;
    s32 var_lr;
    s32 var_r3;
    u16 var_r0;
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
    if ((M2C_FIELD(arg1, u16 *, 0x12) != 0) && ((u32) M2C_FIELD(arg1, u16 *, 0x36) >= 8U)) {
        var_r0 = 8;
    } else {
        var_r0 = M2C_FIELD(arg1, u16 *, 0x36);
    }
    M2C_FIELD(arg0, u16 *, 0xE) = var_r0;
    temp_r3 = M2C_FIELD(arg0, u8 *, 0xA);
    if (temp_r3 != 0) {
        native_arm7_fn_037fe12c(M2C_FIELD(arg1, u32 *, 0), (u32) (arg0 + 0x10), (temp_r3 + 1) & ~1);
    }
}
