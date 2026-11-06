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
extern u32 native_fn_0203dd48();
extern u32 native_fn_0203e660();
extern u32 native_fn_02040434();
extern u32 native_fn_0205f35c();
extern u32 native_fn_ov000_021d8c80();
extern u32 native_fn_ov000_021e1cc0();
u32 native_main_0203e928(u8 *arg0) {
    u32 var_r4;
    u8 var_r5;

    var_r5 = *arg0;
    var_r4 = 0;
    native_fn_ov000_021e1cc0();
    native_fn_0203dd48();
    native_fn_02040434();
    if (var_r5 == 0) {
        native_fn_ov000_021d8c80(1);
        native_fn_0205f35c(-1, 0xA8);
        var_r5 = 0xA;
    } else if ((var_r5 == 0xA) && (native_fn_0203e660(2, 0) != 0)) {
        var_r4 = 1;
    }
    *arg0 = var_r5;
    return var_r4;
}
