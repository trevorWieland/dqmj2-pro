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
extern u32 native_fn_02026144();
extern u32 ov001_record_is_active_021db8d0();
extern u32 native_fn_ov001_02218524();
u32 native_ov001_0221cae4(void *arg0) {
    s32 var_r5;
    s32 var_r6;
    s32 var_r7;
    void *var_r8;

    var_r6 = 0;
    var_r8 = M2C_FIELD(arg0, void **, 8);
    var_r7 = 0;
    var_r5 = 0;
    do {
        if ((ov001_record_is_active_021db8d0(var_r8) != 0) && (M2C_FIELD(var_r8, s8 *, 0x23E) == 0) && (native_fn_ov001_02218524(var_r8, 0x80) != 0)) {
            var_r7 += 1;
            var_r6 += M2C_FIELD(M2C_FIELD(var_r8, void **, 0x1E8), u8 *, 0x94);
        }
        var_r5 += 1;
        var_r8 += 0x440;
    } while (var_r5 < 3);
    if (var_r7 > 0) {
        var_r6 = (s32) native_fn_02026144(var_r6, var_r7);
    }
    if (var_r6 >= 5) {
        return 1U;
    }
    return 0U;
}
