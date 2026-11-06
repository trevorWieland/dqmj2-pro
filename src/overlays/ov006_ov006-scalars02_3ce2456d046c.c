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
extern u32 native_fn_ov006_021f3de4();
extern u32 native_fn_ov006_02202d64();
extern u32 native_fn_ov006_02204970();
extern u8 native_data_ov006_0221c05c[];
u32 native_ov006_021f2eec(void) {
    native_fn_ov006_02202d64(M2C_FIELD(*(u32 *)native_data_ov006_0221c05c, s32 *, 0x114));
    return native_fn_ov006_02204970(M2C_FIELD(*(u32 *)native_data_ov006_0221c05c, s32 *, 0x118), native_fn_ov006_021f3de4);
}
