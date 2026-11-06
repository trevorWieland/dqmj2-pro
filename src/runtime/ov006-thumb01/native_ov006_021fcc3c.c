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
extern u32 native_fn_ov006_021f2370();
extern u32 native_fn_ov006_021f52cc();
extern u32 native_fn_ov006_021fcc90();
extern u32 native_fn_ov006_021fedc8();
extern u32 native_fn_ov006_02203188();
extern u32 native_fn_ov006_022031a0();
extern u8 native_data_ov006_0221c10c[];
u32 native_ov006_021fcc3c(void) {
    u32 var_r0;

    var_r0 = native_fn_ov006_02203188(1);
    if (var_r0 == 0) {
        if ((M2C_FIELD(M2C_FIELD(native_data_ov006_0221c10c, void **, 4), u8 *, 0x1D) == 1) && ((M2C_FIELD(native_data_ov006_0221c10c, u8 *, 0) == 3) || (M2C_FIELD((void *) native_fn_ov006_021fedc8(), u8 *, 0xE7) != 0xFF))) {
            native_fn_ov006_021f2370();
        }
        native_fn_ov006_022031a0(3, 1, 1, 8);
        native_fn_ov006_022031a0(3, 0, 0x14, 8);
        var_r0 = native_fn_ov006_021f52cc(native_fn_ov006_021fcc90);
    }
    return var_r0;
}
