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
extern u32 native_fn_ov000_021f8bb8();
extern u32 native_fn_ov000_021f8c84();
extern u32 native_fn_ov000_021f8d84();
extern u32 native_fn_ov000_021f8e6c();
void native_ov000_021f8b0c(void) {
    s8 var_r4;

    native_fn_ov000_021f8bb8();
    native_fn_ov000_021f8c84();
    native_fn_ov000_021f8d84();
    var_r4 = 3;
    do {
        native_fn_ov000_021f8e6c(var_r4);
        var_r4 += 1;
    } while ((s32) var_r4 <= 7);
}
