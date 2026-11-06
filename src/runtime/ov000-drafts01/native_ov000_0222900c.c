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
extern u32 native_fn_020627a0();
extern u32 native_fn_020628b0();
extern u32 native_fn_02062980();
extern u32 native_fn_02062a10();
extern u32 native_fn_02062a50();
extern u32 native_fn_02062a88();
extern u32 native_fn_ov000_0222976c();
extern u32 native_fn_ov000_0222985c();
typedef struct {
    u8 unknown_0[0x18];
    s16 field_18;
} Record_native_data_ov000_022474c8;
extern Record_native_data_ov000_022474c8 native_data_ov000_022474c8;
u32 native_ov000_0222900c(s32 arg0, s32 arg1) {
    s32 temp_r0_2;
    s32 temp_r0_4;
    s8 var_r7;
    s8 var_r7_2;
    u32 temp_r0;
    u32 temp_r0_3;
    u32 temp_r4;
    u32 temp_r4_2;

    temp_r4_2 = native_fn_02062a10();
    temp_r4 = native_fn_ov000_0222976c(temp_r4_2, native_fn_02062a10(arg1), native_data_ov000_022474c8.field_18);
    var_r7 = 0;
    do {
        temp_r0 = native_fn_02062a50(var_r7);
        if (temp_r0 != 0) {
            temp_r0_2 = M2C_FIELD(temp_r0, s32 *, 0x14);
            if (temp_r0_2 == arg0) {
                native_fn_020628b0(var_r7);
            } else if (temp_r0_2 == arg1) {
                native_fn_020628b0(var_r7);
            }
        }
        var_r7 += 1;
    } while ((s32) var_r7 < 3);
    var_r7_2 = 0;
    do {
        temp_r0_3 = native_fn_02062a88(var_r7_2);
        if (temp_r0_3 != 0) {
            temp_r0_4 = M2C_FIELD(temp_r0_3, s32 *, 0x14);
            if (temp_r0_4 == arg0) {
                native_fn_02062980(var_r7_2);
            } else if (temp_r0_4 == arg1) {
                native_fn_02062980(var_r7_2);
            }
        }
        var_r7_2 += 1;
    } while ((s32) var_r7_2 < 3);
    native_fn_020627a0(arg0);
    native_fn_020627a0(arg1);
    return native_fn_ov000_0222985c(temp_r4);
}
