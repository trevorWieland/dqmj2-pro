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
extern u32 native_fn_02062e18();
extern u32 native_fn_0207e874();
extern u32 native_fn_0207f3b0();
extern u32 native_fn_ov006_021e648c();
extern u32 native_fn_ov006_021e7a00();
extern u32 native_fn_ov006_021eadb0();
typedef struct {
    u8 unknown_0[0xc];
    s32 field_c;
} Record_native_data_ov006_0221c27c;
extern Record_native_data_ov006_0221c27c native_data_ov006_0221c27c;
u32 native_ov006_02206100(s32 arg0) {
    if ((arg0 != 0) && (native_fn_0207e874() != 0)) {
        native_fn_02062e18(native_data_ov006_0221c27c.field_c, native_fn_0207f3b0());
        native_fn_ov006_021eadb0(1);
        native_fn_ov006_021e7a00(0);
        return -2U;
    }
    return native_fn_ov006_021e648c(arg0);
}
