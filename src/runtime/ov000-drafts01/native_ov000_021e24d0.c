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
extern u32 native_fn_ov000_021d8a18();
extern u32 native_fn_ov000_021e07f0();
extern u32 native_fn_ov000_021e0bdc();
extern u32 native_fn_ov000_021e0d78();
extern u32 native_fn_ov000_021e1e40();
extern u32 native_fn_ov000_021e1fa0();
extern u32 native_fn_ov000_021e205c();
extern u32 native_fn_ov000_021e2098();
extern u32 native_fn_ov000_021e2218();
extern u32 native_fn_ov000_021e3320();
extern u8 native_data_ov000_022322c4[];
typedef struct {
    u8 unknown_0[0x274];
    u32 field_274;
    u8 unknown_278[0x6];
    s8 field_27e;
} Record_native_data_ov000_022322d4;
extern Record_native_data_ov000_022322d4 native_data_ov000_022322d4;
u32 native_ov000_021e24d0(void) {
    u16 temp_r0;
    u32 temp_r2;

    native_data_ov000_022322d4.field_27e = 1;
    temp_r0 = M2C_FIELD(M2C_FIELD(native_data_ov000_022322c4, void **, 4), u16 *, 0);
    if ((temp_r0 & 0xF0) && (!(temp_r0 & 2) || (native_fn_ov000_021d8a18() == 2))) {
        native_fn_ov000_021e1e40();
        native_fn_ov000_021e07f0(4);
    }
    if (native_fn_ov000_021d8a18() != 2) {
        native_fn_ov000_021e1fa0(1, 1);
        native_fn_ov000_021e2098();
    }
    if (M2C_FIELD(M2C_FIELD(native_data_ov000_022322c4, void **, 4), u16 *, 2) & 1) {
        native_fn_ov000_021e2218();
    } else if (native_fn_ov000_021e205c() != 0) {
        M2C_FIELD(native_data_ov000_022322c4, s32 *, 8) = 1;
    } else {
        native_fn_ov000_021e3320();
    }
    temp_r2 = native_data_ov000_022322d4.field_274 + 1;
    native_data_ov000_022322d4.field_274 = temp_r2;
    if ((temp_r2 > 0x708U) && (native_fn_ov000_021e0bdc() == 0)) {
        native_fn_ov000_021e07f0(3);
    }
    native_fn_ov000_021e0d78(1, 0, 1);
    return 0U;
}
