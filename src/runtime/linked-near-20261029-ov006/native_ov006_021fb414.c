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
extern u32 native_fn_020024bc();
extern u32 native_fn_02026144();
extern u32 native_fn_ov006_021f2a4c();
extern u32 native_fn_ov006_021fabe4();
extern u32 native_fn_ov006_021fb080();
extern u32 native_fn_ov006_021fb550();
extern u32 native_fn_ov006_021fe6d0();
extern u32 native_fn_ov006_021fe6d8();
extern u32 native_fn_ov006_021fe6e8();
extern u32 native_fn_ov006_02204974();
extern u8 native_data_ov006_0221c0ec[];
u32 native_ov006_021fb414(u32 arg0) {
    s32 temp_r0;

    native_fn_ov006_021fe6e8();
    native_fn_ov006_021f2a4c();
    M2C_FIELD(native_data_ov006_0221c0ec, u16 *, 4) = (u16) (M2C_FIELD(native_data_ov006_0221c0ec, u16 *, 4) + 6);
    temp_r0 = (s32) native_fn_020024bc(M2C_FIELD(native_data_ov006_0221c0ec, u16 *, 4), 0x1D);
    if (temp_r0 >= 6) {
        return native_fn_ov006_021fb080();
    }
    M2C_FIELD(native_data_ov006_0221c0ec, u16 *, 4) = (u16) (M2C_FIELD(native_data_ov006_0221c0ec, u16 *, 4) - temp_r0);
    native_fn_ov006_021fabe4();
    native_fn_02026144(0x37 * M2C_FIELD(native_data_ov006_0221c0ec, u16 *, 4), 0x91);
    native_fn_ov006_021fe6d0();
    native_fn_ov006_021fe6d8();
    native_fn_ov006_021fb550();
    M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0ec, void **, 8), s32 *, 0x38) = 0;
    return native_fn_ov006_02204974(0, arg0);
}
