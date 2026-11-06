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
extern u32 native_fn_ov006_021f4014();
extern u32 native_fn_ov006_021f4260();
extern u32 native_fn_ov006_021f4270();
extern u32 native_fn_ov006_021f4280();
extern u32 native_fn_ov006_021f52cc();
extern u32 native_fn_ov006_021f96bc();
extern u32 native_fn_ov006_021f98d0();
extern u32 native_fn_ov006_021ff6d4();
extern u32 native_fn_ov006_02203188();
extern u8 native_data_ov006_0221c0e4[];
u32 native_ov006_021f965c(void) {
    u32 var_r0;

    var_r0 = native_fn_ov006_02203188(1);
    if (var_r0 == 0) {
        var_r0 = native_fn_ov006_02203188(0);
        if (var_r0 == 0) {
            native_fn_ov006_021f4014();
            native_fn_ov006_021ff6d4(0x14);
            if (M2C_FIELD(*(u32 *)native_data_ov006_0221c0e4, u8 *, 0x14) == 0) {
                native_fn_ov006_021f4260(0);
                native_fn_ov006_021f4280(0);
            } else {
                if (native_fn_ov006_021f98d0(0x1A) != 0) {
                    native_fn_ov006_021f4270(0);
                }
                native_fn_ov006_021f4280(0);
            }
            var_r0 = native_fn_ov006_021f52cc(native_fn_ov006_021f96bc);
        }
    }
    return var_r0;
}
