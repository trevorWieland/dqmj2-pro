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
extern u32 native_fn_02042cd0();
extern u32 native_fn_020430b4();
u32 native_ov001_021f0bec(void *arg0) {
    s32 var_r2;
    u16 temp_r1;
    u32 var_r0;
    u32 var_r4;

    var_r4 = 0;
    if ((s32) M2C_FIELD((void *) native_fn_020430b4(M2C_FIELD(arg0, s16 *, 0x16A)), s16 *, 6) > 0) {
        var_r0 = native_fn_02042cd0();
        if (var_r0 != 0) {
            var_r2 = 0;
            do {
                temp_r1 = M2C_FIELD(var_r0, u16 *, 2);
                var_r2 += 1;
                var_r0 += 6;
                if (temp_r1 == 1) {
                    var_r4 += 1;
                }
            } while (var_r2 < 0x10);
        }
    }
    return var_r4;
}
