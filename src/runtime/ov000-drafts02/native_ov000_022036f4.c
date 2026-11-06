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
extern u32 native_fn_020635d4();
extern u32 native_fn_02072f48();
extern u32 native_fn_ov000_02214a38();
typedef struct {
    u8 unknown_0[0x5];
    u8 field_5;
    u8 unknown_6[0x6];
    s16 field_c;
    u8 field_e;
} Record_native_data_ov000_02238190;
extern Record_native_data_ov000_02238190 native_data_ov000_02238190;
void native_ov000_022036f4(void) {
    u8 temp_r2;

    if ((u32) native_data_ov000_02238190.field_5 >= 0xAU) {
        return;
    }
    ++native_data_ov000_02238190.field_5;
    if (native_data_ov000_02238190.field_5 != 0xA) {
        return;
    }
    if ((native_fn_020635d4(native_data_ov000_02238190.field_c, native_data_ov000_02238190.field_e) != 0) && (native_fn_02072f48(native_data_ov000_02238190.field_c) == 0)) {
        native_fn_ov000_02214a38(native_data_ov000_02238190.field_c, native_data_ov000_02238190.field_e);
        return;
    }
    native_fn_ov000_02214a38(0x159, 0U);
}
