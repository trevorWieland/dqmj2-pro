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
extern u32 native_fn_ov001_021dbe5c();
extern u32 native_fn_ov001_02218644();
u32 native_ov001_022225bc(void *arg0) {
    void *temp_r5;
    s32 var_r6;
    s32 var_r7;

    temp_r5 = M2C_FIELD(arg0, void **, 0);
    var_r7 = M2C_FIELD(arg0, s32 *, 8);
    var_r6 = 0;
loop_1:
    if ((ov001_record_is_active_021db8d0(var_r7) != 0) && (native_fn_ov001_02218644(var_r7, 0x2B) != 0)) {
        if (((s32) M2C_FIELD(temp_r5, s8 *, 0x22F) >= 2) || ((s32) native_fn_ov001_021dbe5c(temp_r5) >= 0x5DC)) {
            return 1U;
        }
        return 0U;
    }
    var_r6 += 1;
    var_r7 += 0x440;
    if (var_r6 >= 3) {
        return 0U;
    }
    goto loop_1;
}
