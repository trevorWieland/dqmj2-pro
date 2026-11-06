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
extern u32 native_fn_0205fae8();
extern u32 native_fn_0205fb3c();
extern u32 native_fn_ov001_02202360();
extern u32 native_fn_ov001_022043f0();
typedef struct {
    u8 unknown_0[0xc];
    s8 field_c;
} Record_native_data_ov001_02239c10;
extern Record_native_data_ov001_02239c10 native_data_ov001_02239c10;
u32 native_ov001_02202478(u32 arg0, u32 arg1, u32 arg2) {
    u32 temp_r0;

    temp_r0 = native_fn_ov001_02202360(native_data_ov001_02239c10.field_c);
    native_fn_ov001_022043f0(temp_r0 + 0x60, arg0, arg1, arg2);
    native_fn_0205fb3c(temp_r0 + 0x60, 3);
    return native_fn_0205fae8(temp_r0 + 0x60, (u8) (M2C_FIELD(temp_r0, u8 *, 0x80) - 4));
}
