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
extern u32 native_fn_02063628();
extern u32 native_fn_020649c0();
extern u32 native_fn_ov001_0222c92c();
void native_main_0204363c(void) {
    s16 temp_r0_2;
    s32 var_r4;
    void *temp_r0;

    native_fn_ov001_0222c92c();
    var_r4 = 0;
    do {
        temp_r0 = (void *) native_fn_020649c0(var_r4);
        temp_r0_2 = M2C_FIELD(temp_r0, s16 *, 0x2E);
        if ((s32) temp_r0_2 >= 0) {
            native_fn_02063628(temp_r0_2, M2C_FIELD(temp_r0, u8 *, 0x30));
        }
        var_r4 += 1;
    } while (var_r4 < 3);
}
