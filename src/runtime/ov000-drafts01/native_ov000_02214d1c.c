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
extern u32 native_fn_0202a1e0();
extern u32 native_fn_0204074c();
extern u32 native_fn_02048e74();
extern u32 native_fn_02048e8c();
extern u32 native_fn_02068ae8();
extern u32 native_fn_0206c644();
extern u32 native_fn_0206c6c0();
extern u32 native_fn_ov000_02214f3c();
extern u32 native_fn_ov000_02215000();
extern u32 native_fn_ov000_02219d8c();
typedef struct {
    u8 field_0;
    s8 field_1;
    s8 field_2;
    u8 unknown_3[0x1];
    s32 field_4;
    s32 field_8;
    s32 field_c;
} Record_native_data_ov000_02245314;
extern Record_native_data_ov000_02245314 native_data_ov000_02245314;
extern u8 native_data_ov000_0224531c[];
u32 native_ov000_02214d1c(void) {
    native_data_ov000_02245314.field_0 = (u8) native_fn_0202a1e0(2);
    native_fn_02048e74(native_data_ov000_0224531c, 1);
    if (native_fn_ov000_02215000() != 0) {
        native_data_ov000_02245314.field_8 = 1;
    } else {
        native_data_ov000_02245314.field_c = 0;
        native_data_ov000_02245314.field_8 = 0;
        if (native_fn_0204074c() == 1) {
            native_fn_ov000_02219d8c(1);
        }
    }
    native_fn_ov000_02214f3c();
    native_fn_02048e8c();
    native_fn_0202a1e0((s8) native_data_ov000_02245314.field_0);
    native_data_ov000_02245314.field_2 = 0x7F;
    native_data_ov000_02245314.field_1 = (s8) native_data_ov000_02245314.field_8;
    native_data_ov000_02245314.field_4 = 1;
    native_fn_0206c644();
    native_fn_02068ae8();
    return native_fn_0206c6c0(2);
}
