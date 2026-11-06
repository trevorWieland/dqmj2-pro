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
extern u32 native_fn_02061944();
extern u8 native_data_021c4f78[];
u32 native_main_0207237c(void) {
    s8 var_ip;
    u32 temp_r0;

    temp_r0 = native_fn_02061944();
    var_ip = 0;
loop_1:
    *(u32 *)(native_data_021c4f78 + (var_ip * 4)) = 0;
    var_ip += 1;
    if ((s32) var_ip < 2) {
        goto loop_1;
    }
    M2C_FIELD(temp_r0, s8 *, 0x26A) = 0;
    return temp_r0;
}
