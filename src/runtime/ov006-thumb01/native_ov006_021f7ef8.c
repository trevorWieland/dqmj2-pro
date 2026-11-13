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
extern u32 native_fn_ov006_021f26f0();
extern u32 native_fn_ov006_021f27fc();
extern u32 native_fn_ov006_021f2b14();
extern u32 ov006_main_loop_set_callback_021f52cc();
extern u32 native_fn_ov006_021f530c();
extern u32 native_fn_ov006_021f7f8c();
extern u32 native_fn_ov006_021f8050();
extern u32 native_fn_ov006_021f80c4();
extern u32 native_fn_ov006_021f81b4();
extern u32 native_fn_ov006_021f8800();
extern u32 native_fn_ov006_021f8b00();
extern u32 native_fn_ov006_021f8b3c();
extern u32 native_fn_ov006_021febc4();
extern u32 native_fn_ov006_022034dc();
extern u32 ov006_clear_buffer_02203c08();
extern u32 native_fn_ov006_0220490c();
typedef struct {
    u8 field_0;
    u8 unknown_1[0x1];
    s16 field_2;
    u32 field_4;
} Record_native_data_ov006_0221c0d8;
extern Record_native_data_ov006_0221c0d8 native_data_ov006_0221c0d8;
u32 native_ov006_021f7ef8(void) {
    s32 sp0;

    native_data_ov006_0221c0d8.field_4 = ov006_clear_buffer_02203c08(0x5C, 4);
    native_fn_ov006_021f530c(&sp0, 0);
    if (sp0 == 0) {
        native_data_ov006_0221c0d8.field_0 = 0;
        native_data_ov006_0221c0d8.field_2 = 0;
    }
    M2C_FIELD(native_data_ov006_0221c0d8.field_4, s8 *, 0x51) = (s8) native_fn_ov006_021febc4(native_data_ov006_0221c0d8.field_4);
    native_fn_ov006_021f7f8c();
    native_fn_ov006_021f2b14();
    native_fn_ov006_021f26f0(0x34, -1, 0);
    native_fn_ov006_021f27fc(2);
    native_fn_ov006_021f8050();
    native_fn_ov006_021f80c4();
    M2C_FIELD(native_data_ov006_0221c0d8.field_4, u32 *, 0xC) = native_fn_ov006_022034dc(0, 0);
    M2C_FIELD(native_data_ov006_0221c0d8.field_4, u32 *, 0x3C) = native_fn_ov006_0220490c(1, native_fn_ov006_021f8b00, 0, 0x6E);
    native_fn_ov006_021f8800();
    native_fn_ov006_021f8b3c();
    return ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021f81b4);
}
