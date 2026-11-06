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
extern u32 native_fn_02040434();
extern u32 native_fn_02041510();
extern u32 native_fn_02041800();
extern u32 native_fn_0205be14();
extern u32 native_fn_ov000_021e1cc0();
extern u32 native_fn_ov000_021e2dcc();
extern u32 native_fn_ov000_02219404();
u32 native_main_0203e5e4(u8 *arg0) {
    u32 temp_r4;
    u32 temp_r4_2;
    u32 var_r5;
    u8 var_r6;

    var_r6 = *arg0;
    var_r5 = 0;
    temp_r4 = native_fn_ov000_021e1cc0();
    native_fn_ov000_021e2dcc();
    native_fn_0203dd48();
    native_fn_02040434();
    if (var_r6 == 0) {
        if ((s32) temp_r4 < 0xF) {
            temp_r4_2 = native_fn_0205be14();
            native_fn_02041510(1, 2, 0x1E);
            var_r6 = 0xA;
            native_fn_ov000_02219404(temp_r4_2);
        }
    } else if ((var_r6 == 0xA) && (native_fn_02041800() != 1)) {
        var_r5 = 1;
    }
    *arg0 = var_r6;
    return var_r5;
}
