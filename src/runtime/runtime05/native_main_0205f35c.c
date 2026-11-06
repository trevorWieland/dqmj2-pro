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
extern u32 native_fn_02039fc4();
extern u32 native_fn_0205f318();
extern u32 native_fn_0205f404();
extern u8 native_data_021b8ae0[];
extern u8 native_data_021b8af0[];
u32 native_main_0205f35c(s32 arg0, s16 arg1) {
    s32 var_r4;
    void *temp_r5;

    var_r4 = arg0;
    if (var_r4 < 0) {
        var_r4 = (s32) native_fn_0205f318();
    }
    if (var_r4 >= 0) {
        temp_r5 = native_data_021b8af0 + (var_r4 * 8);
        native_fn_0205f404(var_r4, 0);
        if (native_fn_02039fc4(temp_r5, -1, -1, arg1, 0) != 0) {
            M2C_FIELD(temp_r5, s16 *, 4) = arg1;
            M2C_FIELD(temp_r5, s8 *, 6) = 0x7F;
            M2C_FIELD(native_data_021b8ae0, s8 *, 1) = 0;
        } else {
            M2C_FIELD(native_data_021b8ae0, s8 *, 1) = 0xA;
        }
    } else {
        M2C_FIELD(native_data_021b8ae0, s8 *, 1) = 7;
    }
    return (u32) var_r4;
}
