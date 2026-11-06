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
extern u32 native_fn_ov006_021f2848();
extern u32 native_fn_ov006_021f2ad4();
extern u32 native_fn_ov006_021f52cc();
extern u32 native_fn_ov006_021fde3c();
extern u32 native_fn_ov006_021fdeac();
extern u8 native_data_ov006_0221c12c[];
u32 native_ov006_021fde00(void) {
    *native_data_ov006_0221c12c = 0;
    native_fn_ov006_021fde3c();
    native_fn_ov006_021f2ad4(8);
    native_fn_ov006_021f26f0(0x38, -1, 0);
    native_fn_ov006_021f27fc(1);
    native_fn_ov006_021f2848(0x27);
    return native_fn_ov006_021f52cc(native_fn_ov006_021fdeac);
}
