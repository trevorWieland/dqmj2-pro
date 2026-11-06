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
extern u32 native_fn_02008d78();
extern u32 native_fn_02008e0c();
extern u32 native_fn_02063abc();
extern u8 native_data_021d69d8[];
void native_main_020cf1f0(void) {
    u8 var_r9;
    s32 temp_r10;

    var_r9 = 0;
loop_1:
    temp_r10 = (var_r9 * 0x28) + (s32) native_data_021d69d8;
    native_fn_02008d78(temp_r10, 0, 0x24);
    native_fn_02008e0c(native_fn_02063abc(var_r9), temp_r10, 0x24);
    M2C_FIELD(temp_r10, s8 *, 0x24) = 0;
    var_r9 += 1;
    M2C_FIELD(temp_r10, s8 *, 0x25) = 0;
    M2C_FIELD(temp_r10, s8 *, 0x26) = 0;
    if ((u32) var_r9 < 9U) {
        goto loop_1;
    }
    return;
}
