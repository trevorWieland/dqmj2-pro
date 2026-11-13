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
extern u32 native_fn_02008e0c();
extern u32 native_fn_020944c0();
extern u32 native_fn_020a4e68();
extern u32 native_fn_ov006_021f221c();
extern u32 ov006_main_loop_set_callback_021f52cc();
extern u32 native_fn_ov006_021f52d8();
extern u32 native_fn_ov006_021f9d1c();
extern u32 native_fn_ov006_021fd960();
extern u32 native_fn_ov006_021ff434();
extern u32 native_fn_ov006_02203690();
extern u32 native_fn_ov006_02203954();
typedef struct {
    u8 field_0;
    u8 unknown_1[0x3];
    s32 field_4;
} Record_native_data_ov006_0221c11c;
extern Record_native_data_ov006_0221c11c native_data_ov006_0221c11c;
u32 native_ov006_021fd85c(void) {
    u32 var_r0;
    u32 temp_r4;

    temp_r4 = native_fn_ov006_021ff434();
    if ((native_data_ov006_0221c11c.field_4 == 0) || (var_r0 = native_fn_020944c0(), (var_r0 != 0))) {
        native_fn_02008e0c(native_fn_020a4e68(), temp_r4 + 0xF0, 0xE);
        native_fn_02008e0c(native_fn_020a4e68(), temp_r4 + 0x1F0, 0xE);
        native_fn_ov006_021f221c();
        native_fn_ov006_02203690(0);
        native_fn_ov006_02203954(0, 0x15);
        if (native_data_ov006_0221c11c.field_0 == 0) {
            native_fn_ov006_021f52d8(0, 1);
            return ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021f9d1c);
        }
        native_fn_ov006_021f52d8(0, 1);
        var_r0 = ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021fd960);
        
        return var_r0;
    }
    return var_r0;
}
