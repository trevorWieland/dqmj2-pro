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
extern u32 native_fn_ov001_021dbe5c();
u32 native_ov001_0221d0ec(void *arg0) {
    s32 var_r4;
    s32 var_r5;
    s32 var_r6;
    void *var_r7;

    var_r5 = 0;
    var_r7 = M2C_FIELD(arg0, void **, 8);
    var_r6 = 0;
    var_r4 = 0;
    do {
        if ((ov001_record_is_active_021db8d0(var_r7) != 0) && ((s32) M2C_FIELD(var_r7, s8 *, 0x22F) > -1) && ((s32) native_fn_ov001_021dbe5c(var_r7) > 1)) {
            var_r6 += 1;
            var_r5 += M2C_FIELD(M2C_FIELD(var_r7, void **, 0x1E8), u8 *, 0x9C);
        }
        var_r4 += 1;
        var_r7 += 0x440;
    } while (var_r4 < 3);
    if (var_r6 > 0) {
        var_r5 = (s32) native_fn_02026144(var_r5, var_r6);
    }
    if (var_r5 >= 5) {
        return 1U;
    }
    return 0U;
}
