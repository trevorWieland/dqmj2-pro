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
extern u32 native_fn_ov006_021f26f0();
extern u32 native_fn_ov006_021f27fc();
extern u32 native_fn_ov006_021f2ad4();
extern u32 native_fn_ov006_021f52cc();
extern u32 native_fn_ov006_021fc8b8();
extern u32 native_fn_ov006_021fc968();
extern u32 native_fn_ov006_021fca18();
extern u32 native_fn_ov006_021fcdb4();
extern u32 native_fn_ov006_02203c08();
typedef struct {
    u8 unknown_0[0x4];
    u32 field_4;
} Record_native_data_ov006_0221c10c;
extern Record_native_data_ov006_0221c10c native_data_ov006_0221c10c;
u32 native_ov006_021fc870(void) {
    u32 temp_r0;

    temp_r0 = native_fn_ov006_02203c08(0x20, 4);
    native_data_ov006_0221c10c.field_4 = temp_r0;
    M2C_FIELD(temp_r0, s8 *, 0x1D) = 0;
    native_fn_ov006_021fc8b8();
    native_fn_ov006_021f2ad4(1);
    native_fn_ov006_021f26f0(0x2F, -1, 0);
    native_fn_ov006_021f27fc(0);
    native_fn_ov006_021fc968();
    native_fn_ov006_021fcdb4();
    return native_fn_ov006_021f52cc(native_fn_ov006_021fca18);
}
