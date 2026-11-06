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
extern u32 native_fn_ov006_021f52cc();
extern u32 native_fn_ov006_021f52d8();
extern u32 native_fn_ov006_021f5a4c();
extern u32 native_fn_ov006_021f5df4();
extern u32 native_fn_ov006_021f621c();
extern u32 native_fn_ov006_021f6e98();
extern u32 native_fn_ov006_02202b24();
extern u32 native_fn_ov006_02203188();
extern u32 native_fn_ov006_02203954();
extern u32 native_fn_ov006_022043a4();
typedef struct {
    u8 field_0;
    u8 field_1;
    u8 unknown_2[0x2];
    s32 field_4;
    s32 field_8;
} Record_native_data_ov006_0221c0a8;
extern Record_native_data_ov006_0221c0a8 native_data_ov006_0221c0a8;
u32 native_ov006_021f68d0(void) {
    u32 var_r0;

    var_r0 = native_fn_ov006_02203188(1);
    if ((var_r0 == 0) && (var_r0 = native_fn_ov006_02203188(0), (var_r0 == 0)) && (var_r0 = native_fn_ov006_021f23c4(), (var_r0 != 0))) {
        native_fn_ov006_022043a4(native_data_ov006_0221c0a8.field_8);
        native_fn_ov006_021f2a4c();
        native_fn_ov006_021f2774();
        native_fn_ov006_02202b24(native_data_ov006_0221c0a8.field_4);
        native_fn_ov006_02203954(1, 1);
        native_fn_ov006_02203954(0, 0x14);
        if (native_data_ov006_0221c0a8.field_1 == 0) {
            native_fn_ov006_021f52d8(0, 0);
            return native_fn_ov006_021f52cc(native_fn_ov006_021f5a4c);
        }
        switch (native_data_ov006_0221c0a8.field_0) {
        default:
            return (u32) native_data_ov006_0221c0a8.field_0;
        case 0:
            native_fn_ov006_021f52d8(0, 1);
            return native_fn_ov006_021f52cc(native_fn_ov006_021f621c);
        case 1:
            native_fn_ov006_021f52d8(0, 1);
            return native_fn_ov006_021f52cc(native_fn_ov006_021f5df4);
        case 2:
            native_fn_ov006_021f52d8(0, 1);
            var_r0 = native_fn_ov006_021f52cc(native_fn_ov006_021f6e98);
            
            return var_r0;
        }
    } else {
        return var_r0;
    }
}
