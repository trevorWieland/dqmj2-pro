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
extern u32 native_fn_020273d8();
extern u32 native_fn_0202a090();
extern u32 native_fn_0202a1e0();
extern u32 native_fn_0202a32c();
extern u32 native_fn_0206258c();
extern u32 native_fn_0207a9ec();
extern u32 native_fn_ov006_021e3f28();
typedef struct {
    u8 field_0;
    u8 unknown_1[0x3];
    u32 field_4;
} Record_native_data_ov006_02218d18;
extern Record_native_data_ov006_02218d18 native_data_ov006_02218d18;
u32 native_ov006_021e3c08(void) {
    if (native_fn_0202a32c(7) == 0) {
        native_fn_0202a090(7, 0x41000);
    }
    native_fn_0202a090(2, 0x29800);
    native_fn_0202a090(1, 0xAF000);
    native_data_ov006_02218d18.field_0 = (u8) native_fn_0202a1e0(1);
    native_data_ov006_02218d18.field_4 = native_fn_0207a9ec(1);
    native_fn_020273d8(4);
    native_fn_ov006_021e3f28(0);
    return native_fn_0206258c(0);
}
