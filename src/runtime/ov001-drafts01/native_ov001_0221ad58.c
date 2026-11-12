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
extern u32 native_fn_ov001_021dbcbc();
extern u32 native_fn_ov001_021dbd24();
u32 native_ov001_0221ad58(void *arg0) {
    s32 temp_r1;
    s32 var_r5;
    s32 var_r6;
    u32 temp_r4;

    var_r6 = M2C_FIELD(arg0, s32 *, 4);
    var_r5 = 0;
loop_1:
    if (ov001_record_is_active_021db8d0(var_r6) != 0) {
        temp_r4 = native_fn_ov001_021dbd24(var_r6);
        temp_r1 = native_fn_ov001_021dbcbc(var_r6) * 3;
        if ((s32) temp_r4 <= (s32) ((s32) (temp_r1 + ((u32) (temp_r1 >> 1) >> 0x1E)) >> 2)) {
            return 1U;
        }
    }
    var_r5 += 1;
    var_r6 += 0x440;
    if (var_r5 >= 3) {
        return 0U;
    }
    goto loop_1;
}
