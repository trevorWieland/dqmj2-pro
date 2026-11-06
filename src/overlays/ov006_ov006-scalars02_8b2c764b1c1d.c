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
extern u32 native_fn_ov006_02202a80();
extern u8 native_data_ov006_0221c178[];
u32 native_ov006_02202fb8(s32 arg0, u32 arg1) {
    u32 temp_r0;
    u8 sp0[4];

    temp_r0 = native_fn_ov006_02202a80(arg1, &sp0, 4);
    *(u32 *)(native_data_ov006_0221c178 + (arg0 * 4)) = temp_r0;
    return temp_r0;
}
