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
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_02008e0c();
extern u32 native_fn_0201b248();
extern u8 native_data_021d1748[];
u32 native_main_02090960(void *arg0) {
    s32 var_r4;
    u8 *var_r5;
    u32 sp0;

    sp0 = native_fn_02007ff4();
    var_r4 = 0;
    var_r5 = native_data_021d1748;
    M2C_FIELD(arg0, s8 *, 0x30) = 0;
loop_1:
    if ((M2C_FIELD(var_r5, u8 *, 0x5A) != 0) && (M2C_FIELD(var_r5, s32 *, 0x54) == 0) && (M2C_FIELD(var_r5, u16 *, 0x58) == 0) && (native_fn_0201b248(var_r5, arg0 + 0x74, 0x20) == 0)) {
        native_fn_02008e0c(var_r5 + 0x20, arg0, 0x30);
        M2C_FIELD(arg0, s8 *, 0x30) = 1;
    } else {
        var_r4 += 1;
        var_r5 += 0x5C;
        if (var_r4 < 4) {
            goto loop_1;
        }
    }
    return native_fn_02008008(sp0);
}
