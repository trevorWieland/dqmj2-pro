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
extern u32 native_fn_ov006_021f221c();
extern u32 native_fn_ov006_021f23c4();
extern u32 native_fn_ov006_021f2774();
extern u32 ov006_main_loop_set_callback_021f52cc();
extern u32 native_fn_ov006_021f52d8();
extern u32 native_fn_ov006_021f5724();
extern u32 native_fn_ov006_021fc08c();
extern u32 native_fn_ov006_021fd11c();
extern u32 native_fn_ov006_02203188();
extern u32 native_fn_ov006_02203690();
extern u32 native_fn_ov006_02203954();
extern u8 native_data_ov006_0221c0fc[];
u32 native_ov006_021fbf48(void) {
    u32 var_r0;

    var_r0 = native_fn_ov006_02203188(0);
    if ((var_r0 == 0) && ((*native_data_ov006_0221c0fc != 0) || (var_r0 = native_fn_ov006_02203188(1), (var_r0 == 0)))) {
        var_r0 = native_fn_ov006_021f23c4();
        if (var_r0 != 0) {
            native_fn_ov006_021f221c();
            native_fn_ov006_02203690(0);
            if (*native_data_ov006_0221c0fc == 0) {
                native_fn_ov006_021f2774();
                native_fn_ov006_02203954(1, 1);
            }
            native_fn_ov006_021f5724();
            if (*native_data_ov006_0221c0fc == 0) {
                native_fn_ov006_021f52d8(2, 1);
                return ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021fd11c);
            }
            native_fn_ov006_021f52d8(0, 0);
            var_r0 = ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021fc08c);
            
            return var_r0;
        }
    }
    return var_r0;
}
