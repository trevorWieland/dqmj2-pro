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
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_ov000_021df950();
extern u8 native_data_ov000_0222baf4[];
extern u8 native_data_ov000_02243e3c[];
u32 native_ov000_02212c94(u8 arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4, u8 arg5, u8 arg6, s16 arg7) {
    s32 temp_ip;
    s32 var_lr;
    s32 var_r4;
    u8 *var_r5;

    var_r5 = native_data_ov000_02243e3c;
    var_r4 = -1;
    var_lr = 0;
loop_1:
    if (M2C_FIELD(var_r5, u8 *, 0x105) == 0) {
        var_r4 = var_lr;
    } else {
        var_lr += 1;
        var_r5 += 0x10C;
        if (var_lr < 0x10) {
            goto loop_1;
        }
    }
    if (var_r4 >= 0) {
        temp_ip = (var_r4 * 0x10C) + (s32) native_data_ov000_02243e3c;
        M2C_FIELD(temp_ip, s32 *, 0x70) = arg1;
        M2C_FIELD(temp_ip, s32 *, 0x74) = arg2;
        M2C_FIELD(temp_ip, s32 *, 0x78) = arg3;
        M2C_FIELD(temp_ip, s32 *, 0x88) = 0;
        M2C_FIELD(temp_ip, s32 *, 0x8C) = arg4;
        M2C_FIELD(temp_ip, s32 *, 0x90) = 0;
        M2C_FIELD(temp_ip, s32 *, 0x7C) = 0x1000;
        M2C_FIELD(temp_ip, s32 *, 0x80) = 0x1000;
        M2C_FIELD(temp_ip, s32 *, 0x84) = 0x1000;
        M2C_FIELD(temp_ip, u8 *, 0x106) = arg0;
        M2C_FIELD(temp_ip, u8 *, 0x107) = arg5;
        M2C_FIELD(temp_ip, s16 *, 0x100) = arg7;
        M2C_FIELD(temp_ip, u8 *, 0x108) = arg6;
        M2C_FIELD(temp_ip, s8 *, 0x105) = 1;
        native_fn_ov000_021df950(*(s16 *)(native_data_ov000_0222baf4 + (M2C_FIELD(temp_ip, u8 *, 0x106) * 2)));
    }
    return (u32) var_r4;
}
