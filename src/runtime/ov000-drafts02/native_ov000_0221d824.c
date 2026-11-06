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
extern u32 native_fn_0206d114();
extern u32 native_fn_ov000_0221f8a0();
extern u8 native_data_ov000_02246340[];
void native_ov000_0221d824(void *arg0, s32 arg1) {
    s32 temp_r0;
    s8 temp_r0_2;
    s32 var_r7;
    s32 var_r8;
    u8 *var_r9;

    if (M2C_FIELD(arg0, s8 *, 0x10) != 1) {
        return;
    }
    if (((arg1 != 0) && (M2C_FIELD(arg0, s32 *, 0) == 2)) || (((s32) M2C_FIELD(arg0, s32 *, 0) < 2) && (native_fn_ov000_0221f8a0() == 0))) {
        var_r7 = -1;
    } else if ((arg1 != 0) && (temp_r0 = M2C_FIELD(arg0, s32 *, 0), (temp_r0 > 2))) {
        var_r7 = temp_r0 - 1;
    } else {
        var_r7 = M2C_FIELD(arg0, s32 *, 0);
    }
    var_r8 = 0;
    var_r9 = native_data_ov000_02246340;
    do {
        temp_r0_2 = (s8) *var_r9;
        if (temp_r0_2 != -1) {
            if (var_r7 == var_r8) {
                native_fn_0206d114(temp_r0_2, 1);
            } else {
                native_fn_0206d114(temp_r0_2, 0);
            }
        }
        var_r8 += 1;
        var_r9 += 1;
    } while (var_r8 < 5);
}
