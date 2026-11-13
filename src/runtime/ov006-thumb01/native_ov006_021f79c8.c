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
extern u32 native_fn_ov006_021f218c();
extern u32 native_fn_ov006_021f26f0();
extern u32 native_fn_ov006_021f27fc();
extern u32 native_fn_ov006_021f2848();
extern u32 native_fn_ov006_021f2b14();
extern u32 native_fn_ov006_021f4e14();
extern u32 ov006_main_loop_set_callback_021f52cc();
extern u32 native_fn_ov006_021f7a10();
extern u32 native_fn_ov006_021f7a80();
extern u32 native_fn_ov006_021ff6d4();
typedef struct {
    u8 unknown_0[0x2];
    s16 field_2;
} Record_native_data_ov006_0221c0cc;
extern Record_native_data_ov006_0221c0cc native_data_ov006_0221c0cc;
u32 native_ov006_021f79c8(void) {
    native_data_ov006_0221c0cc.field_2 = 0;
    native_fn_ov006_021f7a10();
    native_fn_ov006_021f2b14();
    native_fn_ov006_021f26f0(0x36, -1, 0);
    native_fn_ov006_021f27fc(2);
    native_fn_ov006_021f2848(0x22);
    native_fn_ov006_021f218c(0);
    native_fn_ov006_021f4e14();
    native_fn_ov006_021ff6d4(0xB);
    return ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021f7a80);
}
