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
extern u32 native_fn_0207afec();
extern u32 ov001_record_is_active_021db8d0();
u32 native_ov001_0221b0b4(void *arg0) {
    s32 temp_r6;
    s32 var_r7;
    s32 var_r8;
    void *temp_r9;
    void *var_r10;

    var_r7 = 0;
    temp_r6 = M2C_FIELD(arg0, s32 *, 4);
loop_1:
    var_r10 = temp_r6 + (var_r7 * 0x440);
    if (ov001_record_is_active_021db8d0(var_r10) != 0) {
        var_r8 = 0;
        if ((s32) M2C_FIELD(var_r10, u8 *, 0x323) > 0) {
            temp_r9 = var_r10;
loop_4:
            if (M2C_FIELD((void *) native_fn_0207afec(M2C_FIELD(var_r10, u8 *, 0x35E)), s16 *, 0x18) != 0) {
                var_r7 = 3;
            } else {
                var_r8 += 1;
                var_r10 += 1;
                if (var_r8 < (s32) M2C_FIELD(temp_r9, u8 *, 0x323)) {
                    goto loop_4;
                }
            }
        }
    }
    if (var_r7 == 2) {
        return 1U;
    }
    var_r7 += 1;
    if (var_r7 >= 3) {
        return 0U;
    }
    goto loop_1;
}
