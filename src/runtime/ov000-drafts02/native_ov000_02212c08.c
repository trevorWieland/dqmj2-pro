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
extern u32 native_fn_ov000_02212b28();
extern u32 native_fn_ov000_02212b60();
extern u32 native_fn_ov000_02212b98();
extern u32 native_fn_ov000_02212bd0();
extern u8 native_data_ov000_0224373c[];
void native_ov000_02212c08(s32 arg0) {
    s32 var_r4;
    s32 var_r4_2;
    s32 var_r4_3;
    s32 temp_r5;
    s32 var_r6;
    s32 var_r6_2;
    s32 var_r6_3;

    temp_r5 = (arg0 * 0xE0) + (s32) native_data_ov000_0224373c;
    var_r6 = temp_r5 + 0xBC;
    var_r4 = 0;
    do {
        native_fn_ov000_02212bd0(var_r6);
        var_r4 += 1;
        var_r6 += 8;
    } while (var_r4 < 4);
    var_r4_2 = temp_r5 + 0x9C;
    var_r6_2 = 0;
    do {
        native_fn_ov000_02212b98(var_r4_2);
        var_r6_2 += 1;
        var_r4_2 += 8;
    } while (var_r6_2 < 4);
    var_r4_3 = temp_r5 + 0x5C;
    var_r6_3 = 0;
    do {
        native_fn_ov000_02212b60(var_r4_3);
        var_r6_3 += 1;
        var_r4_3 += 0x10;
    } while (var_r6_3 < 4);
    native_fn_ov000_02212b28(temp_r5);
    M2C_FIELD(temp_r5, s8 *, 0xDD) = 0;
    M2C_FIELD(temp_r5, s8 *, 0xDC) = 0;
}
