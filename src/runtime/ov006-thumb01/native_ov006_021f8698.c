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
extern u32 native_fn_ov006_021f2a4c();
extern u32 ov006_main_loop_set_callback_021f52cc();
extern u32 native_fn_ov006_021f52d8();
extern u32 native_fn_ov006_021f5300();
extern u32 native_fn_ov006_021f8d4c();
extern u32 native_fn_ov006_021fc514();
extern u32 native_fn_ov006_021fd11c();
extern u32 native_fn_ov006_021fdb08();
extern u32 native_fn_ov006_021fe4dc();
extern u32 native_fn_ov006_021fe690();
extern u32 native_fn_ov006_021fea78();
extern u32 native_fn_ov006_021fedc8();
extern u32 native_fn_ov006_021fee00();
extern u32 native_fn_ov006_021ff0d0();
extern u32 native_fn_ov006_02202b24();
extern u32 native_fn_ov006_02203188();
extern u32 native_fn_ov006_02203644();
extern u32 native_fn_ov006_02203954();
extern u32 native_fn_ov006_02203c20();
extern u32 native_fn_ov006_022043a4();
extern u32 native_fn_ov006_0220498c();
extern u8 native_data_ov006_0221c0d8[];
extern u8 native_data_ov006_0221c0dc[];
u32 native_ov006_021f8698(void) {
    u32 var_r0;
    s32 var_r4;
    s32 var_r5;

    var_r0 = native_fn_ov006_02203188(1);
    if ((var_r0 != 0) || (var_r0 = native_fn_ov006_02203188(0), (var_r0 != 0)) || (var_r0 = native_fn_ov006_021f23c4(), (var_r0 == 0))) {
        return var_r0;
    }
    native_fn_ov006_0220498c(1, M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0d8, void **, 4), s32 *, 0x3C));
    var_r4 = 0;
    var_r5 = 0;
    do {
        if (M2C_FIELD((M2C_FIELD(native_data_ov006_0221c0d8, void **, 4) + var_r5), s32 *, 0x10) != 0) {
            native_fn_ov006_022043a4();
        }
        if (M2C_FIELD((M2C_FIELD(native_data_ov006_0221c0d8, void **, 4) + var_r5), s32 *, 0x24) != 0) {
            native_fn_ov006_022043a4();
        }
        var_r4 += 1;
        var_r5 += 4;
    } while (var_r4 < 5);
    native_fn_ov006_02203644(M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0d8, void **, 4), s32 *, 0xC));
    native_fn_ov006_021fe690();
    native_fn_ov006_021f2a4c();
    native_fn_ov006_021f2774();
    native_fn_ov006_021fe4dc();
    native_fn_ov006_02202b24(M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0d8, void **, 4), s32 *, 4));
    native_fn_ov006_02202b24(M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0d8, void **, 4), s32 *, 8));
    native_fn_ov006_02203954(1, 1);
    native_fn_ov006_02203954(0, 0x1D);
    M2C_FIELD((void *)0x04000010, s32 *, 0) = 0;
    M2C_FIELD((void *)0x04000010, s32 *, 8) = 0;
    if (M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0d8, void **, 4), u8 *, 0x54) == 0) {
        native_fn_ov006_021fea78();
        native_fn_ov006_021ff0d0(M2C_FIELD((void *) native_fn_ov006_021fedc8(), u8 *, 0xF4));
        native_fn_ov006_021f52d8(2, 0);
        ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021fd11c);
    } else if (M2C_FIELD(native_data_ov006_0221c0d8, u8 *, 0) == 4) {
        native_fn_ov006_021fea78();
        native_fn_ov006_021f52d8(0, 1);
        ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021fc514);
    } else {
        native_fn_ov006_021fee00(M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0d8, void **, 4), s32 *, 0) + (0x2A * M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0d8, void **, 4), u8 *, 0x52)));
        native_fn_ov006_021f52d8(0, 0);
        if (M2C_FIELD((M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0d8, void **, 4), s32 *, 0) + (0x2A * M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0d8, void **, 4), u8 *, 0x52))), u8 *, 0x28) != 0) {
            native_fn_ov006_021f52d8(0, 1);
            native_fn_ov006_021f5300(1, 1);
            ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021f8d4c);
        } else {
            native_fn_ov006_021f52d8(0, 1);
            native_fn_ov006_021f5300(0, 1);
            ov006_main_loop_set_callback_021f52cc(native_fn_ov006_021fdb08);
        }
    }
    return native_fn_ov006_02203c20(native_data_ov006_0221c0dc);
}
