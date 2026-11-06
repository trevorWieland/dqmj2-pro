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
extern u32 native_fn_0205eb00();
extern u32 native_fn_ov001_021f1a44();
extern u32 native_fn_ov001_02204250();
extern u32 native_fn_ov001_02212838();
extern u32 native_fn_ov001_02212848();
u32 native_ov001_0221175c(void) {
    void *temp_r0;
    u32 var_r4;
    u32 temp_r5;
    s8 var_r6;

    var_r4 = 0;
    temp_r5 = native_fn_ov001_021f1a44();
    if (native_fn_ov001_02212848() != -1U) {
        if (native_fn_0205eb00() != 0) {
            return 0U;
        }
        native_fn_ov001_02212838(-1);
        goto block_4;
    }
block_4:
    var_r6 = 0;
loop_5:
    if ((M2C_FIELD((temp_r5 + var_r6), s8 *, 9) != 0x7F) && (temp_r0 = (void *) native_fn_ov001_02204250(), ((s32) M2C_FIELD(temp_r0, s16 *, 0x26) <= 0)) && (M2C_FIELD(temp_r0, u8 *, 0x23) != 0)) {
        var_r4 = 1;
    } else {
        var_r6 += 1;
        if ((s32) var_r6 < 3) {
            goto loop_5;
        }
    }
    return var_r4;
}
