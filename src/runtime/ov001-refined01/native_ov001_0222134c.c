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
extern u32 ov001_record_is_active_021db8d0();
extern u32 native_fn_ov001_021e2c2c();
extern u32 native_fn_ov001_021e86cc();
u32 native_ov001_0222134c(void *arg0) {
    void *temp_r4;
    s32 var_r5;
    s32 var_r5_2;
    void *var_r6;
    void *var_r7;
    void *var_r8;

    temp_r4 = M2C_FIELD(arg0, void **, 0);
    var_r6 = M2C_FIELD(arg0, void **, 4);
    var_r7 = M2C_FIELD(arg0, void **, 8);
    var_r8 = var_r7;
    var_r5 = 0;
loop_1:
    if ((ov001_record_is_active_021db8d0(var_r8) != 0) && (native_fn_ov001_021e86cc(native_fn_ov001_021e2c2c(), M2C_FIELD(var_r8, u8 *, 0x31E), M2C_FIELD(var_r8, u8 *, 0x31F)) == 0)) {
        return 0U;
    }
    var_r5 += 1;
    var_r8 += 0x440;
    if (var_r5 >= 3) {
        var_r5_2 = 0;
loop_6:
        if ((ov001_record_is_active_021db8d0(var_r6) != 0) && (native_fn_ov001_021e86cc(native_fn_ov001_021e2c2c(), M2C_FIELD(var_r7, u8 *, 0x31E), M2C_FIELD(var_r7, u8 *, 0x31F)) != 0) && (M2C_FIELD(temp_r4, u8 *, 0x31F) != M2C_FIELD(var_r6, u8 *, 0x31F))) {
            return 0U;
        }
        var_r5_2 += 1;
        var_r6 += 0x440;
        var_r7 += 0x440;
        if (var_r5_2 >= 3) {
            return 1U;
        }
        goto loop_6;
    }
    goto loop_1;
}
