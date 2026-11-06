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
extern u32 native_fn_0206271c();
extern u32 native_fn_02062d24();
extern u32 native_fn_02062fd4();
extern u32 native_fn_02063038();
extern u32 native_fn_02063050();
extern u32 native_fn_02063068();
extern u32 native_fn_02063080();
extern u32 native_fn_02063098();
typedef struct {
    u8 unknown_0[0x18];
    s16 field_18;
    u8 field_1a;
    u8 unknown_1b[0x1];
    u8 field_1c;
    u8 field_1d;
    u8 field_1e;
} Record_native_data_ov000_022474c8;
extern Record_native_data_ov000_022474c8 native_data_ov000_022474c8;
extern u8 native_data_ov000_022474e8[];
extern u8 native_data_ov000_02247508[];
u32 native_ov000_0222985c(u32 arg0) {
    u32 temp_r0;

    temp_r0 = native_fn_0206271c(native_data_ov000_022474c8.field_18, native_data_ov000_022474c8.field_1a);
    native_fn_02062d24(temp_r0, native_data_ov000_022474e8);
    native_fn_02062fd4(temp_r0, native_data_ov000_02247508);
    native_fn_02063038(temp_r0, arg0);
    native_fn_02063050(temp_r0, native_data_ov000_022474c8.field_1e);
    native_fn_02063068(temp_r0, native_data_ov000_022474c8.field_1c);
    native_fn_02063080(temp_r0, native_data_ov000_022474c8.field_1d);
    native_fn_02063098(temp_r0, native_data_ov000_022474c8.field_1a);
    return temp_r0;
}
