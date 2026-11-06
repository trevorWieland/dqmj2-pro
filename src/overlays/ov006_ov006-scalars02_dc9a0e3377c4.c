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
extern u32 native_fn_ov006_021f290c();
extern u32 native_fn_ov006_021f5418();
extern u32 native_fn_ov006_022034dc();
extern u32 native_fn_ov006_022037c0();
extern u32 native_fn_ov006_022038ac();
extern u8 native_data_ov006_0221c098[];
u32 native_ov006_021f2848(u32 arg0) {
    u32 temp_r4;
    u32 temp_r5;

    temp_r5 = native_fn_ov006_022034dc(0, 0);
    temp_r4 = native_fn_ov006_021f5418(*(u32 *)native_data_ov006_0221c098, arg0);
    native_fn_ov006_022037c0(temp_r5, 0xD, 0x28, 0xE6, 0x70, 2, native_fn_ov006_021f290c(), temp_r4);
    return native_fn_ov006_022038ac(temp_r5);
}
