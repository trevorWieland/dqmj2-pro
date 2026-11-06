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
extern u32 native_fn_0206cc70();
extern u32 native_fn_ov000_02215078();
extern u32 native_fn_ov000_02215960();
extern u8 native_data_ov000_0224532c[];
typedef struct {
    u8 unknown_0[0x496];
    s8 field_496;
} Record_native_data_ov000_022459b4;
extern Record_native_data_ov000_022459b4 native_data_ov000_022459b4;
extern u8 native_data_ov000_022459c4[];
extern u8 native_data_ov000_02245a0c[];
extern u8 native_data_ov000_02245a6c[];
u32 native_ov000_02215850(void) {
    s8 var_r4;
    u8 *var_r5;

    native_fn_0206cc70(2);
    var_r4 = 0;
    var_r5 = native_data_ov000_02245a6c;
    native_data_ov000_022459b4.field_496 = 0;
    do {
        native_fn_ov000_02215960(var_r5);
        var_r4 += 1;
        var_r5 += 0x50;
    } while ((s32) var_r4 < 0xC);
    native_fn_ov000_02215078(native_data_ov000_022459c4, 1);
    native_fn_ov000_02215078(native_data_ov000_02245a0c, 1);
    M2C_FIELD(native_data_ov000_0224532c, s32 *, 0x1C) = 0;
    return (u32) native_data_ov000_0224532c;
}
