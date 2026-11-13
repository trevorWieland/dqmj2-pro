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
extern u32 native_fn_ov006_021f54e8();
extern u32 native_fn_ov006_021f554c();
extern u32 native_fn_ov006_021f7668();
extern u32 native_fn_ov006_02203188();
typedef struct {
    u8 field_0;
    u8 field_1;
} Record_native_data_ov006_0221c0c4;
extern Record_native_data_ov006_0221c0c4 native_data_ov006_0221c0c4;
u32 native_ov006_021f7628(void) {
    u32 var_r0;

    var_r0 = native_fn_ov006_02203188(1);
    if (var_r0 == 0) {
        var_r0 = native_fn_ov006_02203188(0);
        if (var_r0 == 0) {
            if ((native_data_ov006_0221c0c4.field_0 == 0) && (native_data_ov006_0221c0c4.field_1 == 1)) {
                native_fn_ov006_021f554c();
            } else {
                native_fn_ov006_021f54e8();
            }
            var_r0 = ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021f7668);
        }
    }
    return var_r0;
}
