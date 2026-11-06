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
extern u32 native_fn_ov006_021f4290();
extern u32 native_fn_ov006_021f52cc();
extern u32 native_fn_ov006_021f99d0();
extern u32 native_fn_ov006_021f9afc();
extern u32 native_fn_ov006_021f9cd0();
extern u32 native_fn_ov006_02200344();
extern u8 native_data_ov006_0221c0e4[];
u32 native_ov006_021f9970(void) {
    u32 var_r0;
    u8 temp_r0;

    var_r0 = native_fn_ov006_021f4290();
    if (var_r0 == 0) {
        temp_r0 = M2C_FIELD(*(u32 *)native_data_ov006_0221c0e4, u8 *, 0x15);
        if (temp_r0 == 0) {
            return native_fn_ov006_021f52cc(native_fn_ov006_021f99d0);
        }
        if (temp_r0 == 2) {
            native_fn_ov006_02200344(6, 3, 1, -1, 0);
            return native_fn_ov006_021f52cc(native_fn_ov006_021f9cd0);
        }
        native_fn_ov006_02200344(0x47, 2, 1, -1, 0);
        var_r0 = native_fn_ov006_021f52cc(native_fn_ov006_021f9afc);
        
        return var_r0;
    }
    return var_r0;
}
