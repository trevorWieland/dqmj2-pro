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
extern u32 native_fn_0202a634();
extern u32 native_fn_020491f8();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_0206940c();
extern u8 native_data_ov000_022460d4[];
u32 native_ov000_0221bcc4(s32 *arg0) {
    s32 temp_r4;
    u32 temp_r0;

    native_fn_0202a634();
    if (M2C_FIELD(native_data_ov000_022460d4, s8 *, 0x10) == 6) {
        return (u32) native_data_ov000_022460d4;
    }
    if (M2C_FIELD(native_data_ov000_022460d4, s8 *, 0x10) == 0xA) {
        return native_fn_0206940c();
    }
    temp_r4 = M2C_FIELD(native_data_ov000_022460d4, s32 *, 4);
    temp_r0 = native_fn_020491f8();
    if (temp_r0 == 0) {
        return temp_r0;
    }
    *arg0 |= 1;
    if (temp_r4 != M2C_FIELD(native_data_ov000_022460d4, s32 *, 4)) {
        return native_fn_0205e7a8(-1, 0x56);
    }
    return native_fn_0205e7a8(-1, 0x55);
}
