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
extern u32 native_fn_ov006_021f23c4();
extern u32 native_fn_ov006_021f2774();
extern u32 native_fn_ov006_021f52cc();
extern u32 native_fn_ov006_021f52d8();
extern u32 native_fn_ov006_021f5300();
extern u32 native_fn_ov006_021f530c();
extern u32 native_fn_ov006_021fa164();
extern u32 native_fn_ov006_021fb930();
extern u32 native_fn_ov006_021fc870();
extern u32 native_fn_ov006_02203188();
extern u32 native_fn_ov006_02203690();
extern u32 native_fn_ov006_02203954();
u32 native_ov006_021fa0dc(void) {
    u32 var_r0;
    s32 sp0;

    var_r0 = native_fn_ov006_02203188(1);
    if (var_r0 == 0) {
        var_r0 = native_fn_ov006_02203188(0);
        if (var_r0 == 0) {
            var_r0 = native_fn_ov006_021f23c4();
            if (var_r0 != 0) {
                native_fn_ov006_02203690(0);
                native_fn_ov006_021f2774();
                native_fn_ov006_02203954(1, 1);
                native_fn_ov006_02203954(0, 0x15);
                native_fn_ov006_021f530c(0, &sp0);
                if (sp0 != 0) {
                    native_fn_ov006_021f52d8(2, 1);
                    return native_fn_ov006_021f52cc(native_fn_ov006_021fc870);
                }
                native_fn_ov006_021f52d8(2, 0);
                native_fn_ov006_021f5300(0, 0);
                native_fn_ov006_021fb930(0);
                var_r0 = native_fn_ov006_021f52cc(native_fn_ov006_021fa164);
                
                return var_r0;
            }
        }
    }
    return var_r0;
}
