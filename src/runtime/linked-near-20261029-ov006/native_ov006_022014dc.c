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
extern u32 native_fn_02013080();
extern u32 native_fn_ov006_02201270();
extern u32 native_fn_ov006_022012c0();
extern u32 native_fn_ov006_02201544();
extern u8 native_data_ov006_0221c164[];
u32 native_ov006_022014dc(void) {
    if ((u32) (M2C_FIELD(M2C_FIELD(native_data_ov006_0221c164, void **, 4), s32 *, 0x40) - 4) <= 2U) {
        return 1U;
    }
    native_fn_ov006_02201270(4);
    if (native_fn_02013080(native_fn_ov006_02201544, M2C_FIELD(native_data_ov006_0221c164, void **, 4) + 0x1060, (u16) M2C_FIELD(M2C_FIELD(native_data_ov006_0221c164, void **, 4), s32 *, 0x12A4), M2C_FIELD(native_data_ov006_0221c164, void **, 4) + 0xF80, (s32) (u16) M2C_FIELD(M2C_FIELD(native_data_ov006_0221c164, void **, 4), s32 *, 0x12A0), 1) != 2) {
        native_fn_ov006_022012c0();
        return 0U;
    }
    return 1U;
}
