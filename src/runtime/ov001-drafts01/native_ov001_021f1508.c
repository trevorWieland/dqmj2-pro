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
extern u32 native_fn_ov001_021f0f88();
extern u8 native_data_ov001_02238f58[];
u32 native_ov001_021f1508(void) {
    s32 temp_r0;

    M2C_FIELD(native_data_ov001_02238f58, s32 *, 0x24) = 0;
    temp_r0 = (s32) native_fn_ov001_021f0f88();
    M2C_FIELD(native_data_ov001_02238f58, s32 *, 0x28) = (s32) (((s32) (temp_r0 + ((u32) (temp_r0 >> 4) >> 0x1B)) >> 5) + 1);
    return (u32) native_data_ov001_02238f58;
}
