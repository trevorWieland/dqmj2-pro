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
extern u32 native_fn_ov001_021d92c0();
extern u32 native_fn_ov001_021d92dc();
extern u32 native_fn_ov001_021d92f8();
u32 native_ov001_021d85d4(void *arg0) {
    s32 var_r6;
    u32 var_r7;
    void *var_r8;

    var_r7 = 0;
    var_r8 = arg0;
    var_r6 = 0;
    do {
        if (M2C_FIELD(var_r8, u8 *, 0xF) != 0) {
            native_fn_ov001_021d92c0(var_r6, M2C_FIELD(var_r8, s32 *, 0), M2C_FIELD(var_r8, s32 *, 4), M2C_FIELD(var_r8, s32 *, 8));
            native_fn_ov001_021d92dc(var_r6, M2C_FIELD(var_r8, u8 *, 0xC), M2C_FIELD(var_r8, u8 *, 0xD), M2C_FIELD(var_r8, u8 *, 0xE));
            native_fn_ov001_021d92f8(var_r6, 1);
            var_r7 |= 1 << var_r6;
        }
        var_r6 += 1;
        var_r8 += 0x10;
    } while (var_r6 < 4);
    return var_r7;
}
