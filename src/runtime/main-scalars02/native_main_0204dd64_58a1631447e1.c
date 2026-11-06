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
extern u8 native_data_02102d80[];
u32 native_main_0204dd64(s16 arg0) {
    s32 temp_r3;
    s32 var_ip;
    u32 var_lr;

    var_lr = 0;
    var_ip = 0;
loop_1:
    temp_r3 = var_ip * 2;
    if (*(s16 *)(native_data_02102d80 + temp_r3) != 0) {
        goto block_3;
    }
    *(s16 *)(native_data_02102d80 + temp_r3) = arg0;
    var_lr = 1;
    goto block_4;
block_3:
    var_ip += 1;
    if (var_ip < 0x20) {
        goto loop_1;
    }
block_4:
    return var_lr;
}
