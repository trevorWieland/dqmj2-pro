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
extern u32 native_fn_0204b77c();
extern u32 native_fn_0204b904();
extern u32 ov000_display_context_02215698();
extern u8 native_data_ov000_02237f90[];
void native_ov000_02202630(void) {
    u8 var_r7;

    native_fn_0204b77c(ov000_display_context_02215698() + 0x10);
    var_r7 = 0;
    do {
        native_fn_0204b904((var_r7 * 0x48) + (s32) native_data_ov000_02237f90, 1);
        var_r7 += 1;
    } while ((u32) var_r7 < 4U);
}
