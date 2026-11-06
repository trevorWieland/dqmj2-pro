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
extern u32 native_fn_02041e2c();
extern u32 native_fn_02042e30();
extern u32 native_fn_ov001_021d93f8();
extern u32 native_fn_ov001_021d9424();
extern u32 native_fn_ov001_021d9494();
extern u8 native_data_ov001_02238ad4[];
extern u8 native_data_ov001_02238bd4[];
u32 native_ov001_021e32a0(void) {
    s32 sp4;
    s32 sp0;
    u32 var_r4;

    var_r4 = 0;
    if ((native_fn_ov001_021d93f8(0) != 0) && (native_fn_ov001_021d9424(native_data_ov001_02238ad4, 0, 0) != 0)) {
        native_fn_ov001_021d9494(native_data_ov001_02238ad4, 0, 1);
        native_fn_02042e30(0, &sp4, &sp0);
        native_fn_02041e2c(native_data_ov001_02238bd4, sp4, sp0, sp4);
        var_r4 = 1;
        M2C_FIELD(native_data_ov001_02238ad4, s8 *, 0x1E8) = 1;
        M2C_FIELD(native_data_ov001_02238ad4, s8 *, 0x1E9) = 1;
    }
    return var_r4;
}
