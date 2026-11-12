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
u32 native_ov001_0221f398(void *arg0) {
    s32 temp_r0;
    s32 temp_r0_2;
    s32 var_r4;
    s32 var_r5;
    s32 var_r6;
    s32 var_r6_2;
    s32 var_r7;
    s32 var_r8;

    var_r5 = 0;
    var_r7 = M2C_FIELD(arg0, s32 *, 4);
    var_r8 = M2C_FIELD(arg0, s32 *, 8);
    var_r4 = 0x270F;
    var_r6 = 0;
    do {
        if (ov001_record_is_active_021db8d0(var_r8) != 0) {
            temp_r0 = (s32) native_fn_ov001_021dbe5c(var_r8);
            if (temp_r0 >= var_r5) {
                var_r5 = temp_r0;
            }
        }
        var_r6 += 1;
        var_r8 += 0x440;
    } while (var_r6 < 3);
    var_r6_2 = 0;
    do {
        if (ov001_record_is_active_021db8d0(var_r7) != 0) {
            temp_r0_2 = (s32) native_fn_ov001_021dbe5c(var_r7);
            if (temp_r0_2 <= var_r4) {
                var_r4 = temp_r0_2;
            }
        }
        var_r6_2 += 1;
        var_r7 += 0x440;
    } while (var_r6_2 < 3);
    if (var_r4 <= (s32) (var_r5 - 0x64)) {
        return 1U;
    }
    return 0U;
}
