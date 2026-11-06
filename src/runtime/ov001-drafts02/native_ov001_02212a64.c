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
extern u32 native_fn_0205f98c();
extern u32 native_fn_ov001_022129f4();
void native_ov001_02212a64(void *arg0) {
    u8 var_r4;

    var_r4 = 0;
    do {
        if (M2C_FIELD((void *) native_fn_0205f98c(M2C_FIELD(arg0, s32 *, 0x1C), var_r4), s32 *, 0x84) != 0) {
            native_fn_ov001_022129f4(arg0, var_r4, M2C_FIELD(arg0, s8 *, 0x24));
        }
        var_r4 += 1;
    } while ((u32) var_r4 < 0x18U);
}
