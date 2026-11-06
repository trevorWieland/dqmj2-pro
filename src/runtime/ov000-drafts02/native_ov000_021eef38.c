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
extern u32 native_fn_020484dc();
extern u32 native_fn_020485b4();
extern u32 native_fn_020c1c20();
extern u32 native_fn_020c1cb8();
extern u32 native_fn_020c1e50();
typedef struct {
    u8 field_0;
    u8 unknown_1[0x3];
    s32 field_4;
} Record_native_data_ov000_02236bd0;
extern Record_native_data_ov000_02236bd0 native_data_ov000_02236bd0;
extern u8 native_data_ov000_02236bd8[];
extern u8 native_data_ov000_02236bdc[];
extern u8 native_data_ov000_02236be0[];
extern u8 native_data_ov000_02236be4[];
extern u8 native_data_ov000_02236bec[];
extern u8 native_data_ov000_02236c04[];
void native_ov000_021eef38(void) {
    s32 var_r5;
    u8 *var_r5_2;
    u8 *var_r6;
    s32 var_r6_2;

    native_fn_020c1e50(2, native_data_ov000_02236be0);
    var_r6 = native_data_ov000_02236bec;
    var_r5 = 0;
    do {
        native_fn_020c1cb8(2, var_r6);
        var_r5 += 1;
        var_r6 += 4;
    } while (var_r5 < 6);
    var_r5_2 = native_data_ov000_02236c04;
    var_r6_2 = 0;
    do {
        native_fn_020c1cb8(2, var_r5_2);
        var_r6_2 += 1;
        var_r5_2 += 4;
    } while (var_r6_2 < 6);
    native_fn_020c1cb8(2, native_data_ov000_02236bd8);
    native_fn_020c1cb8(2, native_data_ov000_02236bdc);
    native_fn_020c1e50(2, native_data_ov000_02236be4);
    if (native_data_ov000_02236bd0.field_4 != 0) {
        native_fn_020485b4();
    }
    native_fn_020484dc(1, native_data_ov000_02236bd0.field_0);
    native_fn_020c1c20(0);
}
