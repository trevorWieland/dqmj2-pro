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
extern u32 native_fn_ov001_021db8d0();
extern u32 native_fn_ov001_021dbcf0();
extern u32 native_fn_ov001_021dbd30();
u32 native_ov001_02219be0(void *arg0) {
    s32 temp_r1;
    void *temp_r4;
    s32 var_r5;
    void *var_r6;
    u32 temp_r7;

    temp_r4 = M2C_FIELD(arg0, void **, 0);
    var_r6 = M2C_FIELD(arg0, void **, 4);
    var_r5 = 0;
loop_1:
    if ((native_fn_ov001_021db8d0(var_r6) != 0) && (M2C_FIELD(temp_r4, u8 *, 0x31F) != M2C_FIELD(var_r6, u8 *, 0x31F))) {
        temp_r7 = native_fn_ov001_021dbd30(var_r6);
        temp_r1 = native_fn_ov001_021dbcf0(var_r6) * 3;
        if ((s32) temp_r7 <= (s32) ((s32) (temp_r1 + ((u32) (temp_r1 >> 1) >> 0x1E)) >> 2)) {
            return 1U;
        }
        goto block_7;
    }
block_7:
    var_r5 += 1;
    var_r6 += 0x440;
    if (var_r5 >= 3) {
        return 0U;
    }
    goto loop_1;
}
