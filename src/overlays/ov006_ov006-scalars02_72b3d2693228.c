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
extern u32 native_fn_ov006_021f2934();
extern u32 native_fn_ov006_021f2ac4();
extern u32 native_fn_ov006_021f535c();
extern u32 native_fn_ov006_021f53b8();
extern u32 native_fn_ov006_021f53fc();
extern u32 native_fn_ov006_021fedb8();
extern u32 native_fn_ov006_02202fd8();
extern u32 native_fn_ov006_02203188();
extern u32 native_fn_ov006_022049c4();
extern u8 native_data_ov006_0221c098[];
u32 native_ov006_021f581c(void) {
    u32 var_r0;

    var_r0 = native_fn_ov006_02203188(1);
    if (var_r0 == 0) {
        var_r0 = native_fn_ov006_02203188(0);
        if (var_r0 == 0) {
            native_fn_ov006_022049c4(0, 0);
            native_fn_ov006_022049c4(1, 0);
            native_fn_ov006_02202fd8(1);
            native_fn_ov006_02202fd8(0);
            native_fn_ov006_021f2ac4();
            native_fn_ov006_021f2934();
            native_fn_ov006_021f53fc(*(u32 *)native_data_ov006_0221c098);
            native_fn_ov006_021f53b8();
            native_fn_ov006_021fedb8();
            var_r0 = native_fn_ov006_021f535c();
        }
    }
    return var_r0;
}
