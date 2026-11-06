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
extern u32 native_fn_ov001_021db438();
extern u32 native_fn_ov001_021dc200();
extern u32 native_fn_ov001_021f0bec();
extern u32 native_fn_ov001_021f0c40();
extern u32 native_fn_ov001_02202584();
typedef struct {
    u8 unknown_0[0xa];
    s8 field_a;
    u8 unknown_b[0x1];
    s8 field_c;
    u8 unknown_d[0x1];
    s8 field_e;
    u8 unknown_f[0x25];
    u32 field_34;
} Record_native_data_ov001_02239a14;
extern Record_native_data_ov001_02239a14 native_data_ov001_02239a14;
u32 native_ov001_021f9e10(void) {
    native_data_ov001_02239a14.field_34 = native_fn_ov001_021db438(0, native_data_ov001_02239a14.field_e);
    if (native_fn_ov001_021dc200() == 0) {
        native_data_ov001_02239a14.field_a = 0xA;
    } else {
        M2C_FIELD(native_data_ov001_02239a14.field_34, s8 *, 0x356) = (s8) native_fn_ov001_021f0bec(native_data_ov001_02239a14.field_34);
        M2C_FIELD(native_data_ov001_02239a14.field_34, s16 *, 0x346) = (s16) native_fn_ov001_021f0c40(native_data_ov001_02239a14.field_34);
        native_data_ov001_02239a14.field_a = 6;
        native_fn_ov001_02202584(M2C_FIELD(native_data_ov001_02239a14.field_34, u8 *, 0x31F));
    }
    native_data_ov001_02239a14.field_c = 3;
    return 1U;
}
