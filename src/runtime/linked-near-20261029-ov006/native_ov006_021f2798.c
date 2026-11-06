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
extern u32 native_fn_0201d780();
extern u32 native_fn_ov006_021f5328();
extern u8 native_data_ov006_0220b138[];
extern u8 native_data_ov006_0221c010[];
u32 native_ov006_021f2798(void *arg0) {
    u32 temp_r0;

    native_fn_0201d780(native_data_ov006_0221c010, arg0, 0x3F);
    if (M2C_FIELD(arg0, u8 *, 5) == 0x78) {
        return (u32) native_data_ov006_0221c010;
    }
    temp_r0 = native_fn_ov006_021f5328();
    if ((M2C_FIELD(arg0, u8 *, 5) == 0x79) && (temp_r0 != 0)) {
        return (u32) native_data_ov006_0221c010;
    }
    M2C_FIELD(native_data_ov006_0221c010, u8 *, 5) = (u8) native_data_ov006_0220b138[temp_r0];
    return (u32) native_data_ov006_0221c010;
}
