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
extern u32 native_fn_ov001_021db410();
extern u32 native_fn_ov001_021db438();
extern u32 native_fn_ov001_021e34f0();
extern u32 native_fn_ov001_02218010();
extern u32 native_fn_ov001_0221806c();
u32 native_ov001_021d94cc(u32 arg0, u32 arg1) {
    s32 var_r6;
    u32 temp_r0;

    native_fn_ov001_021e34f0();
    if (native_fn_ov001_0221806c() != 0) {
        native_fn_ov001_02218010(arg1);
    }
    var_r6 = 0;
    do {
        native_fn_ov001_021db410(native_fn_ov001_021db438(0, var_r6), arg0);
        temp_r0 = native_fn_ov001_021db410(native_fn_ov001_021db438(1, var_r6), arg1);
        var_r6 += 1;
    } while (var_r6 < 3);
    return temp_r0;
}
