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
extern u32 native_fn_02045654();
extern u32 native_fn_020484dc();
extern u32 native_fn_020485b4();
extern u32 native_fn_02084f4c();
extern u32 native_fn_ov005_021da874();
extern u8 native_data_ov005_021e708c[];
typedef struct {
    u8 unknown_0[0x8];
    u8 field_8;
    u8 unknown_9[0xf];
    s32 field_18;
    u8 unknown_1c[0x30];
    s32 field_4c;
} Record_native_data_ov005_021e9818;
extern Record_native_data_ov005_021e9818 native_data_ov005_021e9818;
extern u8 native_data_ov005_021e992c[];
u32 native_ov005_021dc4cc(void) {
    u8 var_r6;

    if (native_data_ov005_021e9818.field_8 != 2) {
        return (u32) native_data_ov005_021e9818.field_8;
    }
    var_r6 = 0;
    native_data_ov005_021e9818.field_8 = 0U;
    if ((s32) native_data_ov005_021e9818.field_4c > 0) {
        do {
            native_fn_02084f4c(*(u32 *)(native_data_ov005_021e992c + (var_r6 * 4)));
            var_r6 += 1;
        } while ((s32) var_r6 < (s32) native_data_ov005_021e9818.field_4c);
    }
    native_fn_ov005_021da874();
    native_fn_020485b4(native_data_ov005_021e9818.field_18);
    native_fn_020484dc(0, *native_data_ov005_021e708c);
    return native_fn_02045654(1);
}
