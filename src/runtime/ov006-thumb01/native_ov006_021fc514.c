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
extern u32 native_fn_ov006_021f52cc();
extern u32 native_fn_ov006_021fc564();
extern u32 native_fn_ov006_021fc5d4();
extern u32 native_fn_ov006_021fea58();
extern u32 native_fn_ov006_021feaa0();
extern u32 native_fn_ov006_021ff6d4();
typedef struct {
    u8 field_0;
    u8 unknown_1[0x1];
    s16 field_2;
} Record_native_data_ov006_0221c108;
extern Record_native_data_ov006_0221c108 native_data_ov006_0221c108;
u32 native_ov006_021fc514(void) {
    native_data_ov006_0221c108.field_2 = 0;
    native_data_ov006_0221c108.field_0 = 0;
    native_fn_ov006_021fc564();
    native_fn_ov006_021f26f0(0x33, -1, 0);
    native_fn_ov006_021f2b14();
    native_fn_ov006_021f27fc(2);
    native_fn_ov006_021f2848(0x33);
    native_fn_ov006_021f218c(0);
    native_fn_ov006_021fea58();
    native_fn_ov006_021feaa0();
    native_fn_ov006_021ff6d4(0xA);
    return native_fn_ov006_021f52cc(native_fn_ov006_021fc5d4);
}
