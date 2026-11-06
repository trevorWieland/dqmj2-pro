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
extern u32 native_fn_ov006_02201aac();
extern u32 native_fn_ov006_02201f54();
extern u8 native_data_ov006_0221c16c[];
u32 native_ov006_02201fbc(void) {
    u8 temp_r0;

    temp_r0 = M2C_FIELD(*(u32 *)native_data_ov006_0221c16c, u8 *, 0xA90);
    if ((temp_r0 == 1) || (temp_r0 == 0x1A) || (temp_r0 == 0x1D)) {
        native_fn_ov006_02201f54();
        native_fn_ov006_02201aac();
        M2C_FIELD(*(u32 *)native_data_ov006_0221c16c, u8 *, 0xA90) = 2U;
        return 1U;
    }
    return 0U;
}
