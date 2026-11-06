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
extern u8 native_data_021d4d68[];
extern u8 native_data_021d4ef4[];
u32 native_main_020c3948(s32 arg0) {
    s32 temp_ip;
    u32 temp_ip_2;
    u8 var_lr;
    u8 var_lr_2;

    if (arg0 == 0) {
        return 0U;
    }
    var_lr = 0;
loop_3:
    temp_ip_2 = (var_lr * 0x84) + (s32) native_data_021d4d68;
    if (arg0 == M2C_FIELD(temp_ip_2, s32 *, 0x14)) {
        return temp_ip_2;
    }
    var_lr += 1;
    if ((u32) var_lr >= 3U) {
        var_lr_2 = 0;
loop_7:
        temp_ip = var_lr_2 * 0x84;
        if (arg0 == M2C_FIELD((native_data_021d4d68 + temp_ip), s32 *, 0x1A0)) {
            return (u32) (native_data_021d4ef4 + temp_ip);
        }
        var_lr_2 += 1;
        if ((u32) var_lr_2 >= 3U) {
            return 0U;
        }
        goto loop_7;
    }
    goto loop_3;
}
