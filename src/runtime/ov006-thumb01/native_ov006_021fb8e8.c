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
extern u32 ov006_main_loop_set_callback_021f52cc();
extern u32 native_fn_ov006_021fb918();
extern u32 native_fn_ov006_021fe5cc();
extern u32 native_fn_ov006_021ff6d4();
extern u32 native_fn_ov006_02200548();
extern u32 native_fn_ov006_02200574();
extern u8 native_data_ov006_0221c0ec[];
u32 native_ov006_021fb8e8(void) {
    u32 var_r0;

    var_r0 = native_fn_ov006_02200574();
    if (var_r0 == 0) {
        native_fn_ov006_021ff6d4(6);
        native_fn_ov006_02200548();
        native_fn_ov006_021fe5cc(M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0ec, void **, 8), s32 *, 0xC));
        var_r0 = ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021fb918);
    }
    return var_r0;
}
