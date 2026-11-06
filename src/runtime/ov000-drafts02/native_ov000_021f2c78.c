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
extern u32 native_fn_02008c58();
extern u32 native_fn_02049ad0();
extern u32 native_fn_ov000_021f2c64();
void native_ov000_021f2c78(void) {
    s8 var_r6;

    native_fn_ov000_021f2c64();
    var_r6 = 0;
    do {
        native_fn_02008c58(0, native_fn_02049ad0(var_r6), 0xC);
        var_r6 += 1;
    } while ((s32) var_r6 < 0x13);
}
