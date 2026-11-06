#define NULL ((void *)0)
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
extern u32 native_fn_0208a31c();
u32 native_main_0208b3a4(s32 arg0) {
    void *temp_r0;
    void *temp_r2;
    void *var_r3;

    temp_r0 = (void *) native_fn_0208a31c();
    var_r3 = NULL;
    temp_r2 = M2C_FIELD(temp_r0, void **, 0x2270);
    if ((temp_r2 != NULL) && ((u32) M2C_FIELD(temp_r0, u32 *, 0x2274) > 0xCU)) {
        var_r3 = M2C_FIELD(temp_r2, void **, 4);
        if (var_r3 != NULL) {
loop_3:
            if (M2C_FIELD(var_r3, s32 *, 4) != arg0) {
                var_r3 = M2C_FIELD(var_r3, void **, 0xC);
                if (var_r3 != NULL) {
                    goto loop_3;
                }
            }
        }
    }
    return (u32) var_r3;
}
